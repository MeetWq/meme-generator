# https://github.com/nonebot/nonebot2/blob/master/nonebot/log.py
import logging
import sys
from typing import TYPE_CHECKING

import loguru

if TYPE_CHECKING:
    from loguru import Logger, Record

logger: "Logger" = loguru.logger


class LoguruHandler(logging.Handler):
    """logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# https://github.com/nonebot/nonebot2/blob/master/nonebot/drivers/fastapi.py#L182
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "meme_generator.log.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
        },
    },
}


def setup_logger():
    from .config import config_file_path, meme_config

    def default_filter(record: "Record"):
        """默认的日志过滤器，根据 `log_level` 配置改变日志等级。"""
        log_level = meme_config.log.log_level
        levelno = (
            logger.level(log_level).no if isinstance(log_level, str) else log_level
        )
        return record["level"].no >= levelno

    default_format: str = (
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "<c><u>{name}</u></c> | "
        # "<c>{function}:{line}</c>| "
        "{message}"
    )

    logger.remove()
    logger.add(
        sys.stdout,
        level=0,
        diagnose=False,
        filter=default_filter,
        format=default_format,
    )

    logger.opt(colors=True).info(
        f"Config file path: <y><d>{config_file_path.resolve()}</d></y>"
    )
    logger.opt(colors=True).debug(
        f"Loaded config: <y><d>{str(meme_config.dict())}</d></y>"
    )
