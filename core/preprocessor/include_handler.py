from os import abort
from typing import List
import re
import sys

from handlers import register_handler, is_directive
from errors import *


def include(lines: List[str], line_index: int) -> int:
    path_chain = []
    to_include = read_arg(lines[line_index])
    try:
        includes = collect_includes(to_include, path_chain)
        lines[line_index:line_index+1] = includes
        return line_index
    except PreprocessorError as e:
        e.line_num = line_index
        print(e.what(lines), sys.stderr)
        exit(1)


def read_arg(line: str) -> str:
    match = re.search(r'\"([^\"]+)\"|\'([^\']+)\'|(\S+)', line)
    if match:
        return match.group(1) or match.group(2) or match.group(3)
    return ''


def is_include(line: str) -> bool:
    return is_directive(line, "include")


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


register_handler("include", include)