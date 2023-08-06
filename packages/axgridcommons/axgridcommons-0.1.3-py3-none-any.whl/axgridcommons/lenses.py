# coding: utf-8

from pprint import pprint


def get(data, path, default=None):
    """
    Возвращает элемент по указанному пути
    {"a": {"b": {"c": 5}}}
    assert get(a.b.c) == 5
    :param data: dict
    :param path: пусть с раздилителем .
    :param default: значение по умолчанию, может быть задано как массив для каждого шага
    :return: значение / default
    """
    if "." not in path:
        return data.item(path, default)
    keys = path.split('.')
    _d = data
    if isinstance(default, list):
        _defaults = default
        default = None
    else:
        _defaults = None

    print("%s, %s, %s, %s" % (data, path, default, _defaults))
    for key in keys:
        if key in _d:
            _d = _d[key]
            if _defaults:
                _defaults.pop(0)
        else:
            if _defaults and len(_defaults):
                return _defaults[0]
            return default
    return _d


def set(data, path, value, errors=None):
    if "." not in path:
        data[path] = value
        return data

    keys = path.split('.')
    _d = data
    for key in keys[:-1]:
        if key not in _d:
            _d[key] = {}
        _d = _d[key]
    _d[keys[-1]] = value
    return data
