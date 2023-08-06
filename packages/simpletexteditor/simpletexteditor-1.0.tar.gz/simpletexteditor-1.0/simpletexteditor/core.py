import re

split_to_words_with_signs_pattern = re.compile(r'\S+')


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
    words = split_to_words_with_signs_pattern.findall(text)
    return [i for i, e in enumerate(words) if e == word_to_find]


def words_in_text(text):
    return split_to_words_with_signs_pattern.findall(text)


class Cursor:
    def __init__(self, start_position=None, end_position=None, is_forward_direction=True, target_data=''):
        self.start_position = start_position
        self.end_position = end_position
        self.is_forward_direction = is_forward_direction
        self.validate_cursor()
        self.data = None
        self.data = self.get_data(target_data)

    def validate_cursor(self):
        if not check_value_type(self.start_position, [int, str]):
            raise ValueError('start_position value should be int or str object')

        if not check_value_type(self.end_position, [int, str]):
            raise ValueError('end_position value should be int or str object')

        if not check_value_type(self.is_forward_direction, bool):
            raise ValueError('is_forward_direction value should be bool object')

    def get_data(self, target_data=None):
        if self.data is None:
            words = words_in_text(target_data)         # Массив слов
            words_reverse = words           # Массив слов в обратном  порядке
            words_reverse.reverse()
            words_count = len(words)        # Количество слов
            words_range = range(len(words)) # Индексы слов

            if self.is_forward_direction:
                local_start = self.start_position
                local_end = self.end_position
            else:
                local_start = self.end_position
                local_end = self.start_position

            if check_value_type(local_start, int):
                if local_start not in words_range:
                    local_start = 0
                local_start = words[local_start]

            if check_value_type(local_end, int):
                if local_end not in words_range:
                    local_end = words_count - 1
                local_end = words[local_end]

            start_ix = target_data.find(local_start)
            if start_ix == -1:
                start_ix = 0
            end_ix = [i for i, e in enumerate(target_data) if e == local_end and i > start_ix + len(local_start)]
            if len(end_ix) == 0:
                end_ix = len(target_data)
            else:
                end_ix = end_ix[0]

            self.data = target_data[start_ix:end_ix]

        return self.data


class Text:
    def __init__(self, data=''):
        self.data = data
        self.cursors = {}

    def get_data(self):
        return self.data

    def add_cursor(self, name=None, start_position=None, end_position=None, is_forward_direction=True):
        if not check_value_type(name, str):
            raise ValueError('cursor name should be str object')
        self.cursors[str(name)] = Cursor(start_position, end_position, is_forward_direction, self.data)

    def print_cursor(self, cursor_name=None):
        if cursor_name is None:
            [self.print_cursor(i) for i in self.cursors.keys()]
        else:
            if not check_value_type(cursor_name, str):
                raise ValueError('cursor name should be str object')
            print(self.get_cursor_print_data(cursor_name))

    def get_cursor_print_data(self, cursor_name=None):
        if not check_value_type(cursor_name, str):
            raise ValueError('cursor name should be str object')
        return 'Cursor \'' + cursor_name + '\': ' + self.cursors[cursor_name].get_data()


class Editor:
    def __init__(self):
        self.texts = {}

    def add_text(self, name=None, text=''):
        if not check_value_type(name, str):
            raise ValueError('name value should be str object')
        self.texts[name] = Text(text)

    def print_text(self, text_name=None):
        if text_name is None:
            [self.print_text(i) for i in self.texts.keys()]
        else:
            if not check_value_type(text_name, str):
                raise ValueError('text name should be str object')
            print(self.get_text_print_data(text_name))
            self.texts[text_name].print_cursor()

    def get_text_print_data(self, text_name=None):
        if not check_value_type(text_name, str):
            raise ValueError('text name should be str object')
        return 'Text \'' + text_name + '\': ' + self.texts[text_name].get_data()