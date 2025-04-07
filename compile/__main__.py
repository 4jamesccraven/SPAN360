from __future__ import annotations
from .cli import cli
from .parse import parse_data
from .encoders import ENCODERS

from sys import stderr


def main() -> None:
    args = cli()

    sentence_pairings = parse_data()
    encoder = ENCODERS[args.output_type]

    if sentence_pairings is not None:
        print(encoder(sentence_pairings))
    else:
        print('Unable to load sentences', file=stderr)


if __name__ == '__main__':
    main()
