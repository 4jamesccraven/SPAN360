from .encoders import ENCODERS

from argparse import ArgumentParser, Namespace


def cli() -> Namespace:
    parser = ArgumentParser(
        'compile', description='Compile the corpus into a machine-readable format'
    )

    parser.add_argument(
        'output_type', help='The desired output format', choices=ENCODERS.keys()
    )

    return parser.parse_args()
