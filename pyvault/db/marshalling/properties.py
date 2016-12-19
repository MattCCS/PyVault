
import abc


class Saveable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def save(self):
        pass


class Loadable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractstaticmethod
    def load():
        pass
