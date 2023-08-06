import helper as h
import cursor as c


class Text:
    def __init__(self, data=''):
        self.data = data
        self.cursors = {}

    def get_data(self):
        return self.data

    def add_cursor(self, name=None, start_position=None, end_position=None, is_forward_direction=True):
        if not h.check_value_type(name, str):
            raise ValueError('cursor name should be str object')
        self.cursors[str(name)] = c.Cursor(start_position, end_position, is_forward_direction, self.data)

    def print_cursor(self, cursor_name=None):
        if cursor_name is None:
            [self.print_cursor(i) for i in self.cursors.keys()]
        else:
            if not h.heck_value_type(cursor_name, str):
                raise ValueError('cursor name should be str object')
            print(self.get_cursor_print_data(cursor_name))

    def get_cursor_print_data(self, cursor_name=None):
        if not h.check_value_type(cursor_name, str):
            raise ValueError('cursor name should be str object')
        return 'Cursor \'' + cursor_name + '\': ' + self.cursors[cursor_name].get_data()
