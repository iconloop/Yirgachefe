"""Test Config"""
import os
from pathlib import Path

import pytest

from yirgachefe import config as config_
from yirgachefe import logger
from yirgachefe.config_ import Config

logger.update_logger(stream_out=True, coloredlog=True)
config = config_


@pytest.fixture
def config_path() -> Path:
    root_path = Path(os.path.join(os.path.dirname(__file__), '.'))
    file_path: Path = root_path.joinpath('temp-configure.json')
    return file_path


@pytest.fixture(autouse=True)
def patch_config_with_params(config_path):
    from yirgachefe.config_ import Config
    global config

    file_path: Path = config_path
    if file_path.exists():
        file_path.unlink()

    config = Config(config_path=str(file_path), create=True, logger=logger)
    yield
    if file_path.exists():
        file_path.unlink()


class TestConfig:
    def test_get_config(self):
        assert config['debug'] is not None

    def test_load_config(self, config_path):
        config.load_config(str(config_path))

    def test_load_env(self):
        os.environ['DEBUG'] = 'True'
        config._load_config_env()
        assert config['debug'] is True

        os.environ['debug'] = 'False'
        config._load_config_env()
        assert config['debug'] is False

    def test_set_config_in_code(self):
        with pytest.raises(KeyError):
            print(config['NEW'])
        config['NEW'] = 'new value'
        assert config['NEW'] == 'new value'
        ori_debug_mode = config['debug']
        config['debug'] = not ori_debug_mode
        assert config['debug'] != ori_debug_mode

    def test_use_config_as_attributes(self):
        with pytest.raises(KeyError):
            print(config.NEW)
        config.NEW = 'new value'
        assert config['NEW'] == 'new value'
        ori_debug_mode = config.debug
        config.debug = not ori_debug_mode
        assert config.debug != ori_debug_mode

    def test_write_config(self, config_path):
        config.NEW = 'new2 value2'
        config._write_config(config._config, str(config_path))
        config2 = Config(config_path=str(config_path))
        assert config.NEW == config2['NEW']
