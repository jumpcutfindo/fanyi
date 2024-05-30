import re


def remove_non_chinese_items(items: list[str]) -> list[str]:
    """Removes any items that do not contain Chinese from the results"""
    return list(filter(lambda x: re.match(r'[^A-Za-z\d\s]+', x), items))

def clean_words(items: list[str]) -> list[str]:
    """Removes items that are considered unclean, and removes symbols from words"""
    results = []
    for item in items:
        results.append(re.sub(r'[^\w\s]', '', item))

    results = list(filter(lambda x: re.match(r'\S', x), results))
    return results
