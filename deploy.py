import argparse

info = """
Super User Stone 0.0
"""


def parse():
    parser = argparse.ArgumentParser(description='Super User Stone')
    parser.add_argument('-i', '--input',
                        dest='depot',
                        required=False,
                        default=".",
                        help='configuration depot')
    parser.add_argument('--install',
                        dest='install',
                        action='store_true',
                        help='install given programs (use sus_installations.cfg)')
    parser.set_defaults(install=False)

    args = parser.parse_args()
    return args


def deploy(args):
    print(str(args))
    pass


if __name__ == "__main__":
    args = parse()
    deploy(args)