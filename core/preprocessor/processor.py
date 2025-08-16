import argparse
import sys
import os


from utils import replace_extension

core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
sys.path.insert(0, core_path)

from cli.cfgparse import parse_args
from context import Context
from handlers import is_directive, get_handler
from errors import PreprocessorError, SourceIndexError


def process(args: argparse.Namespace) -> Context:
    input_file: str = args.input
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.readlines()

    context = Context(args, [], input_file)
    pointer = 0

    try:
        while pointer < len(source):
            if is_directive(source[pointer]):
                handler = get_handler(source[pointer])
                if args.verbose:
                    print(f"Processing directive at line {pointer + 1}: {source[pointer].strip()}")
                pointer = handler(source, pointer, context)
                if pointer < 0 or pointer > len(source):
                    raise SourceIndexError(f"invalid index returned: {pointer}", handler)
            else:
                pointer += 1

        from macro_processor import expand_macros
        expand_macros(source, context.macro_table)

    except PreprocessorError as e:
        e.line_num = pointer
        print(e.what(source), file=sys.stderr)
        exit(1)

    if args.E:  # preprocess only mode enabled
        target = input_file if args.output is None else args.output
        filename = replace_extension(target, '.i')
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(source)
        if args.verbose:
            print(f"target file is {filename}")

    return context


if __name__ == "__main__":
    try:
        sys.argv = ['processor.py', '-i', 'example.txt', '--verbose', '-E', '-o', 'output']
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
