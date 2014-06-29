"""
SUS relocation
"""

import os

import util
import text_util
from deployment import Deployment

import config as conf


class Relocation(Deployment):
    """
    A class of folder relocations.
    Any instance of this class represents a relocation of exactly one folder.
    """

    def __init__(self, depot, reloc_folder_name, destination_path):
        """
        Initialize all information that is needed to perform and evaluate this relocation.
        @param depot: The path to the depot folder.
        @param reloc_folder_name: The name of the folder to relocate.
        @param destination_path: The path to the destination of the relocation folder
        """
        self.depot = depot
        self.reloc_folder_name = reloc_folder_name
        self.relocs_folder_path = os.path.join(depot, conf.RELOCS_FOLDER_NAME)

        self.source = os.path.join(self.relocs_folder_path, self.reloc_folder_name)
        self.destination = destination_path

    def deploy(self, args):
        """
        Deploy this relocation.
        @param args: The parsed arguments from the command-line.
        """
        self.check_before()
        self.relocate(args)
        self.check_after()

    def check_before(self):
        """
        Check the state of the relocation before deployment.
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
        Check the state of the relocation after deployment.
        """
        self.dst_exists_after = os.path.exists(self.destination)
        self.dst_is_file_after = os.path.isfile(self.destination)
        self.dst_is_link_after = os.path.islink(self.destination)
        self.dst_is_dir_after = os.path.isdir(self.destination)

    def relocate(self, args):
        """
        Actually relocate the folder by linking the correct spot to the original folder.
        @param args: The parsed arguments from the command-line.
        """
        if args.dry:
            print(str(self.source) + " -> " + str(self.destination))
            return

        if not self.src_exists or self.src_is_file:
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
            if args.color:
                result = ""
                for b in bool_list:
                    result += " " + text_util.status_block(b)
                return result[1:]
            else:
                return ""
        blocks = list()
        blocks.append(self.dst_exists_after)
        blocks.append(
            self.src_is_dir == self.dst_is_dir_after and self.src_is_file == self.dst_is_file_after)

        if args.copy:
            blocks.append(not self.dst_is_link_after)
        else:
            blocks.append(self.dst_is_link_after)

        print(get_blocks(blocks) + " " + self.source + " -> " + self.destination)
