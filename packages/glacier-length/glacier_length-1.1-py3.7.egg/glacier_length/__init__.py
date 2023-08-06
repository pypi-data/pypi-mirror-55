import logging

from ._src import get_all_length


__version__ = "1.1"

logger = logging.getLogger(__name__)  # 创建一个logger
logger.addHandler(logging.NullHandler())  # 给logger添加handler