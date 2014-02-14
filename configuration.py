import os
import socket
from deployment import Deployment

DEFAULT_SHARED_FOLDER_NAME = "shared"


class Configuration(Deployment):
    def __init__(self, depot, config_file_name, destination_path):
        self.depot = depot
        self.config_file_name = config_file_name
        self.destination_path = destination_path

        self.shared_folder_path = os.path.join(depot, DEFAULT_SHARED_FOLDER_NAME)
        self.host_folder_path = os.path.join(depot, socket.gethostname())

        self.config_in_shared_folder = os.path.join(self.shared_folder_path,self.config_file_name)
        self.config_in_host_folder = os.path.join(self.shared_folder_path,self.host_folder_path)

        self.shared_config_exists = os.path.exists(self.config_in_shared_folder)
        self.host_config_exists = os.path.exists(self.config_in_shared_folder)

        self.source = None
        if self.shared_config_exists:
            self.source = self.config_in_shared_folder
        if self.host_config_exists:
            self.source = self.config_in_host_folder
        print(str(self.__dict__))

    def deploy(self):
        self.check_before()
        self.link()
        self.check_after()

    def check_before(self):
        pass

    def check_after(self):
        pass

    def link(self):