import os
import json

from modules.system import File


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
