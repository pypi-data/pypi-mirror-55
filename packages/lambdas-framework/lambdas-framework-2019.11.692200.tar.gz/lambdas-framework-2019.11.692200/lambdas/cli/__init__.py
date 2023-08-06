# Standard imports
import argparse

# Local imports
from lambdas.cli import node


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest='subparser_name')

    node.put_subparser(subparsers)

    args = parser.parse_args()

    if args.subparser_name:
        args.subparser_handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    cli()
