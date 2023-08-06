from simpletexteditor import helper as h
from simpletexteditor import text as t


class Editor:
    def __init__(self):
        self.texts = {}

    def add_text(self, name=None, text=''):
        if not h.check_value_type(name, str):
            raise ValueError('name value should be str object')
        self.texts[name] = t.Text(text)

    def print_text(self, text_name=None):
        if text_name is None:
            [self.print_text(i) for i in self.texts.keys()]
        else:
            if not h.check_value_type(text_name, str):
                raise ValueError('text name should be str object')
            print(self.get_text_print_data(text_name))
            self.texts[text_name].print_cursor()

    def get_text_print_data(self, text_name=None):
        if not h.check_value_type(text_name, str):
            raise ValueError('text name should be str object')
        return 'Text \'' + text_name + '\': ' + self.texts[text_name].get_data()

if __name__ == '__main__':
    e = Editor()
    e.add_text('test', 'dskfdk sd jfs djk d jskdk sd')
    e.print_text()
    
