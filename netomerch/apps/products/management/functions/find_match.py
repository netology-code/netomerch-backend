import difflib


def find_match(sample, search_set):
    similarity = 0.5
    result = False
    for item in search_set:
        matcher = difflib.SequenceMatcher(a=sample.lower(), b=item[0].lower())
        ratio = matcher.ratio()
        if ratio > similarity:
            similarity = ratio
            result = item
    return result
