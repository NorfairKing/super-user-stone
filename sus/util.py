"""
SUS utility functions
"""

import os
import shutil
import subprocess
import configparser
from os.path import expanduser


def expand(path):
    """
    Expand a given path to an absolute path.
    @param path: The given path.
    @return: The expansion of the given path.
    """
    return os.path.abspath(expanduser(path))


def remove(path):
    """
    Remove the file at a given path.
    @param path: The given path.
    """
    os.remove(expand(path))


def remove_dir(path):
    """
    Remove the directory at a given path
    @param path: The given path.
    """
    shutil.rmtree(path)


def unlink(path):
    """
    Unlink the symbolic link at the given path.
    @param path: The given path.
    """
    os.unlink(expand(path))


def copy(src, dst):
    """
    Copy a file from a given source to a given destination.
    @param src: The given source.
    @param dst: The given destination
    """
    dst = expand(dst)
    src = expand(src)
    ensure_dir(dst)
    shutil.copy(src, dst)


def link(src, dst):
    """
    Link a file from a given source to a given destionation.
    @param src: The given source.
    @param dst: The given destination
    """
    dst = expand(dst)
    src = expand(src)
    ensure_dir(dst)
    os.symlink(src, dst)

def ensure_dir(file):
    d = os.path.dirname(file)
    if not os.path.exists(d):
        os.makedirs(d)



def get_parser(path):
    """
    Get a config parser for a given config file.
    @param path: The path to a config file.
    @return: If there are parse errors in the config file, return none, else: a parser for the given file.
    """
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str
    try:
        config_parser.read(path)
    except configparser.ParsingError:
        return None
    return config_parser


def call(command_string, sudo):
    if sudo:
        command_string = "sudo " + command_string

    process = subprocess.Popen(command_string, shell=True)
    process.wait()