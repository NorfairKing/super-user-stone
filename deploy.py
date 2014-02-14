import os
import argparse
from os.path import expanduser

import util
import text_util

from configuration import Configuration

info = """
Super User Stone 0.0
"""

# Constants
DEFAULT_CONFIGURATIONS_FILE_NAME = "sus_configurations.cfg"


# Parse command line argument
parser = argparse.ArgumentParser(description='Super User Stone')
parser.add_argument('-i', '--input',
                    dest='depot',
                    required=True,
                    help='configuration depot')
parser.add_argument('--copy',
                    dest='copy',
                    action='store_true',
                    help='copy configurations instead of linking them')
parser.set_defaults(copy=False)
args = parser.parse_args()

depot = os.path.abspath(expanduser(args.depot))

configurations_file = os.path.join(depot, DEFAULT_CONFIGURATIONS_FILE_NAME)
configurations_file_exists = os.path.isfile(configurations_file)
if configurations_file_exists:
    configurations_parser = util.get_parser(configurations_file)
    configurations_parse_succes = not (configurations_parser is None)


def deploy():
    deploy_configurations()


def deploy_configurations():
    print()

    print("Configurations:")
    print(text_util.status_block(configurations_file_exists), "File Exists")
    if not configurations_file_exists:
        return
    print(text_util.status_block(configurations_parse_succes), "Parse Succes")
    if not configurations_parse_succes:
        return

    print()

    configs= []
    sections = configurations_parser.sections()
    for section in sections:
        for option, cfg in configurations_parser.items(section):
            config_file_name = option
            destination_path = os.path.join(expanduser(section), cfg)
            configs.append(Configuration(depot, config_file_name, destination_path))
            print(option, os.path.join(expanduser(section), cfg))

    print()
    print()

if __name__ == "__main__":
    print(info)
    deploy()