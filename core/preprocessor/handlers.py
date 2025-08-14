from typing import List

def include(lines: List[str], line_index: int) -> int:
    pass

def invisible(lines: List[str], line_index: int) -> int:
    pass

def mirror(lines: List[str], line_index: int) -> int:
    pass

def repeat(lines: List[str], line_index: int) -> int:
    pass

def random(lines: List[str], line_index: int) -> int:
    pass

def debug(lines: List[str], line_index: int) -> int:
    pass

def info(lines: List[str], line_index: int) -> int:
    pass

def warning(lines: List[str], line_index: int) -> int:
    pass

def error(lines: List[str], line_index: int) -> int:
    pass


directive_prefix = "@"

handlers = {
    f"{directive_prefix}include": include,
    f"{directive_prefix}invisible": invisible,
    f"{directive_prefix}mirror": mirror,
    f"{directive_prefix}repeat": repeat,
    f"{directive_prefix}random": random,
    f"{directive_prefix}debug": debug,
    f"{directive_prefix}info": info,
    f"{directive_prefix}warning": warning,
    f"{directive_prefix}error": error,
}
