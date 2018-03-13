import csv
import os
import json
from typing import Iterable, Dict

import datetime


def save_to_file(header, row_generator, filename, overwrite=False):
    if not overwrite and os.path.isfile(filename):
        raise FileExistsError("The given filename '%s' already exists and "
                              "overwrite is set to False".format(filename))

    with open(filename, "w") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        writer.writerow(header)
        writer.writerows(row_generator)


def save_to_json_file(json_iterable: Iterable[Dict], basedir, overwrite=False):
    """
    Dumps a iterable of jsons into a single JSON file, where the jsons
    are enclosed in a single list called data.

    This function will collect the entire iterable into a list (in-memory)
    before attempting to dump it into a file, so be cautious about the
    file size.
    :param json_iterable: The source of json
    :param basedir: The base directory to place the dumped results
    :param overwrite: Whether any existing files with the input filename
    should be overwritten.
    :return:
    """
    assert os.path.isdir(basedir), "The base directory doesnt exist."

    filename = _generate_results_filename(basedir)
    if not overwrite and os.path.isfile(filename):
        raise FileExistsError("The given filename '%s' already exists and "
                              "overwrite is set to False".format(filename))

    with open(filename + ".json", "w") as file:
        data = {"data": list(json_iterable)}
        json.dump(data, file, indent=4)


def serialize_sparse_vector(array):
    indices = ",".join(
        str(idx) + ":" + "{:.8f}".format(val) for idx, val in enumerate(array)
        if val != 0)
    return str(len(array)) + "," + indices


def _generate_results_filename(basedir) -> str:
    """Generate a folder named after the current date inside basedir"""
    date = datetime.datetime.today().strftime("%Y-%m-%d-%H_at_%M-%S")
    filename = os.path.join(basedir, date)
    return filename
