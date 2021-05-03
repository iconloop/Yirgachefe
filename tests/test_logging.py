"""Test Logger"""
import os
from pathlib import Path

import pytest

from yirgachefe import logger


@pytest.fixture
def log_file() -> Path:
    root_path = Path(os.path.join(os.path.dirname(__file__), '.'))
    file_path: Path = root_path.joinpath('temp-log-file.log')
    return file_path


@pytest.fixture(autouse=True)
def clear_test_log_file(log_file):
    file_path: Path = log_file
    if file_path.exists():
        file_path.unlink()
    yield
    if file_path.exists():
        file_path.unlink()


class TestLogger:
    def test_get_logger(self):
        logger.get_logger().warning('warning log')

    def test_autocomplete(self):
        logger.debug('debug log')

    def test_coloredlog(self):
        print()
        logger.update_logger(stream_out=True)
        logger.info('log')
        logger.critical('log')
        logger.error('log')
        logger.debug('log')
        logger.warning('log')
        logger.critical('log')

        logger.update_logger(stream_out=True, coloredlog=True)
        logger.info('color')
        logger.critical('color')
        logger.error('color')
        logger.debug('color')
        logger.warning('color')
        logger.critical('color')

    def test_log_file(self, log_file):
        print()
        logger.update_logger(log_path=str(log_file), stream_out=True)
        logger.debug('file')

        logger.update_logger(stream_out=True, coloredlog=True)
        logger.debug('color NO-FILE')

        logger.update_logger(log_path=str(log_file), stream_out=True, coloredlog=True)
        logger.debug('color file')

        with open(str(log_file), 'r') as _log_file:
            logs = _log_file.readlines()
            for log in logs:
                assert 'NO-FILE' not in log
