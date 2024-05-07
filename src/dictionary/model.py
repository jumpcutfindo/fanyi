from typing import List


class DictionaryEntry:
  def __init__(self, traditional: str, simplified: str, pinyin: str, definitions: List[str]):
    self.traditional = traditional
    self.simplified = simplified
    self.pinyin = pinyin
    self.definitions = definitions


class Dictionary:
  def __init__(self, entries: List[DictionaryEntry]):
    self.__entries = entries
    self.__simplified_map = {x.simplified: x for x in entries}
    self.__traditional_map = {x.traditional: x for x in entries}

  def length(self):
    """Returns the number of entries present in the dictionary"""
    return len(self.__entries)

  def find_simplified(self, simplified: str):
    """Searches for a word by its Simplified Chinese representation"""
    if simplified in self.__simplified_map:
      return self.__simplified_map[simplified]
    return None

  def find_traditional(self, traditional: str):
    """Searches for a word by its Traditional Chinese representation"""
    if traditional in self.__traditional_map:
      return self.__traditional_map[traditional]
    return None
