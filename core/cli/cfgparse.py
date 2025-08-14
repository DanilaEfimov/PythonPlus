import argparse

parser = argparse.ArgumentParser(
    description="meta Python compiler for extending language syntax and possibilities"
)

def init_parser() -> None:
    parser.add_argument(
        '-i', '--input',
        help="path to source code Python+ file",
        required=True,
        type=str
    )

    parser.add_argument(
        '-o', '--output',
        help="name of compiled file",
        default='out.py',
        type=str
    )

    parser.add_argument(
        '--stdout',
        help="enable step's output",
        action='store_true'
    )

    parser.add_argument(
        '--check-only',
        help="only checks source code",
        action='store_true'
    )

    parser.add_argument(
        '--enable',
        help="enables given extensions",
        type=str
    )

    parser.add_argument(
        '--disable',
        help="disables given extensions",
        type=str
    )

    parser.add_argument(
        '--verbose',
        help="enable all output mode",
        action='store_true'
    )

    parser.add_argument(
        '--version',
        help="prints compiler version details",
        version="Python+ 1.0",
        action='version'
    )

def parse_args() -> argparse.Namespace:

    args = parser.parse_args()

    args.enable = [e.strip() for e in args.enable.split(',')] if args.enable else []
    args.disable = [e.strip() for e in args.disable.split(',')] if args.disable else []

    return args

if __name__ == "__main__":
    init_parser()
    args = parse_args()
    print(args)