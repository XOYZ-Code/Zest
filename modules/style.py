import numpy
from .terminalsize import *


class Style:
    style_obj_id = ''
    style_length = 50
    style_char = '.'
    style_end = ': '
    style_return = ''
    secure_id_length = 10
    secure_letter_list = list('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    align_space = ' '

    def __init__(self, paramter_length=50, parameter_char='.', parameter_end=': '):
        self.style_length = paramter_length
        self.style_char = parameter_char
        self.style_end = parameter_end

    def fit_number(self, number, length=5):
        if isinstance(number, str):
            cache = number
        else:
            cache = str(number)
        self.style_return = ''
        for i in range(length - len(cache)):
            self.style_return += '0'
        self.style_return += cache
        return self.style_return

    def paint(self, parameter_text='', parameter_subject='Console', parameter_request_input=False):
        self.style_return = parameter_subject

        for space in range(len(parameter_subject), self.style_length):
            self.style_return += self.style_char

        self.style_return += self.style_end

        if not parameter_request_input:
            print(self.style_return + str(parameter_text))
        else:
            return input(self.style_return)

    def create_id(self, length=secure_id_length):
        return_value = ''
        secure = self.secure_letter_list
        for i in range(length):
            return_value += str(secure[numpy.random.randint(len(secure))])
        return return_value

    def align_horizontal(self, left_content, right_content, length='full_console', space_char=' '):
        if length == 'full_console':
            length = get_terminal_size()[0]
        self.align_space = space_char
        return_val = left_content
        for i in range(len(left_content), length - len(right_content)):
            return_val += self.align_space

        return return_val + right_content

    def align_center(self, content, width='full_console', space_char=' '):
        if width == 'full_console':
            width = get_terminal_size()[0]
        self.align_space = space_char
        cache = ''
        for i in range(int((width - len(content)) / 2)):
            cache += self.align_space
        ret = cache + content + cache
        for i in range(len(ret), width):
            ret += self.align_space
        return ret
