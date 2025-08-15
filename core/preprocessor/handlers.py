from typing import List, Callable


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
        handler: Callable[[list[str], int], int],
        *,
        overwrite: bool=False
) -> None:
    global handlers

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
    global handlers

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


def get_handler(line: str) -> Callable[[List[str], int], int]:
    name = line.split()[0].strip()
    if name not in handlers:
        raise ValueError(f"No handler registered as '{name}'")
    return handlers[name]


""" vvv All handlers must be registered here vvv """
import include_handler
import plugins.register