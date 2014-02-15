"""
SUS deployment
"""

import abc


class Deployment(object):
    """
    A class of deployments, anything that needs to be deployed by SUS.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deploy(self):
        """
        Deploy this deployment.
        """

    @abc.abstractmethod
    def evaluate(self):
        """
        Evaluate the deployment
        """
