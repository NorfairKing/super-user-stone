import os
import sys
import argparse
from os.path import expanduser

import util
import text_util

from configuration import Configuration

with open("last_use.txt", "w") as text_file:
    print("Last time SUS was deployed, you used the following command: " + " ".join(sys.argv), file=text_file)


info = """
Super User Stone 0.0
"""

# Constants
DEFAULT_CONFIGURATIONS_FILE_NAME = "sus_configurations.cfg"


# Parse command line arguments
parser = argparse.ArgumentParser(description='Super User Stone')
parser.add_argument('-i', '--input',
                    dest='depot',
                    required=True,
                    help='configuration depot')
parser.add_argument('--dry',
                    dest='dry',
                    action='store_true',
                    help='don\'t actually do anything, just show what would happen.')
parser.add_argument('--replace',
                    dest='replace',
                    action='store_true',
                    help='replace existing files')
parser.add_argument('--copy',
                    dest='copy',
                    action='store_true',
                    help='copy configurations instead of linking them')
parser.set_defaults(dry=False, copy=False)
args = parser.parse_args()

depot = util.expand(args.depot)

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

    configs = []
    sections = configurations_parser.sections()
    for section in sections:
        for option, cfg in configurations_parser.items(section):
            config_file_name = option
            destination_path = os.path.join(expanduser(section), cfg)
            configs.append(Configuration(depot, config_file_name, destination_path))

    for c in configs:
        c.deploy(args=args)

    print()
    print()


if __name__ == "__main__":
    print(info)
    deploy()