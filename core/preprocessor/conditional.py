from typing import List, Callable

from core.preprocessor.utils import search_end
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
    from macro_processor import Macros, MacrosParam

    if lines[line_index].split()[1].startswith('__'):
        macros = MacrosParam(lines, line_index)
        context.macro_table.table.append(macros)
    else:
        macros = Macros(lines, line_index)
        context.macro_table.table.append(macros)

    end_index = search_end(lines, line_index)
    lines[line_index:end_index+1] = []
    return line_index

def undef(lines: List[str], line_index: int, context: Context) -> int:
    pass

def ifpp(lines: List[str], line_index: int) -> int:
    pass


conditional_handlers ={
    "define" : define,
    "undef" : undef,
    "if" : ifpp,
    "end": end
}

for name, handler in conditional_handlers.items():
    register_handler(name, handler)