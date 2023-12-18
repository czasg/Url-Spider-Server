# coding: utf-8


def any2str(obj):
    if not obj:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, list):
        return any2str(obj[0])
    return f"{obj}"


def any2list(obj):
    if not obj:
        return []
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        return obj
    return [f"{obj}"]
