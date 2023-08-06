import re


def check_value_type(value, expected_type):
    if expected_type is not None:
        if type(expected_type) is not list:
            expected_type = [expected_type]
        if value is None or type(value) not in expected_type:
            return False
        else:
            return True
    else:
        return True


def find_word_in_text(text, word_to_find):
    words = words_in_text(text)
    return [i for i, e in enumerate(words) if e == word_to_find]


def words_in_text(text):
    pattern = re.compile(r'\S+')
    return pattern.findall(text)

