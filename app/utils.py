import os


def store_datasets(data):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "..", "data", data.filename)
    data.save(file_path)
    return file_path
