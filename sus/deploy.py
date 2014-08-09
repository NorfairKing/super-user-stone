"""
The deploy script.
"""

import os
import sys
import argparse
import subprocess
from os.path import expanduser

import util
import text_util

from configuration import Configuration

import config as conf

info = """
Super User Stone 0.5
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description='Super User Stone')
parser.add_argument('-d', '--depot',
                    dest='depot',
                    required=True,
                    default=False,
                    help='configuration depot')
parser.add_argument('--dry',
                    dest='dry',
                    action='store_true',
                    default=False,
                    help='don\'t actually do anything, just show what would happen.')
parser.add_argument('--replace',
                    dest='replace',
                    action='store_true',
                    default=False,
                    help='replace existing files')
parser.add_argument('--copy',
                    dest='copy',
                    action='store_true',
                    default=False,
                    help='copy configurations instead of linking them')
parser.add_argument('--no-last-run-file',
                    dest='last_run_file',
                    action='store_false',
                    default=True,
                    help='Don\'t make a last-run file.')
parser.add_argument('--rerun',
                    dest='rerun',
                    action='store_true',
                    default=False,
                    help='Do nothing else but re run the last deployment.')
parser.add_argument('--colorless',
                    dest='color',
                    action='store_false',
                    default=True,
                    help='Don\'t use any colors.')
parser.set_defaults(dry=False, copy=False)
args = parser.parse_args()

depot = util.expand(args.depot)

#configurations
configurations_file = os.path.join(depot, conf.CONFIGURATIONS_FILE_NAME)
configurations_file_exists = os.path.isfile(configurations_file)
if configurations_file_exists:
    configurations_parser = util.get_parser(configurations_file)
    configurations_parse_succes = not (configurations_parser is None)


def deploy():
    """
    Deploy SUS entirely
    """

    deploy_configurations()

    if args.last_run_file:
        make_last_run_file()

def deploy_configurations():
    """
    Deploy configurations as specified by the config file.
    """
    print()

    print("Configurations:")
    if args.color:
        print(text_util.status_block(configurations_file_exists), end=" ")
    print("SUS configurations config file existence")
    if not configurations_file_exists:
        return
    if args.color:
        print(text_util.status_block(configurations_parse_succes), end=" ")
    print("Parse Succes")
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

    for c in configs:
        c.evaluate(args=args)

    print()
    print()

def make_last_run_file():
    """
    Make the last run file
    """
    with open(os.path.join(depot, conf.LAST_RUN_FILE), 'w') as f:
        f.write(" ".join(sys.argv))


def rerun():
    """
    Rerun the last deployment.
    """
    with open(os.path.join(depot, conf.LAST_RUN_FILE), 'r') as f:
        cmd = "python3 " + f.readline()
        process = subprocess.Popen(cmd, shell=True)
        process.wait()


if __name__ == "__main__":
    if args.rerun:
        rerun()
        exit()
    print(info)
    deploy()
