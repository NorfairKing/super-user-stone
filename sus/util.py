import os
import shutil
import configparser
from os.path import expanduser


def expand(path):
    return os.path.abspath(expanduser(path))

def remove(path):
    os.remove(expand(path))

def remove_dir(path):
    shutil.rmtree(path)

def unlink(path):
    os.unlink(expand(path))

def copy(src, dst):
    shutil.copy(expand(src), expand(dst))

def link(src, dst):
    os.symlink(expand(src), expand(dst))

def get_parser(path):
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str
    try:
        config_parser.read(path)
    except configparser.ParsingError:
        return None
    return config_parser