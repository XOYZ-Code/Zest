import os
import sys
import time
import json

from .system import File


class Project:
    project_author = ''
    project_name = ''
    project_version = [0, 0, 0]
    project_version_str = '0.0.0'
    #   [0] Major Update
    #   [1] Minor Update
    #   [2] Build nr. in the current Minor Update of the current Major update
    project_new_feature = False
    project_info_file = 'data/system/'
    project_file_control = File()
    project_log_file = ''

    def __init__(self, parameter_name, parameter_author):
        self.project_name = parameter_name
        self.project_author = parameter_author

    def initialize_project_build(self):
        #   set project info file path
        self.project_info_file = 'data/system/project_info.pi'
        self.project_log_file = 'data/system/project_log.pl'
        #   loading project information
        try:
            self.load_info()
        except FileNotFoundError:
            print('self.load_info() returned FileNotFoundError')
        self.log('Loading project Information')
        #   Counting new build
        self.new_build()
        self.log('Increasing build number to ' + str(self.project_version[2]))
        self.log('Finished Loading of >' +
                 self.project_name + '< from >' +
                 self.project_author + '< at version >' +
                 self.project_version_str + '<')
        self.save_info()

    def new_build(self):
        self.project_version[2] += 1
        self.project_version_str = str(self.project_version[0]) + '.' + \
                                   str(self.project_version[1]) + ' Build ' + str(self.project_version[2])

    def new_minor_update(self):
        self.project_version[1] += 1
        self.project_version[2] = 0
        self.project_version_str = str(self.project_version[0]) + '.' + \
                                   str(self.project_version[1]) + ' Build ' + str(self.project_version[2])

    def new_major_update(self):
        self.project_version[0] += 1
        self.project_version[1] = 0
        self.project_version[2] = 0
        self.project_version_str = str(self.project_version[0]) + '.' + \
                                   str(self.project_version[1]) + ' Build ' + str(self.project_version[2])

    def save_info(self):
        cache_file_content = [
            'Project name............: ' + self.project_name + '\n',
            'Project Author..........: ' + self.project_author + '\n',
            'Project Version nr......: ' + str(self.project_version) + '\n',
            'Project Version str.....: ' + self.project_version_str
        ]
        self.project_file_control.save(self.project_info_file, cache_file_content)

    def log(self, parameter_to_log):
        cache_log = ''

        for space in range(len(time.ctime()), 20):
            cache_log += '.'

        cache_log += ': '

        open(self.project_log_file, 'a').write(str(time.ctime()) + cache_log + parameter_to_log + '\n')

    def load_info(self):
        cache_file_content = open(self.project_info_file)
        for line in cache_file_content:
            cache_line = line.replace('\n', '').split(': ')
            if 'Project Name' in cache_line[0]:
                self.project_name = cache_line[1]
            if 'Project Author' in cache_line[0]:
                self.project_author = cache_line[1]
            if 'Project Version nr' in cache_line[0]:
                self.project_version = eval(cache_line[1])

            self.project_version_str = str(self.project_version[0]) + '.' + str(self.project_version[1]) + ' Build ' + \
                                       str(self.project_version[2])

    class Statistics:
        stats = None
        stats_file = 'data/system/statistics.json'
        stats_file_handling = File()

        def __init__(self):
            self.stats = self.stats_file_handling.read_json(self.stats_file)

        def update_stat(self, parameter_stat, new_value):
            cache_stats = self.stats_file_handling.read_json(self.stats_file)
            for stat in cache_stats:
                if stat == parameter_stat:
                    if new_value.split(' ')[0] == 'add' or new_value.split(' ')[0] == '+':
                        cache_stats[parameter_stat] = \
                            float(cache_stats[parameter_stat]) + float(new_value.split(' ')[1])
                    else:
                        if new_value.split(' ')[0] == 'substract' or new_value.split(' ')[0] == '-':
                            cache_stats[parameter_stat] = \
                                float(cache_stats[parameter_stat]) - float(new_value.split(' ')[1])
                        else:
                            if new_value.split(' ')[0] == 'multiply' or new_value.split(' ')[0] == '*':
                                cache_stats[parameter_stat] = \
                                    float(cache_stats[parameter_stat]) * float(new_value.split(' ')[1])
                            else:
                                if new_value.split(' ')[0] == 'divide' or new_value.split(' ')[0] == '/':
                                    cache_stats[parameter_stat] = \
                                        float(cache_stats[parameter_stat]) / float(new_value.split(' ')[1])
                                else:
                                    cache_stats[parameter_stat] = new_value
            self.stats_file_handling.save_json(self.stats_file, cache_stats)
