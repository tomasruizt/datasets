import csv
import os


def save_to_file(header, row_generator, filename, overwrite=False):

    if not overwrite and os.path.isfile(filename):
        raise FileExistsError("The given filename '%s' already exists and overwrite is set to False".format(filename ))

    with open(filename, "w") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        writer.writerow(header)
        writer.writerows(row_generator)
