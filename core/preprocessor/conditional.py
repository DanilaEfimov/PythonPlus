from typing import List, Callable
from core.preprocessor.handlers import register_handler, directive_prefix


def is_conditional(line: str) -> bool:
    return any(line.strip().startswith(f"{directive}") for directive in conditional_handlers)

def define(lines: List[str], line_index: int) -> int:
    pass

def undef(lines: List[str], line_index: int) -> int:
    pass

def ifpp(lines: List[str], line_index: int) -> int:
    pass


conditional_handlers ={
    "define" : define,
    "undef" : undef,
    "if" : ifpp
}

for name, handler in conditional_handlers.items():
    register_handler(name, handler)