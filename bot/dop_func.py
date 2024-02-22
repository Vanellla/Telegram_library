import os
import string
import random

from settings import tmp_files


def get_hex_string():
    alf = string.hexdigits[:16]
    return "".join([random.choice(alf) for x in range(32)])

def clean_tmp_files():
    folder = tmp_files
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except:
            pass