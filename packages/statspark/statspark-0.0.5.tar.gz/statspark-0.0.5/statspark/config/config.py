
from collections import namedtuple
import re


RegisteredOption = namedtuple(
    "RegisteredOption", 
    "key defval doc validator"
)
def is_tuple_str(x):
    if not isinstance(x, tuple):
        msg = 'qgf.available_dbname should be a tuple, not {}.'
        raise ValueError(msg.format(type(x)))
    for item in x:
        if not isinstance(item, str):
            msg = 'Elements in qgf.available_dbname should be str, not {}.'
            raise ValueError(msg.format(type(item)))
    return None
def is_str(x):
    if not isinstance(x, str):
        raise ValueError('qgf.dbname must be str, not {}'.format(type(x)))
    return None
_global_config = {
    'qgf': {
        'available_dbname': ('bigquery', 'postgres'),
        'dbname': 'bigquery'
    }
}
_registered_options = {
    'qgf.available_dbname': RegisteredOption(
        key = "qgf.available_dbname",
        defval = ('bigquery', 'postgres'),
        doc =\
            "\n (str)\n    " +\
            "All available dbnames that are supported.",
        validator = is_tuple_str
    ),
    'qgf.dbname': RegisteredOption(
        key = 'qgf.dbname',
        defval = 'bigquery',
        doc =\
            "\n: str\n    " +\
            "A current dbname. Default is 'bigquery'.\n" +\
            "See qgf.available_dbname for all available dbnames.",
        validator = is_str
    )
}


class CallableDynamicDoc:
    def __init__(self, func):
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)
class DictWrapper:
    def __init__(self, d, prefix = ""):
        object.__setattr__(self, "d", d)
        object.__setattr__(self, "prefix", prefix)

    def __setattr__(self, key, val):
        prefix = object.__getattribute__(self, "prefix")
        if prefix:
            prefix += "."
        prefix += key
        if key in self.d and not isinstance(self.d[key], dict):
            _set_option(prefix, val)
        else:
            raise KeyError("Value cannot be set to nonexisting options.")

    def __getattr__(self, key):
        prefix = object.__getattribute__(self, "prefix")
        if prefix:
            prefix += "."
        prefix += key
        try:
            v = object.__getattribute__(self, "d")[key]
        except KeyError:
            raise KeyError("No such option exists.")
        if isinstance(v, dict):
            return DictWrapper(v, prefix)
        else:
            return _get_option(prefix)

    def __dir__(self):
        return list(self.d.keys())    
def _get_option(pat):
    key = _get_single_key(pat)
    root, k = _get_root(key)
    
    return root[k]
def _get_registered_option(key):

    return _registered_options.get(key)
def _get_root(key):
    path = key.split(".")
    cursor = _global_config
    for p in path[:-1]:
        cursor = cursor[p]
    return cursor, path[-1]
def _get_single_key(pat):
    keys = _select_options(pat)
    if len(keys) == 0:
        raise KeyError("No such keys: {pat!r}".format(pat = pat))
    if len(keys) > 1:
        raise KeyError("Pattern matched multiple keys.")
    key = keys[0]
    
    return key
def _select_options(pat):
    if pat in _registered_options:
        return [pat]
    keys = sorted(_registered_options.keys())
    if pat == 'all':
        return keys
    
    return [k for k in keys if re.search(pat, k, re.I)]
def _set_option(*args, **kwargs):
    nargs = len(args)
    if not nargs or nargs % 2 != 0:
        msg = "Must provide an even number of non-keyword arguments."
        raise ValueError(msg)
    silent = kwargs.pop("silent", False)
    if kwargs:
        msg2 = '_set_option() got an unexpected keyword argument "{kwarg}"'
        raise TypeError(msg2.format(list(kwargs.keys())[0]))
    for k, v in zip(args[::2], args[1::2]):
        key = _get_single_key(k)
        o = _get_registered_option(key)
        if o and o.validator:
            o.validator(v)
        
        root, k = _get_root(key)
        root[k] = v


get_option = CallableDynamicDoc(_get_option)
options = DictWrapper(_global_config)
set_option = CallableDynamicDoc(_set_option)
