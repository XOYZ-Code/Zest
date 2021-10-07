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
        self.project_info_file = 'data/system/project_info.pl'
        self.project_log_file = 'data/system/project_log.pl'
        #   loading project information
        try:
            self.log('Loading project Information')
            self.load_info()
        except FileNotFoundError:
            print('self.load_info() returned FileNotFoundError')
            os.makedirs(self.project_log_file.split('/project')[0])
            os.makedirs(self.project_info_file.split('/project')[0])
        #   Counting new build
        self.new_build()
        self.log('Finished Loading of >' +
                 self.project_name + '< from >' +
                 self.project_author + '< at version >' +
                 self.project_version_str + '<')
        self.save_info()

    def new_build(self):
        self.project_version[2] += 1
        self.project_version_str = str(self.project_version[0]) + '.' + \
                                   str(self.project_version[1]) + ' Build ' + str(self.project_version[2])
        self.log('Increasing build number to ' + str(self.project_version[2]))

    def new_minor_update(self):
        self.project_version[1] += 1
        self.project_version[2] = 0
        self.project_version_str = str(self.project_version[0]) + '.' + \
                                   str(self.project_version[1]) + ' Build ' + str(self.project_version[2])
        self.log('Increasing minor number to ' + str(self.project_version[1]))

    def new_major_update(self):
        self.project_version[0] += 1
        self.project_version[1] = 0
        self.project_version[2] = 0
        self.project_version_str = str(self.project_version[0]) + '.' + \
                                   str(self.project_version[1]) + ' Build ' + str(self.project_version[2])
        self.log('Increasing major number to ' + str(self.project_version[0]))

    def save_info(self):
        cache_file_content = [
            'Project name............: ' + self.project_name + '\n',
            'Project Author..........: ' + self.project_author + '\n',
            'Project Version nr......: ' + str(self.project_version) + '\n',
            'Project Version str.....: ' + self.project_version_str
        ]
        self.project_file_control.save(self.project_info_file, cache_file_content)
        
        README = open('README.md').readlines()
        README[0] = '# image_upscaler ' + self.project_version_str + '\n'
        open('README.md', 'w').writelines(README)

    def log(self, parameter_to_log, print_log=False, save_to_log=True):
        cache_log = ''

        for space in range(len(time.ctime()), 20):
            cache_log += '.'

        cache_log += ': '
        end_str = str(time.ctime()) + cache_log + parameter_to_log
        if save_to_log:
            open(self.project_log_file, 'a').write(end_str + '\n')
        if print_log:
            print(end_str)

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
