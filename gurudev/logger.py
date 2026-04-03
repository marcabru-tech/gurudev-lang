"""Sistema de logging estruturado para GuruDev."""
import logging
import sys
from enum import IntEnum
from typing import Optional

class LogLevel(IntEnum):
    """Níveis de log do GuruDev."""
    SILENT = 60
    ERROR = 50
    WARNING = 40
    INFO = 30
    DEBUG = 20
    TRACE = 10
    ALL = 0

class GuruLogger:
    """Logger estruturado para o ecossistema GuruDev."""
    _instance: Optional['GuruLogger'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name: str = "gurudev", level: LogLevel = LogLevel.INFO):
        if self._initialized:
            return
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Handler para console com cores
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self._initialized = True

    def debug(self, msg: str, **kwargs):
        self._log(logging.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs):
        self._log(logging.INFO, msg, **kwargs)

    def warning(self, msg: str, **kwargs):
        self._log(logging.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs):
        self._log(logging.ERROR, msg, **kwargs)

    def trace(self, msg: str, **kwargs):
        self._log(logging.DEBUG, f"[TRACE] {msg}", **kwargs)

    def _log(self, level: int, msg: str, **kwargs):
        if kwargs:
            msg = f"{msg} | {kwargs}"
        self.logger.log(level, msg)

def get_logger(name: str = "gurudev") -> GuruLogger:
    """Retorna instância singleton do logger."""
    return GuruLogger(name)
