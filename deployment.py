import abc

class Deployment(object):
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