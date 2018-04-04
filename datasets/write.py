import csv
import os
import json
from typing import Iterable, Dict

import datetime


class Writer:
    """
    The writer encapsulates all methods needed into an injectable
    dependency.
    """

    @staticmethod
    def save_to_file(header, row_generator, filename, overwrite=False):
        if not overwrite and os.path.isfile(filename):
            raise FileExistsError("The given filename '%s' already exists and "
                                  "overwrite is set to False".format(filename))

        with open(filename, "w") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)

            writer.writerow(header)
            writer.writerows(row_generator)

    @staticmethod
    def save_to_json_file(json_iterable: Iterable[Dict], basedir,
                          overwrite=False):
        """
        Dumps a iterable of jsons into a single JSON file, where the
        jsons are enclosed in a single list called data.

        This function will collect the entire iterable into a list
        (in-memory) before attempting to dump it into a file, so be
        cautious about the file size.
        :param json_iterable: The source of json
        :param basedir: The base directory to place the dumped results
        :param overwrite: Whether any existing files with the input
        filename should be overwritten.
        :return:
        """
        assert os.path.isdir(basedir), "The base directory doesnt exist."

        filename = Writer._generate_results_filename(basedir)
        if not overwrite and os.path.isfile(filename):
            raise FileExistsError("The given filename '%s' already exists and "
                                  "overwrite is set to False".format(filename))

        with open(filename + ".json", "w") as file:
            data = {"data": list(json_iterable)}
            json.dump(data, file, indent=4)

    @staticmethod
    def serialize_sparse_vector(array):
        serialized_key_values_lst = []
        for idx, val in enumerate(array):
            if val is not 0:
                entry = Writer._serialize_dict_entry(idx, val)
                serialized_key_values_lst.append(entry)
        serialized_key_values = ",".join(serialized_key_values_lst)
        vector_dim = str(len(array))
        return vector_dim + "," + serialized_key_values

    @staticmethod
    def _serialize_dict_entry(key, val):
        return str(key) + ":" + "{:.8f}".format(val)

    @staticmethod
    def _generate_results_filename(basedir) -> str:
        """
        Generate a folder named after the current date inside basedir
        """
        date = datetime.datetime.today().strftime("%Y-%m-%d_at_%H-%M-%S")
        filename = os.path.join(basedir, date)
        return filename
