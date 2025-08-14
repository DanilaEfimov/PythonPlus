import cli.cfgparse
import compiler


def main():
    cli.cfgparse.init_parser()
    args = cli.cfgparse.parse_args()

    compiler.compile(args)


if __name__ == "__main__":
    main()
