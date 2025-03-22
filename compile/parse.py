from __future__ import annotations

from dataclasses import dataclass
from itertools import product, filterfalse, groupby, tee 
from operator import attrgetter
from os import environ
from sys import exception, stderr
from typing import Optional


type SentencePairing = tuple[str, ...]

SOURCE_IS_MODERN = {
    '1': False,
    '2': True,
    '3': True,
}


@dataclass
class Sentence:
    '''Record struct for a sentence in the corpus'''
    id: int
    source: int
    modern: bool
    contents: str

    @staticmethod
    def from_str(string: str) -> Sentence:
        '''Convert a record in the corpus to a Sentence object'''
        items = string.split(':')

        try:
            assert len(items) >= 3
        except AssertionError:
            raise ValueError(f'Mal-formed entry {string}')

        id, source, *contents = items
        contents = ':'.join(contents)
        modern = SOURCE_IS_MODERN[source]

        try:
            id = int(id)
            source = int(source)
        except ValueError:
            raise ValueError('Mal-formed identifier, could not convert'
                             f' to int: {string}')

        return Sentence(id, source, modern, contents)


def parse_data() -> Optional[list[SentencePairing]]:
    '''
    Gets all the data from the corpus, and creates all necessary
    combinations of old and modern sentences

    Returns
    -------
        A list of 2-tuples of strings, or None
    '''

    try:
        with open('./corpus.dat', 'r', encoding='utf8') as f:
            # Only keep non-empty lines that aren't comments
            corpus = [l for line in f if (l := line.strip())
                      and not l.startswith('#')]

        records = map(Sentence.from_str, corpus)

    except FileNotFoundError:
        print('Corpus not found. Ensure that you are running this'
              ' from the root directory of the project',
              file=stderr)
        return

    except ValueError as e:
        print(f'Error parsing corpus:\n{e}',
              file=stderr)
        return

    output: list[tuple[str, ...]] = []

    get_id = attrgetter('id')
    get_contents = attrgetter('contents')
    is_modern = attrgetter('modern')

    records = sorted(records, key=get_id)

    comb_iter = groupby(records, key=get_id)

    if not 'NO_TQDM' in environ:
        try:
            from tqdm import tqdm
            comb_iter = tqdm(comb_iter)
        except ModuleNotFoundError:
            print('Unable to load tqdm. Proceeding without.',
                  file=stderr)

    for _, group in comb_iter:
        old, new = tee(group)
        old = filterfalse(is_modern, old)
        new = filter(is_modern, new)

        old, new = map(get_contents, old), map(get_contents, new)

        output.extend(product(old, new))

    return output
