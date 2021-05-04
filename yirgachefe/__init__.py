from pathlib import Path

import sys

from .config_ import Config
from .logger_ import Logger

__all__ = ['Config', 'Logger', 'config', 'logger']


def _get_main_module_name():
    return str(Path(sys.modules['__main__'].__file__).stem)


logger = Logger(name=_get_main_module_name())
config = Config(logger=logger)
