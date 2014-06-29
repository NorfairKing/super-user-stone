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

from installation import Installation
from configuration import Configuration
from relocation import Relocation

import config as conf

info = """
Super User Stone 0.4
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description='Super User Stone')
parser.add_argument('-i', '--input',
                    dest='depot',
                    required=True,
                    default=False,
                    help='configuration depot')
parser.add_argument('--dry',
                    dest='dry',
                    action='store_true',
                    default=False,
                    help='don\'t actually do anything, just show what would happen.')
parser.add_argument('--install',
                    dest='install',
                    action='store_true',
                    default=False,
                    help='Install all preferred packages as specified in \'installations.sus\'.')
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

#installations
installations_file = os.path.join(depot, conf.INSTALLATIONS_FILE_NAME)
installations_file_exists = os.path.isfile(installations_file)
if installations_file_exists:
    installations_parser = util.get_parser(installations_file)
    installations_parse_succes = not (installations_parser is None)

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
    if (args.install):
        deploy_installations()
    deploy_configurations()
    deploy_relocations()
    if args.last_run_file:
        make_last_run_file()


def deploy_installations():
    """
    Deploy installations as specified by the config file.
    """
    print()

    print("Installations:")
    if args.color:
        print(text_util.status_block(installations_file_exists), end="")
    print("SUS installations config file existence")
    if not installations_file_exists:
        return
    if args.color:
        print(text_util.status_block(installations_parse_succes), end="")
    print("Parse Succes")
    if not installations_parse_succes:
        return

    print()

    installs = []
    for option, cfg in installations_parser.items(conf.SUDO_INSTALLATION_SECTION):
        print(option, cfg)
        installs.append(Installation(command=option, arguments=cfg, sudo=True))

    for option, cfg in installations_parser.items(conf.DEFAULT_INSTALLATION_SECTION):
        print(option, cfg)
        installs.append(Installation(command=option, arguments=cfg, sudo=False))

    for i in installs:
        i.deploy()


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
        c.evaluate(args=args)

    print()
    print()


def deploy_relocations():
    """
    Deploy relocations as specified by the config file.
    """
    print()

    print("Relocations:")
    if args.color:
        print(text_util.status_block(relocations_file_exists), end=" ")
    print("SUS relocations config file existence")
    if not relocations_file_exists:
        return
    if args.color:
        print(text_util.status_block(relocations_parse_succes), end=" ")
    print("Parse Succes")
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
