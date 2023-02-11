import loguru
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger

logger: "Logger" = loguru.logger
