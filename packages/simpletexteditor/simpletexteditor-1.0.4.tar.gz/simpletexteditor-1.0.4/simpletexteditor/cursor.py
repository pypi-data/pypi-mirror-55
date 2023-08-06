from simpletexteditor import helper as h


class Cursor:
    def __init__(self, start_position=None, end_position=None, is_forward_direction=True, target_data=''):
        self.start_position = start_position
        self.end_position = end_position
        self.is_forward_direction = is_forward_direction
        self.validate_cursor()
        self.data = None
        self.data = self.get_data(target_data)

    def validate_cursor(self):
        if not h.check_value_type(self.start_position, [int, str]):
            raise ValueError('start_position value should be int or str object')

        if not h.check_value_type(self.end_position, [int, str]):
            raise ValueError('end_position value should be int or str object')

        if not h.check_value_type(self.is_forward_direction, bool):
            raise ValueError('is_forward_direction value should be bool object')

    def get_data(self, target_data=None):
        if self.data is None:
            words = h.words_in_text(target_data)         # Массив слов
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

            if h.check_value_type(local_start, int):
                if local_start not in words_range:
                    local_start = 0
                local_start = words[local_start]

            if h.check_value_type(local_end, int):
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
