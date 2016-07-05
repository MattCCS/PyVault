"""
"""

# standard
import abc


class Saveable(object):
    """
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def save(self):
        pass
