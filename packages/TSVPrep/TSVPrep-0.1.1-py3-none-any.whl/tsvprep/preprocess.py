"""
Preprocessing tools for delimited text files.
"""

# module dependencies
import csv
from operator import itemgetter


def _diff_fieldnames(fieldnames, fieldnames_key):
    """
    Returns the difference in the members of fieldnames and fieldnames_key.

    Checking membership is one-sided; There may be members of fieldnames_key
    that aren't members of fieldnames. This would be true if there are multiple
    delimited text files with different fieldnames that need to be merged. In
    that case, fieldnames_key would be the set of all fieldnames needed in the
    merged file, and fieldnames would only be made up of the fieldnames in a
    single delimited text file.
    """
    fieldnames = set(fieldnames)

    # Calculate the difference in the sets
    return fieldnames - fieldnames_key


def _missing_fields(record):
    """
    Accepts a record from a csv.DictReader object and determines if any
    fields have been filled in with None by the DictReader. Returns a list of
    field names that have been filled in with None type, or false if all fields are
    present.
    """
    missing_fields = False
    for key in record:
        if record[key] is None:
            if not missing_fields:
                missing_fields = []
            missing_fields.append(key)

    return missing_fields


def _extra_fields(record, restkey):
    """
    Accepts a record from a csv.DictReader object and determines if any extra
    fields are present in the column named after the 'restkey' passed to the
    csv.DictReader constructor.

    Returns the list of extra fields or False if no extra fields are present.
    """
    extra_fields = False
    for key in record:
        if key == restkey:
            extra_fields = record[key]

    return extra_fields


def _record_discrepancy(record, restkey):
    """
    Checks the record for missing or extra fields and returns a string describing
    the missing or extra fields.
    """

    if _missing_fields(record):
        return f"Missing fields: {_missing_fields(record)}"

    if _extra_fields(record, restkey):
        return f"Extra fields: {_extra_fields(record, restkey)}"

    return False


def file_integrity_scan(file, fieldnames_key, restkey="EXTRA FIELDS", delimiter="\t"):
    """
    Opens file as a csv.DictReader object and scans the file for fieldname discrepancies,
    missing fields, or extra fields.

    Data pertaining to the previously mentioned items is stored in a dictionary.
    The keys of the dictionary describe where the discrepancy can be found. The
    value stored under the key describes the discrepancy itself. This data is
    intended to be used in reporting/logging later on.
    """
    fieldnames_key = set(fieldnames_key)
    integrity_data = dict()

    with open(file, newline="") as delimited_file:
        # Create the csv reader with tab set as delimiter.
        reader = csv.DictReader(delimited_file, restkey=restkey, delimiter=delimiter)
        if _diff_fieldnames(reader.fieldnames, fieldnames_key):
            key = str(reader.line_num)
            integrity_data[key] = _diff_fieldnames(reader.fieldnames, fieldnames_key)
        for record in reader:
            key = str(reader.line_num)
            if _record_discrepancy(record, restkey):
                integrity_data[key] = _record_discrepancy(record, restkey)
    return integrity_data


def sort_by_fieldname(file, fieldname, delimiter="\t"):
    """
    Returns a sorted list of records from the given delimited text file.

    The list is sorted by the given fieldname.
    """

    with open(file, newline="") as delimited_file:
        reader = csv.DictReader(delimited_file, delimiter=delimiter)
        return sorted(reader, key=itemgetter(fieldname))
