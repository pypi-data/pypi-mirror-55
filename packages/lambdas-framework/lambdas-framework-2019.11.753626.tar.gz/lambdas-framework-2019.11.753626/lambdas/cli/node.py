# Local imports
from lambdas.constants import (
    COMPUTING_NODE_DEFAULT_HOST,
    COMPUTING_NODE_DEFAULT_PORT,
    AVAILABLE_CPUS,
)
from lambdas.entities import (
    ComputingNode,
)


def put_subparser(subparsers):
    parser = subparsers.add_parser(
        'node',
        help='Serve a Computing Node in this machine',
    )
    parser.add_argument(
        '--host',
        help='host',
        required=False,
        default=COMPUTING_NODE_DEFAULT_HOST,
    )
    parser.add_argument(
        '--port',
        help='port',
        type=int,
        required=False,
        default=COMPUTING_NODE_DEFAULT_PORT,
    )
    parser.add_argument(
        '--processes',
        help='processes',
        type=int,
        required=False,
        default=AVAILABLE_CPUS,
    )
    parser.set_defaults(subparser_handler=handler)


def handler(args):
    ComputingNode(
        host=args.host,
        port=args.port,
        processes=args.processes,
    )
