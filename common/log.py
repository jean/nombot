"""Log Util"""

from utils.factory import Creator
from utils.singleton import Singleton
from utils.logger import Logger as L
from common.config import Conf


class Logger(metaclass=Singleton):
    """Shared loggers singleton"""
    def __init__(self):
        self.conf = Conf()
        self.loggers = {}

    def get(self, name):
        """Creates a logger if one doesn't exist"""
        try:
            return self.loggers[name]
        except KeyError:
            return self.create(name)

    def create(self, name):
        """Creates a logger if one doesn't exist"""
        self.loggers[name] = Log(name)
        return self.loggers[name]


class Log(L):
    """
    Facade for the logging facility.  See utils/logger.py for more information.
    """
    def __init__(self, name):
        self.name = name
        self.conf = Conf().get_logger(name)
        self.level = self.conf["level"]

        self.basicConfig(self.level)
        self.debug(f"Logging started for {self.name}")

    def exc(self, message):
        """
        Log an error-level message. If exc_info is True, if an exception
        was caught, show the exception information (message and stack trace).
        """
        self.critical(message, exc_info=True)
        raise Exception(message)


class LoggerMixin:
    """Mixin to be used to simplify the logging interface"""
    def create_logger(self):
        """Generates a logger instance from the singleton"""
        self.log = Logger().get(self.name)
