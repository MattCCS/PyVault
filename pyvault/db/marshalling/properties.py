
import abc


class Saveable(abc.ABC):

    @abc.abstractmethod
    def save(self):
        pass


class Loadable(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def load():
        pass


class Newable(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def new():
        pass
