import argparse
import sys

from handlers import is_directive, get_handler
from errors import *


def process(args: argparse.Namespace) -> int:
    input_file: str = args.input
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.readlines()

    pointer = 0
    try:
        while pointer < len(source):
            if is_directive(source[pointer]):
                handler = get_handler(source[pointer])
                if args.verbose:
                    print(f"Processing directive at line {pointer + 1}: {source[pointer].strip()}")
                pointer = handler(source, pointer)
                if pointer < 0 or pointer > len(source):
                    raise SourceIndexError(f"invalid index returned: {pointer}", handler)
            else:
                pointer += 1
    except PreprocessorError as e:
        e.line_num = pointer
        print(e.what(source), sys.stderr)
        exit(1)

    return 0


if __name__ == "__main__":
    try:
        from ..cli.cfgparse import parse_args
        args = parse_args()
        process(args)
    except PreprocessorError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)
    except IOError as e:
        print(f"I/O Error: {e}", file=sys.stderr)
        exit(3)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        exit(2)

    exit(0)