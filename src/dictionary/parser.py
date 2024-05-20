import re
from typing import List

from .model import Dictionary, DictionaryEntry


def __read_file(file_name: str) -> str:
    """Opens and reads the text within the provided file"""
    f = open(file_name, 'r', encoding='utf-8')
    return f.read()


def __remove_copyright(text: str) -> str:
    """Removes the chunk of copyright text present at the top of the dict file"""
    pattern = re.compile(r'^#.*\n', re.MULTILINE)
    return pattern.sub('', text)


def __parse_line(line: str) -> DictionaryEntry:
    traditional, simplified, pinyin, definitions = re.match(
        r'(.*) (.*) (\[.*\]) \/(.*)\/', line).groups()  # type: ignore

    definitions = definitions.split('/')

    entry = DictionaryEntry(traditional, simplified, pinyin, definitions)

    return entry


def parse(file_name: str) -> Dictionary:
    """Parses the given dictionary file into an application friendly format"""
    print('Parsing Mandarin dictionary data...')
    raw_text = __read_file(file_name)
    raw_text = __remove_copyright(raw_text)

    lines = raw_text.splitlines()

    entries: List[DictionaryEntry] = []
    for line in lines:
        entries.append(__parse_line(line))

    dictionary = Dictionary(entries)

    print('Dictionary parsed with {} entries'.format(dictionary.length()))

    return dictionary
