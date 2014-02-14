import os
import shutil
import configparser
from os.path import expanduser


def expand(path):
    return expanduser(path)


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