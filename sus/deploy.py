"""
The deploy script.
"""

import os
import argparse
from os.path import expanduser

import util
import text_util

from configuration import Configuration
from relocation import Relocation

import config as conf

info = """
Super User Stone 0.2
"""

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

#configurations
configurations_file = os.path.join(depot, conf.CONFIGURATIONS_FILE_NAME)
configurations_file_exists = os.path.isfile(configurations_file)
if configurations_file_exists:
    configurations_parser = util.get_parser(configurations_file)
    configurations_parse_succes = not (configurations_parser is None)

#relocations
relocations_file = os.path.join(depot, conf.RELOCATIONS_FILE_NAME)
relocations_file_exists = os.path.isfile(relocations_file)
if relocations_file_exists:
    relocations_parser = util.get_parser(relocations_file)
    relocations_parse_succes = not (relocations_parser is None)


def deploy():
    """
    Deploy SUS entirely
    """
    deploy_configurations()
    deploy_relocations()


def deploy_configurations():
    """
    Deploy configurations as specified by the config file.
    """
    print()

    print("Configurations:")
    print(text_util.status_block(relocations_file_exists), "SUS configurations config file existence")
    if not relocations_file_exists:
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
        c.evaluate(args=args)

    print()
    print()


def deploy_relocations():
    """
    Deploy relocations as specified by the config file.
    """
    print()

    print("Relocations:")
    print(text_util.status_block(relocations_file_exists), "SUS relocations config file existence")
    if not relocations_file_exists:
        return
    print(text_util.status_block(relocations_parse_succes), "Parse Succes")
    if not relocations_parse_succes:
        return

    print()

    relocs = []
    sections = relocations_parser.sections()
    for section in sections:
        for option, cfg in relocations_parser.items(section):
            relocation_file_name = option
            destination_path = os.path.join(expanduser(section), cfg)
            relocs.append(Relocation(depot, relocation_file_name, destination_path))

    for r in relocs:
        r.deploy(args=args)
        r.evaluate(args=args)

    print()
    print()


def deploy_installations():
    """
    Deploy installations as specified by the config file.
    """


if __name__ == "__main__":
    print(info)
    deploy()
