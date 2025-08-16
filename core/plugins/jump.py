"""
Example of using Python+ preprocessor API
"""
from typing import List

from context import Context
from handlers import register_handler


def jump(lines: List[str], line_index, context: Context) -> int:
    pass


register_handler("jump", jump)