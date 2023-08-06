"""
Methods for locating and proofreading .tsv files.
"""

# module dependencies
import csv
import logging
from os import listdir
from os.path import isfile, join
from operator import itemgetter
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)
LOGGER = logging.getLogger(__name__)


def list_tsv_files(dir_name):
    """
    Returns a list of all .tsv files in a given directory.

    The directory name must be a str or a path-like object.
    """
    print(Fore.BLUE + "Getting tsv files...")

    entries = listdir(dir_name)

    files = [
        join(dir_name, f)
        for f in entries
        if isfile(join(dir_name, f)) and f.endswith(".tsv")
    ]

    if len(files) > 0:
        text_color = Fore.GREEN
    elif len(files) == 0:
        text_color = Fore.RED
    print(text_color + Style.BRIGHT + f"{str(len(files))} tsv files located.\n")
    print(Style.RESET_ALL)
    return files


def _fieldname_discrepancies(fieldnames_key, fieldnames):
    """
    Checks for a difference in the members of fieldnames and fieldnames_key.

    Both fieldnames and fieldnames_key must be sets. Fieldnames_key is the set
    used to check membership of fieldnames against.

    A discrepancy is detected if any members of fieldnames aren't members of
    fieldnames_key. Prints an informative message and returns True if a
    discrepancy is detected.

    Returns False if no discrepancies are detected.

    Checking membership is one-sided; There may be members of fieldnames_key
    that aren't members of fieldnames. This would be true if there are multiple
    .tsv files with different fieldnames that need to be merged. In that case,
    fieldnames_key would be the set of all fieldnames needed in the merged file,
    and fieldnames would only be made up of the fieldnames in a single .tsv file.
    """
    if not isinstance(fieldnames_key, set):
        raise TypeError("fieldnames_key must be a set.")

    # Calculate the difference in the sets
    fieldname_difference = fieldnames - fieldnames_key
    if len(fieldname_difference) != 0:
        msg = f"{len(fieldname_difference)} extra field name(s) detected:"
        msg += f" {fieldname_difference} not present in fieldnames_key."
        print(Fore.RED + Style.BRIGHT + msg)
        return True

    return False


def _record_discrepancies(record, line_num):
    """
    Determines if there are any missing or extra fields in the given record. The
    records of a DictReader object are passed to this method and as such, must
    be dictionaries.

    When the DictReader reads from a .tsv file, any missing fields are filled in
    with None type. Any extra fields are placed in a field named 'QUESTIONABLE'.
    This method simply looks for the presence of any fields with None type or
    data under 'QUESTIONABLE'.

    If missing or extra fields are detected, an informative message is printed
    and True is returned.

    Returns False if no missing/extra fields are detected.
    """
    msg = Fore.RED + Style.BRIGHT + f"Line {line_num}:"
    extra_fields = False
    missing_fields = set()
    # Examine the fields in the record for missing or extra fields
    for key in record:
        if record[key] is None:
            missing_fields.add(key)
        elif key == "MISPLACED FIELDS":
            extra_fields = record[key]
    # Determine the message that should be printed based on any missing/extra fields
    if len(missing_fields) > 0:
        msg += f" {len(missing_fields)} missing record(s) detected:"
        msg += f" Field(s) {missing_fields} is(are) missing."
    elif extra_fields:
        msg += f" Extra fields detected: {extra_fields}"
    else:
        return False

    print(msg)
    return True


def proofread(fieldnames_key, tsv_file):
    """
    Proof-read over the field names and the records in the given .tsv file.

    Requires a 'key' set of field names to check record field membership against
    and a .tsv file.

    Prints detailed messages and returns 1 if any discrepancies are detected.
    Otherwise, prints a confirmation and returns 0.
    """
    print(Fore.BLUE + f"Proof-reading {tsv_file}...")

    with open(tsv_file, newline="") as tsvfile:
        # Create the csv reader with tab set as delimiter.
        tsv_reader = csv.DictReader(tsvfile, restkey="MISPLACED FIELDS", delimiter="\t")
        # Check for discrepancies in the field names
        fieldnames = set(tsv_reader.fieldnames)
        fieldname_discrepancies = _fieldname_discrepancies(fieldnames_key, fieldnames)
        # Check for discrepancies in the records
        record_discrepancies = False
        for record in tsv_reader:
            tmp = _record_discrepancies(record, tsv_reader.line_num)
            if record_discrepancies is False and tmp is True:
                record_discrepancies = tmp

    if not fieldname_discrepancies and not record_discrepancies:
        print(Style.BRIGHT + Fore.GREEN + "No discrepancies found.")
        print(Style.RESET_ALL)
        return 0

    return 1


def sort_dict_reader_by_fieldname(file, fieldname, delimiter="\t"):
    """
    Returns a sorted list of records from the given .tsv file.

    The list is sorted by the given fieldname.
    """
    if not file.endswith(".tsv"):
        raise TypeError(f"{file} is not a .tsv file.")

    with open(file, newline="") as tsvfile:
        tsv_reader = csv.DictReader(tsvfile, delimiter=delimiter)
        return sorted(tsv_reader, key=itemgetter(fieldname))
