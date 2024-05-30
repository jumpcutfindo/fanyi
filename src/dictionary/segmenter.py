import pkuseg

from typing import cast
from .utils import clean_words, remove_non_chinese_items


def segment_into_subphrases(phrases) -> dict[str, list[str]]:
    """
        Segments a list of phrases into smaller units.

        Uses `pkuseg` to help with the segmentation.
        """
    segmenter = pkuseg.pkuseg()
    phrases = remove_non_chinese_items(phrases)

    phrases_map = {}

    for phrase in phrases:
        subphrases = cast(list[str], segmenter.cut(phrase))
        subphrases = remove_non_chinese_items(subphrases)
        phrases_map[phrase] = clean_words(subphrases)

    return phrases_map
