import configparser
import importlib.resources as pkg_resources
from typing import Any


class __MetaConfigParser(type):
    def __init__(self, *args: Any, **kwds: Any):
        self.config_parser = configparser.ConfigParser()
        with pkg_resources.path(__package__, "config.ini") as path:
            self.config_parser.read(path)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.config_parser


class ConfigParser(metaclass=__MetaConfigParser):
    """Use this class to get config data from config.ini

    For example:
        ConfigParser()["appData"]["TOKEN"]  # get token from config.ini
    """
    pass
