import re

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
    from macro_processor import Macros, ParamMacros

    line = lines[line_index]
    splited = [word.strip() for word in line.split()]
    if Macros.is_singleline_syntax(line):
        name = splited[1]
        body = ' '.join(splited[2:])
        context.macro_table.append(Macros(name, body))
        lines.pop(line_index)

    elif Macros.is_multyline_syntax(line):
        end_index = search_end(lines, line_index)
        name = splited[1]
        body = ''.join(lines[line_index + 1:end_index])
        context.macro_table.append(Macros(name, body))
        lines[line_index:end_index + 1] = []

    elif ParamMacros.is_singleline_syntax(line):
        name = ParamMacros.get_name(line)
        macros = ParamMacros(name)
        macros.params = macros.get_values(line)

        prefix_pattern = rf'{re.escape(directive_prefix)}define\s+{re.escape(name)}\s*\([^)]*\)'
        body = re.sub(prefix_pattern, '', line, count=1).strip()

        macros.set_body(body)
        context.macro_table.append(macros)
        lines.pop(line_index)

    elif ParamMacros.is_multyline_syntax(line):
        end_index = search_end(lines, line_index)
        name = ParamMacros.get_name(line)
        macros = ParamMacros(name)
        macros.params = macros.get_values(line)

        body = ''.join(lines[line_index+1:end_index])

        macros.set_body(body)
        context.macro_table.append(macros)
        lines[line_index:end_index + 1] = []

    else:
        raise DirectiveSyntaxError(f"Invalid '{directive_prefix}define' syntax", line_index)

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