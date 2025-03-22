from .parse import SentencePairing

from itertools import starmap
from json import dumps
from typing import Callable


ENCODERS = dict()
def register_encoder(f: Callable) -> Callable:
    ENCODERS[f.__name__] = f
    return f


@register_encoder
def json(sentences: list[SentencePairing]) -> str:
    def pairing_to_dict(pair: SentencePairing) -> dict[str, str]:
        old, modern, *_ = pair
        return {'old': old, 'modern': modern}

    dump: list[dict[str, str]] = list(map(pairing_to_dict, sentences))

    return dumps(dump)


@register_encoder
def tab_separated(sentences: list[SentencePairing]) -> str:
    return '\n'.join(list(starmap(lambda l, r: f'{l}\t{r}', sentences)))


@register_encoder
def csv(sentences: list[SentencePairing]) -> str:
    return '\n'.join(['old,modern'] + list(starmap(lambda l, r: f'{l},{r}', sentences)))
