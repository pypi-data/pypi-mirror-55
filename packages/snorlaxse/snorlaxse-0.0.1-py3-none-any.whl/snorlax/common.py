import os


def is_exists_ds_store(path):
    if '.DS_Store' in os.listdir(path):
        print(".DS_Store does exists.")
