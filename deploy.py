import os
import argparse
from os.path import expanduser

import util

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

depot = os.path.abspath(args.depot)

configurations_file = os.path.join(depot, DEFAULT_CONFIGURATIONS_FILE_NAME)
configurations_file_exists = os.path.isfile(configurations_file)
if configurations_file_exists:
    configurations_parser = util.get_parser(configurations_file)
    configurations_parse_error = configurations_parser is None

def deploy():
    deploy_configurations()


def deploy_configurations():
    print(depot)


if __name__ == "__main__":
    print(info)
    deploy()