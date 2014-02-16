"""
SUS installation
"""

import util
from deployment import Deployment


class Installation(Deployment):
    def __init__(self, command, arguments, sudo):
        self.command = command
        self.arguments = arguments
        self.sudo = sudo

    def deploy(self):
        """
        Install the given programs
        """
        full_command = self.command + " " + self.arguments
        util.call(full_command, sudo=self.sudo)

    def evaluate(self):
        """
        Evaluate the deployment
        """
