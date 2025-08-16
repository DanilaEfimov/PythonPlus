from typing import List, Callable

from context import Context
from errors import DirectiveSyntaxError
from utils import search_end


def setvar(lines: List[str], line_index: int, context: Context) -> int:
    pass


def invisible(lines: List[str], line_index: int, context: Context) -> int:
    # @invisible ~ @repeat 0
    lines[line_index] = f"{directive_prefix}repeat {0}"
    return repeat(lines, line_index, context)


def mirror(lines: List[str], line_index: int, context: Context) -> int:
    pass

def repeat(lines: List[str], line_index: int, context: Context) -> int:
    end_index = search_end(lines, line_index)
    if end_index == -1:
        raise DirectiveSyntaxError("utils.search_end::Missed 'end' directive", context.base_line)
    lines[line_index:end_index+1] = lines[line_index+1:end_index] * 5
    return line_index + 5 * (end_index-line_index-1)

def random(lines: List[str], line_index: int, context: Context) -> int:
    pass

def debug(lines: List[str], line_index: int, context: Context) -> int:
    pass

def info(lines: List[str], line_index: int, context: Context) -> int:
    pass

def warning(lines: List[str], line_index: int, context: Context) -> int:
    pass

def error(lines: List[str], line_index: int, context: Context) -> int:
    pass


directive_prefix = "@"  # space-free prefix

handlers = {
    f"{directive_prefix}invisible"  : invisible,
    f"{directive_prefix}mirror"     : mirror,
    f"{directive_prefix}repeat"     : repeat,
    f"{directive_prefix}random"     : random,
    f"{directive_prefix}debug"      : debug,
    f"{directive_prefix}info"       : info,
    f"{directive_prefix}warning"    : warning,
    f"{directive_prefix}error"      : error
}


def register_handler(
        directive: str,
        handler: Callable[[list[str], int, Context], int],
        *,
        overwrite: bool=False
) -> None:

    if not directive.startswith(directive_prefix):
        directive = directive_prefix + directive

    if directive in handlers:
        print(f"Directive '{directive}' already registered")
        if overwrite:
            print(f"Directive '{directive}' overwritten.")
        else:
            print(f"Directive '{directive}' already registered. Skipping.")
            return

    handlers[directive] = handler


def unregister_handler(directive: str) -> None:

    if not directive.startswith(directive_prefix):
        directive = directive_prefix + directive

    if directive not in handlers:
        raise ValueError(f"Directive '{directive}' isn't registered")

    handlers.pop(directive)


def is_directive(line: str, directive: str | None = None) -> bool:
    stripped = line.strip()
    if directive is not None:
        if not directive.startswith(directive_prefix):
            directive = directive_prefix + directive
        return stripped.startswith(directive)
    else:
        return any(stripped.startswith(handler) for handler in handlers)


def get_handler(line: str) -> Callable[[List[str], int, Context], int]:
    name = line.split()[0].strip()
    if name not in handlers:
        raise ValueError(f"No handler registered as '{name}'")
    return handlers[name]


""" vvv All handlers must be registered here vvv """
import include
import conditional
import core.plugins.register    # preprocessor API plugins