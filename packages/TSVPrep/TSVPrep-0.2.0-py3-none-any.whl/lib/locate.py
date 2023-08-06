"""
Methods for locating files of a specific extension type.
"""
from os import listdir
from os.path import isfile, join


def list_files_by_ext_type(dir_name, ext_type):
    """
    Returns a list of all files in a given directory with the given extension.

    The directory name must be a str or a path-like object.
    """

    entries = listdir(dir_name)

    files = [
        join(dir_name, f)
        for f in entries
        if isfile(join(dir_name, f)) and f.endswith(ext_type)
    ]

    return files
