"""
SUS configuration
"""

import os
import socket

import util
import text_util
from deployment import Deployment

import config as conf


class Configuration(Deployment):
    """
    A class of configuration deployments.
    Any instance of this class represents a deployment of exactly one config file.
    """

    def __init__(self, depot, config_file_name, destination_path):
        """
        Initialize all information that is needed to perform and evaluate the deployment of this configuration.
        @param depot: The path to the depot folder.
        @param config_file_name: The name of the config file to deploy.
        @param destination_path: The path to the destination of the config file.
        """
        self.depot = depot
        self.config_file_name = config_file_name

        self.shared_folder_path = os.path.join(depot, conf.SHARED_FOLDER_NAME)
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
        """
        Deploy this configuration.
        @param args: The parsed arguments from the command-line.
        """
        self.check_before()
        self.link(args)
        self.check_after()

    def check_before(self):
        """
        Check the state of the configuration before deployment.
        """
        self.src_exists = os.path.exists(self.source)
        self.src_is_file = os.path.isfile(self.source)
        self.src_is_link = os.path.islink(self.source)
        self.src_is_dir = os.path.isdir(self.source)

        self.dst_exists_before = os.path.exists(self.destination)
        self.dst_is_file_before = os.path.isfile(self.destination)
        self.dst_is_link_before = os.path.islink(self.destination)
        self.dst_is_dir_before = os.path.isdir(self.destination)

    def check_after(self):
        """
        Check the state of the configuration after deployment.
        """
        self.dst_exists_after = os.path.exists(self.destination)
        self.dst_is_file_after = os.path.isfile(self.destination)
        self.dst_is_link_after = os.path.islink(self.destination)
        self.dst_is_dir_after = os.path.isdir(self.destination)

    def link(self, args):
        """
        Actually deploy the configuration by linking the correct spot to the original file.
        @param args: The parsed arguments from the command-line.
        """
        if args.dry:
            print(str(self.source) + " -> " + str(self.destination))
            return

        if not self.src_exists:
            return

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
                # File already exists and isn't going to be replaced.
                return
        else:
            #This is some weird nonsense conserning broken links
            if self.dst_is_link_before:
                util.unlink(self.destination)

        if args.copy:
            util.copy(self.source, self.destination)
        else:
            util.link(self.source, self.destination)


    def evaluate(self, args):
        """
        Evaluate the deployment of this configuration.
        @param args: The parsed arguments from the command-line.
        """
        if args.dry:
            return

        def get_blocks(bool_list):
            result = ""
            for b in bool_list:
                result += " " + text_util.status_block(b)
            return result[1:]

        blocks = list()
        blocks.append(self.src_exists)
        blocks.append(self.dst_exists_after)
        blocks.append(
            self.src_is_dir == self.dst_is_dir_after and self.src_is_file == self.dst_is_file_after)

        if args.copy:
            blocks.append(not self.dst_is_link_after)
        else:
            blocks.append(self.dst_is_link_after)

        print(get_blocks(blocks) + " " + self.source + " -> " + self.destination)
