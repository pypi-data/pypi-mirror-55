from __future__ import annotations
import argparse
import json
import yaml
import logging
import logging.config
import pathlib

from . import logger


class _Executable():
    OBJECT_LIST = {}

    def __init__(self, name: str):
        self.parser = argparse.ArgumentParser()

        # Logging args

        sub_parser = self.parser.add_subparsers()

        # Parameter configuration

        param_parser = sub_parser.add_parser(
            'param', help="configure with commandline paramters")
        param_parser.add_argument('-v', '--verbosity', action='count',
                                  help="change debug level")

        output_parser = param_parser.add_mutually_exclusive_group()
        output_parser.add_argument('-f', '--file', help="log to file location")
        output_parser.add_argument(
            '-c', '--console', action="store_true", help="Log to console")

        # File configuration

        file_parser = sub_parser.add_parser(
            'file', help="configure with a .ini file")
        file_parser.add_argument('-f', '--file', help="file location")

        # Defaults
        self._file_path = None
        self.logger = logging.getLogger(name)

    def __enter__(self):
        # Set logging output

        # Param configuration
        if hasattr(self.args, "verbosity"):
            logger.set_logger(self.args.verbosity)

            if self.args.file is not None:
                self._file_path = logger.set_file_handler(self.args.file)
            elif self.args.console:
                logger.set_console_handler()

            # TEMP FIX
            else:
                self.logger.disabled = True
        
        # File configuration
        else:
            config_path = pathlib.Path(self.args.file)
            if not config_path.exists() or not config_path.is_file():
                raise ValueError
            
            config_dict = None

            # Only ini, json, and yml are valid config file types
            if config_path.suffix == "ini":
                logging.config.fileConfig(config_path)

            elif config_path.suffix == "json":
                config_dict = json.load(config_path)

            elif config_path.suffix == "yml":
                with config_path.open('r') as stream:
                    config_dict = yaml.safe_load(stream)
            else:
                raise ValueError
            
            if config_dict != None:
                logging.config.dictConfig(config_dict)

        return self

    def __exit__(self, err_type, err_value, traceback)->bool:
        pass

    @property
    def args(self)->argparse.Namespace:
        """args of self.parser"""
        return self.parser.parse_args()


def getExecutable(name: str)->_Executable:
    """ factory function to recieve a executable object"""

    for v in _Executable.OBJECT_LIST:
        if name == v:
            return _Executable.OBJECT_LIST[v]
    obj = _Executable(name)
    _Executable.OBJECT_LIST = obj
    return obj