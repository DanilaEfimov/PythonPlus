import re
import sys
import os

import handlers
from errors import *


def include(lines: List[str], line_index: int) -> int:
    to_include = read_arg(lines[line_index])
    path_chain = []

    if not is_valid_filename(to_include):
        raise DirectiveSyntaxError(f"Include::Invalid filename: '{to_include}'", line_index)
    if not file_exists(to_include):
        raise UnexpectedFileError("checkout given filenames", to_include, line_index)

    try:
        includes = collect_includes(to_include, path_chain)
        lines[line_index:line_index+1] = includes
        return line_index
    except PreprocessorError as e:
        e.line_num = line_index
        print(e.what(lines), sys.stderr)
        exit(1)


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


def collect_includes(to_include: str, path_chain: list[str]) -> list[str]:
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
                raise DirectiveSyntaxError("include::invalid path syntax")

            included_lines = collect_includes(path, path_chain)
            lines[i:i+1] = included_lines
            i += len(included_lines)
        else:
            i += 1

    path_chain.pop()
    return lines


handlers.register_handler("include", include)