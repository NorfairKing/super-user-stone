import abc

class Deployment(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deploy(self):
        """
        Deploy this deployment.
        """