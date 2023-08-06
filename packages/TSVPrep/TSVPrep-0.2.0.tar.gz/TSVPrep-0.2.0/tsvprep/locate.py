"""
Methods for locating files of a specific extension type.
"""
from os import listdir
from os.path import isfile, join, splitext


def list_files_by_ext_type(dir_name, ext, join_dir_name=True):
    """
    Returns a list of all files in dir_name with file extension in ext.
    ext can be a str or a list; the extension is checked the same way.

    join may be either True or False; if True, dir_name is joined to the file
    name and added to the list. Otherwise, just the filename is returned.

    The directory name must be a str or a path-like object.
    """

    entries = listdir(dir_name)

    if join_dir_name:
        files = [
            join(dir_name, f)
            for f in entries
            if isfile(join(dir_name, f)) and splitext(f)[1] in ext
        ]
    else:
        files = [
            f for f in entries if isfile(join(dir_name, f)) and splitext(f)[1] in ext
        ]

    return files
