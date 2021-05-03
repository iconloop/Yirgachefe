"""Config"""
import json
import logging
import os
from pathlib import Path

from yirgachefe.logger_ import Logger


class Config:
    CONFIG_DEFAULT_FILE = 'configure.json'

    def __init__(self, config_path: str = '', create: bool = False, logger=None):
        super().__init__()
        _config_path = config_path or str(self.get_path(self.CONFIG_DEFAULT_FILE))
        self._config = {}
        self._logger: Logger = logger or logging.getLogger(__name__)
        self._log_options = None
        self._load_config_file(_config_path, check_exist=False)
        self._set_common_default()

        if create:
            self._write_config(self._config, _config_path)

        if 'config_path' in self._config:
            self._load_config_file(str(self._config['config_path']), check_exist=False)

        self._load_config_env()
        self._update_log_options()

    def load_config(self, config_path: str):
        """Load User configuration file.

        However, os 'env' variables always have higher priority than config files.
        If the 'env' variable is set, the value of the config file is not applied.

        :param config_path: The str path created with pathlib.Path is recommended.
        """
        self._load_config_file(config_path=config_path)
        self._load_config_env()
        self._update_log_options()

    def __setattr__(self, key, value):
        if key in ['_config', '_logger', '_log_options']:
            self.__dict__[key] = value
        else:
            self._config[key] = value

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__getattribute__(name)
        return self[name]

    def __setitem__(self, key, item):
        self._config[key] = item
        self._update_log_options()

    def __getitem__(self, key):
        return self._config[key]

    def _set_common_default(self):
        if 'debug' not in self._config:
            self._logger.debug("config['debug'] is not configured. So default(False) is used.")
            self._config['debug'] = False
        if 'log_level' not in self._config:
            self._logger.debug("config['log_level'] is not configured. So default(logging.WARNING) is used.")
            self._config['log_level'] = logging.getLevelName(logging.WARNING)
        if 'log_format' not in self._config:
            self._logger.debug("config['log_format'] is not in configured. So default is used.")
            self._config['log_format'] = \
                "%(asctime)s,%(msecs)03d %(process)d %(thread)d %(levelname)s %(filename)s(%(lineno)d) %(message)s"
        if 'encoding' not in self._config:
            self._config['encoding'] = "utf-8"

    def _load_config_file(self, config_path: str, check_exist=True):
        if not check_exist and not Path(config_path).is_file():
            return

        with open(config_path, 'r') as config_file:
            self._config.update(json.load(config_file))

    def _load_config_env(self):
        for config_name in self._config:
            env_value = os.getenv(config_name) or os.getenv(str.upper(config_name))
            if env_value is not None:
                if isinstance(self[config_name], (bool, int, float)):
                    env_value = eval(env_value)
                self[config_name] = env_value

    def _update_log_options(self):
        """Update log_options and logger."""
        prev_log_options = self._log_options
        self._log_options = ''.join(
            [str(self._config.get(key)) for key in ['debug', 'log_level', 'log_path', 'log_format']]
        )

        if prev_log_options != self._log_options and isinstance(self._logger, Logger):
            self._logger.update_logger(
                log_level=logging.getLevelName(self._config.get('log_level')),
                log_format=self._config.get('log_format'),
                log_path=self._config.get('log_path'),
                stream_out=self._config.get('debug'),
                coloredlog=self._config.get('debug'))

    def _write_config(self, config: dict, config_path: str):
        with open(config_path, 'w', encoding=self._config['encoding']) as config_file:
            json.dump(config, config_file, indent=4, sort_keys=True)

    @staticmethod
    def get_path(path: str) -> Path:
        """Get Path from current working directory.

        :param path: file_name or path
        :return:
        """
        root_path = Path(os.path.join(os.getcwd()))
        return root_path.joinpath(path)
