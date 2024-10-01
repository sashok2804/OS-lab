import os

def is_valid_directory(directory):
    return os.path.exists(directory) and os.path.isdir(directory)
