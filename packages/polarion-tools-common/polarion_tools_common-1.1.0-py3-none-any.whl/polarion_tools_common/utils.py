"""Utility functions."""

import os


def merge_dicts(dict_a, dict_b):
    """Merge dict_b into dict_a."""
    if not (isinstance(dict_a, dict) and isinstance(dict_b, dict)):
        return dict_a

    mergeable = (list, set, tuple)
    for key, value in dict_b.items():
        if key in dict_a and isinstance(value, mergeable) and isinstance(dict_a[key], mergeable):
            new_list = set(dict_a[key]).union(value)
            dict_a[key] = sorted(new_list)
        elif key not in dict_a or not isinstance(value, dict):
            dict_a[key] = value
        else:
            merge_dicts(dict_a[key], value)

    return dict_a


def get_unicode_str(obj):
    """Make sure obj is a valid unicode string."""
    if isinstance(obj, str):
        text = obj
    elif isinstance(obj, bytes):
        text = obj.decode("utf-8", errors="ignore")
    else:
        text = str(obj)
    return text


def find_in_parent_dirs(path, filenames, stop_in=()):
    """Search up from a given path to find files."""
    prev, path = None, os.path.abspath(path)
    while prev != path:
        if any(os.path.exists(os.path.join(path, d)) for d in filenames):
            return path
        dirname = os.path.basename(path.rstrip("/"))
        if any(dirname == d for d in stop_in):
            return None
        prev, path = path, os.path.abspath(os.path.join(path, os.pardir))
    return None


def find_tests_marker(path, markers=(".polarion_tests",), stop_in=("site-packages",)):
    """Search up from a given path to find the tests markers."""
    return find_in_parent_dirs(path, markers, stop_in=stop_in)


def find_vcs_root(path, dirs=(".git",)):
    """Search up from a given path to find the project root."""
    return find_in_parent_dirs(path, dirs)
