#!/usr/bin/env python3

import json

class ShellReporter:
    def report_categories(self, categories):
        to_dict = lambda x: { 'TOOL': '{:s}'.format(x.tool), 'CONTEXT': '{:s}'.format(x.context) }
        category_dict_list = list(map(to_dict, categories))
        print(json.dumps(category_dict_list))

    def report_activity(self, activity):
        category = '{:s}->{:s}'.format(activity.tool, activity.type)
        self._report_activity(activity.timestamp, '{:s}.STATUS'.format(category), '{:d} ({:s})'.format(activity.status, 'SUCCESS' if activity.status else 'FAILURE'))
        self._report_activity(activity.timestamp, '{:s}.DURATION'.format(category), activity.duration)

    def _report_activity(self, timestamp, metric_name, metric_value):
        print('timestamp: {:%Y:%m:%dT:%H:%M:%S:%z} | metric_name: {:s} | metric_value: {}'.format(timestamp, metric_name, metric_value))