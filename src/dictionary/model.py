from typing import List


class DictionaryEntry:
  def __init__(self, traditional: str, simplified: str, pinyin: str, definitions: List[str]):
    self.traditional = traditional
    self.simplified = simplified
    self.pinyin = pinyin
    self.definitions = definitions


class Dictionary:
  def __init__(self, entries: List[DictionaryEntry]):
    self.entries = entries

  def length(self):
    return len(self.entries)
