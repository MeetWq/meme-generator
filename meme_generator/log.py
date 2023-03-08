from typing import TYPE_CHECKING

import loguru

if TYPE_CHECKING:
    from loguru import Logger

logger: "Logger" = loguru.logger
