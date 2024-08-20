import os
import shutil

def copy_directory(source_path, dest_path):
    """
    Recursively copy the contents of one directory to another.

    :param source_path:     The source directory path
    :param dest_path:       The destination directory path
    """
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    os.makedirs(dest_path) 

    for item in os.listdir(source_path):
        source_item = os.path.join(source_path, item)
        dest_item = os.path.join(dest_path, item)

        if os.path.isdir(source_item):
            copy_directory(source_item, dest_item)
        else:
            shutil.copy(source_item, dest_item)
