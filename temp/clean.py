from itertools import chain
from os import listdir

from bs4 import BeautifulSoup
from tqdm import tqdm


def main() -> None:
    files = [f for f in listdir() if f.endswith('.html')]

    text = []

    for file in tqdm(files):
        with open(file, 'r', encoding='utf8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        text.append(soup.text.splitlines())

    text = list(chain.from_iterable(text))
    text = [line.strip() for line in text if line]
    text = '\n'.join(text)

    print(text)

if __name__ == '__main__':
    main()
