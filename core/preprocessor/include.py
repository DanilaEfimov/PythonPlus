import re
import sys
import os
from typing import List

import handlers
from context import Context
from errors import (
    DirectiveSyntaxError,
    UnexpectedFileError,
    SelfReferenceError,
    PreprocessorError
)


def include(lines: List[str],
            line_index: int,
            context: Context) -> int:
    to_include = read_arg(lines[line_index])
    path_chain = []

    if not is_valid_filename(to_include):
        raise DirectiveSyntaxError(f"Include::Invalid filename: '{to_include}'", context.base_line)
    if not file_exists(to_include):
        raise UnexpectedFileError("checkout given filenames", to_include, context.base_line)

    try:
        includes = collect_includes(to_include, path_chain, context)
        lines[line_index:line_index+1] = includes
        return line_index
    except PreprocessorError as e:
        e.line_num = context.base_line
        print(e.what(lines), sys.stderr)
        return -1


def read_arg(line: str) -> str:
    match = re.search(r'include\s+(?:"([^"]+)"|\'([^\']+)\'|(\S+))', line)
    if match:
        return match.group(1) or match.group(2) or match.group(3)
    return ''


def is_include(line: str) -> bool:
    return handlers.is_directive(line, "include")


def is_valid_filename(filename: str) -> bool:
    if not len(filename):
        return False

    forbidden = r'[<>:"/\\|?*]' # Windows
    if re.search(forbidden, filename):
        return False

    return True


def file_exists(filename: str) -> bool:
    return os.path.isfile(filename)


def collect_includes(to_include: str,
                     path_chain: list[str],
                     context: Context) -> list[str]:
    if to_include in path_chain:
        raise SelfReferenceError(f"Cyclic include detected. Path chain: {path_chain}", to_include)

    with open(to_include, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    path_chain.append(to_include)

    i = 0
    while i < len(lines):
        if is_include(lines[i]):
            path = read_arg(lines[i])
            if path == '':
                raise UnexpectedFileError("include::invalid path syntax", to_include)

            included_lines = collect_includes(path, path_chain, context)
            lines[i:i+1] = included_lines
            i += len(included_lines)
        else:
            i += 1

    path_chain.pop()
    return lines


handlers.register_handler("include", include)