import os


def file_delete(file):
    if os.path.isfile(file.path):
        os.remove(file.path)
