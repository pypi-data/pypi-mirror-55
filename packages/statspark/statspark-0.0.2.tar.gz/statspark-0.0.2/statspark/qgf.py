
def count_null(table_name, column_names, sql_type = 'bigquery'):
    '''(str, [str][, str]) -> str

    Return the query that counts the number of NULLs at each column
    in column_names of table_name. sql_type is either 'bigquery' or
    'postgres'.

    >>> # e.g.1 bigquery
    >>> colnames = ['RowId', 'IntersectionId']
    >>> gic_train =\\
    ... "kaggle-competition-datasets.geotab_intersection_congestion.train"
    >>> # count_null(gic_train, colnames, 'bigquery')
    >>> # e.g.2 postgres
    >>> colnames2 = ['store', 'storetype', 'competitiondistance']
    >>> # count_null('train_feateng', colnames2, 'postgres')
    '''

    nulls_counted = "SELECT {ccws} FROM {tbl}"
    ccw = "COUNT(CASE WHEN {0} IS NULL THEN 1 END) AS {0}, "
    ccws = ''.join(map(lambda x: ccw.format(x), column_names))[:-2]
    nulls_counted = nulls_counted.format(
        ccws = ccws,
        tbl = "`" + table_name + "`" if sql_type == 'bigquery' \
            else table_name
    )

    if sql_type == 'bigquery':
        bq_nc = "('{0}', SUM({0})), "
        null_count =\
            "".join(map(lambda x: bq_nc.format(x), column_names))[:-2]
        get_query =\
            '''
            SELECT 
                r.* 
            FROM (
                SELECT [
                    STRUCT<column_name STRING, null_count INT64>
                    {0}
                ] AS row
                FROM (
                    {1}
                ) AS nulls_counted
            ), 
            UNNEST(row) AS r;
            '''\
            .format(null_count, nulls_counted)
    else:
        column_name =\
            "UNNEST(ARRAY[{0}])".format(
                ''.join(map(lambda x: "'" + x + "', ", column_names))[:-2]
            )
        null_count =\
            "UNNEST(ARRAY[{0}])".format(
                ''.join(map(lambda x: x + ", ", column_names))[:-2]
            )
        get_query =\
            '''
            SELECT
                {0} AS column_name, 
                {1} AS null_count 
            FROM (
                {2}
            ) AS nulls_counted;
            '''\
            .format(column_name, null_count, nulls_counted)

    return get_query
