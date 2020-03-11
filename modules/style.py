class Style:
    style_obj_id = ''
    style_length = 50
    style_char = '.'
    style_end = ': '
    style_return = ''

    def __init__(self, paramter_length=50, parameter_char='.', parameter_end=': '):
        self.style_length = paramter_length
        self.style_char = parameter_char
        self.style_end = parameter_end

    def paint(self, parameter_text, parameter_subject='Console', parameter_request_input=False):
        self.style_return = parameter_subject

        for space in range(len(parameter_subject), self.style_length):
            self.style_return += self.style_char

        self.style_return += self.style_end

        if not parameter_request_input:
            print(self.style_return + parameter_text)
        else:
            return input(self.style_return)
