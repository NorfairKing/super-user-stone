import os
import socket

from deployment import Deployment

import util
import text_util

DEFAULT_SHARED_FOLDER_NAME = "shared"


class Configuration(Deployment):
    def __init__(self, depot, config_file_name, destination_path):
        self.depot = depot
        self.config_file_name = config_file_name

        self.shared_folder_path = os.path.join(depot, DEFAULT_SHARED_FOLDER_NAME)
        self.host_folder_path = os.path.join(depot, socket.gethostname())

        self.config_in_shared_folder = os.path.join(self.shared_folder_path, self.config_file_name)
        self.config_in_host_folder = os.path.join(self.host_folder_path, self.config_file_name)

        self.shared_config_exists = os.path.exists(self.config_in_shared_folder)
        self.host_config_exists = os.path.exists(self.config_in_host_folder)

        self.source = None
        if self.shared_config_exists:
            self.source = self.config_in_shared_folder
        if self.host_config_exists:
            self.source = self.config_in_host_folder
        self.destination = destination_path


    def deploy(self, args):
        self.check_before()
        self.link(args)
        self.check_after()
        if not args.dry:
            self.evaluate()

    def check_before(self):
        self.dst_exists_before = os.path.exists(self.destination)
        self.dst_is_file_before = os.path.isfile(self.destination)
        self.dst_is_link_before = os.path.islink(self.destination)
        self.dst_is_dir_before = os.path.isdir(self.destination)

    def check_after(self):
        self.dst_exists_after = os.path.exists(self.destination)
        self.dst_is_file_after = os.path.isfile(self.destination)
        self.dst_is_link_after = os.path.islink(self.destination)
        self.dst_is_dir_after = os.path.isdir(self.destination)

    def link(self, args):
        if args.dry:
            print(str(self.source) + " -> " + str(self.destination))
            return

        if args.copy:
            if self.dst_exists_before:
                os.remove(self.destination)
            util.copy(self.source, self.destination)
        else:
            if self.dst_exists_before:
                if args.replace:
                    if self.dst_is_link_before:
                        util.unlink(self.destination)
                    elif self.dst_is_file_before:
                        util.remove(self.destination)
                    elif self.dst_is_dir_before:
                        util.remove_dir(self.destination)
                    else:
                        #SUS should never get here.
                        raise Exception("WTF is this shit")
                else:
                    # ("file " + self.destination + " already exists")
                    return
            util.link(self.source, self.destination)


    def evaluate(self):
        def get_blocks(bool_list):
            result = ""
            for b in bool_list:
                result += " " + text_util.status_block(b)
            return result[1:]

        blocks = [True, False] #For testing purpses.
        #TODO actual evaluation

        print(get_blocks(blocks) + " " + self.source + " -> " + self.destination)