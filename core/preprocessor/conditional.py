from typing import List, Callable

from errors import *
from handlers import register_handler, directive_prefix
from context import Context, State

def is_conditional(line: str) -> bool:
    return any(line.strip().startswith(f"{directive}") for directive in conditional_handlers)

def end(lines: List[str], line_index: int, context: Context) -> int:
    if context.state != State.WAITING_END_OF_BLOCK:
        raise DirectiveSyntaxError("Unexpected directive 'end'", context.base_line)
    return line_index   # nothing modified

def define(lines: List[str], line_index: int, context: Context) -> int:
    pass

def undef(lines: List[str], line_index: int, context: Context) -> int:
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