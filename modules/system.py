import json
import os


class System:
    system_file_settings = 'None'

    def __init__(self, system_settings_file):
        self.system_file_settings = system_settings_file

    def load_setting(self, parameter_setting='None', parameter_file='None'):
        try:
            if parameter_file == 'None':
                cache_file = open(self.system_file_settings).readlines()
            else:
                cache_file = open(parameter_file).readlines()

            for line in cache_file:
                if line[0] != '#':
                    print('Thist line will be skipped: ' + line)
        except FileNotFoundError:
            print('The file ' + parameter_file + ' does not exists. The same applies for the System file: ' +
                  self.system_file_settings)


class File:
    file_total_written = 0
    file_total_readed = 0

    def save(self, parameter_file, parameter_content):
        os.makedirs(os.path.dirname(parameter_file), exist_ok=True)
        open(parameter_file, 'w').writelines(parameter_content)
        self.file_total_written += 1

    def save_json(self, parameter_file, parameter_content):
        os.makedirs(os.path.dirname(parameter_file), exist_ok=True)
        open(parameter_file, 'w').write(json.dumps(parameter_content))
        self.file_total_written += 1

    def read_raw(self, parameter_file):
        cache_raw = open(parameter_file).read()
        self.file_total_readed += 1
        return cache_raw

    def read_json(self, parameter_file):
        cache_raw = open(parameter_file).read()
        self.file_total_readed += 1
        return json.loads(cache_raw)

    def read_lines(self, parameter_file):
        cache_lines = open(parameter_file).readlines()
        self.file_total_readed += 1
        return cache_lines
