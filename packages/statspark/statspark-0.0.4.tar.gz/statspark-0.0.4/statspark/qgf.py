
sql_type = 'bigquery'


def count_distinct(table_name, column_names, sql_type = sql_type):
    '''(str, str or [str][, str]) -> str

    Return the query that counts the number of unique values at each
    column in column_names (or column_names if column_names is a string) 
    of table_name.
    sql_type is either 'bigquery' or 'postgres'.
    '''

    counted = request_each(
        table_name, 
        column_names, 
        "COUNT(DISTINCT({0})) AS {0}",
        sql_type
    )
    get_query = transpose(
        counted, column_names, 'column_name', 'num_distinct', sql_type
    )

    return get_query
def count_null(table_name, column_names, sql_type = sql_type):
    '''(str, str or [str][, str]) -> str

    Return the query that counts the number of NULLs at each column
    in column_names (or column_names if column_names is a string) of 
    table_name.
    sql_type is either 'bigquery' or 'postgres'.

    >>> # e.g.1 bigquery
    >>> colnames = ['RowId', 'IntersectionId']
    >>> gic_train =\\
    ... "kaggle-competition-datasets.geotab_intersection_congestion.train"
    >>> # count_null(gic_train, 'RowId', 'bigquery')
    >>> # count_null(gic_train, colnames, 'bigquery')
    >>> # e.g.2 postgres
    >>> colnames2 = ['store', 'storetype', 'competitiondistance']
    >>> # count_null('train_feateng', colnames2, 'postgres')
    '''

    counted = request_each(
        table_name, 
        column_names, 
        "COUNT(CASE WHEN {0} IS NULL THEN 1 END) AS {0}",
        sql_type
    )
    get_query = transpose(
        counted, column_names, 'column_name', 'num_null', sql_type
    )

    return get_query
def is_unique(table_name, column_names, sql_type = sql_type):
    '''(str, str or [str][, str]) -> str

    If column_names is a string, return the query that checks whether 
    values at each record in column_names are unique across table_name.
    If column_names is a list of str, return the query that check whether 
    the combination of values at each record in column_names are unique
    across table_name. 
    sql_type is either 'bigquery' or 'postgres'.
    '''

    tbl = "`{0}`" if sql_type == 'bigquery' else "{0}"
    tbl = tbl.format(table_name)
    counters = "COUNT({0}) AS nrow, COUNT(DISTINCT({1})) AS distinct_{2}"
    if isinstance(column_names, str):
        names = column_names
        counters =\
            counters.format(column_names, column_names, names)
    else:
        if len(column_names) == 1:
            return is_unique(table_name, column_names[0], sql_type)
        casters = "CAST({col} AS {type}), '_', "
        casters = ''.join(map(
            lambda x: casters.format(
                col = x, 
                type = "STRING" if sql_type == 'bigquery' else 'TEXT'
            ), 
            column_names
        ))
        concats = "CONCAT({0})".format(casters[:-7])
        names = '_'.join(column_names)
        counters = counters.format(column_names[0], concats, names)
    get_query =\
        '''
        SELECT
            nrow,
            distinct_{names},
            sub.nrow = sub.distinct_{names} AS is_unique
        FROM (
            SELECT
                {counters}
            FROM
                {tbl}
        ) AS sub
        '''\
        .format(names = names, counters = counters, tbl = tbl)
    
    return get_query
def request_each(table_name, column_names, request, sql_type = sql_type):
    '''(str, str or [str], str[, str]) -> str

    Return the query that performs a requested computation `request` at 
    each column in column_names of table_name. A place of column should be
    denoted as "{0}" in `request`.
    sql_type is either 'bigquery' or 'postgres'.

    >>> # e.g.
    >>> request1 = "COUNT(DISTINCT({0})) AS {0}"
    >>> request2 = "COUNT(CASE WHEN {0} IS NULL THEN 1 END) AS {0}"
    '''

    if isinstance(column_names, str):
        column_names = [column_names]
    tbl = "`{0}`" if sql_type == 'bigquery' else "{0}"
    tbl = tbl.format(table_name)
    requests = ', '.join(map(lambda x: request.format(x), column_names))

    return "SELECT {0} FROM {1}".format(requests, tbl)
def transpose(query, column_names, key = 'key', value = 'value', 
              sql_type = sql_type):
    '''(str, str or [str][, str, str, str]) -> str

    Precondition: 
    1. `query` should be a query that returns a 1-by-k table.
    2. `column_names` must match with the list of all column names of the 
        table returned by `query`.

    Return the query that transposes a 1-by-k table (obtainable by 
    `query` argument), column names exactly matching with `column_names`,
    where k is the number of columns and the row contains numbers. `key` 
    will be the name of "column" column in the new table, and `value` will
    be the name of value column. 
    `sql_type` is either 'bigquery' or 'postgres'.
    '''

    if sql_type == 'bigquery':
        bq_sums = "('{0}', {0})"
        summed = ", ".join(map(lambda x: bq_sums.format(x), column_names))
        get_query =\
            '''
            SELECT 
                r.* 
            FROM (
                SELECT [
                    STRUCT<{k} STRING, {v} INT64>
                    {uakv}
                ] AS row
                FROM (
                    {base_tbl}
                ) AS result
            ), 
            UNNEST(row) AS r
            '''\
            .format(
                k = key, v = value, 
                uakv = summed, 
                base_tbl = query
            )
    else: # postgres
        keys =\
            "UNNEST(ARRAY[{0}])"\
                .format("'" + "', '".join(column_names) + "'")
        values =\
            "UNNEST(ARRAY[{0}])"\
                .format(', '.join(column_names))
        get_query =\
            '''
            SELECT
                {uak} AS {k}, 
                {uav} AS {v} 
            FROM (
                {base_tbl}
            ) AS result
            '''\
            .format(
                uak = keys, k = key,
                uav = values, v = value,
                base_tbl = query
            )

    return get_query
