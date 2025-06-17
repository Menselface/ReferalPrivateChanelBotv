import sys
from loguru import logger

from config import config

logger.remove()
logger.add(
    sink=sys.stdout,
    format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
    " | <level>{level: <8}</level>"
    " | <cyan>{module}:{line}</cyan>"
    " | <white><b>{message}</b></white>",
    level=config.logger.logger,
)
logger = logger.opt(colors=True)