#!/usr/bin/env python3

import json

class ShellReporter:
    def report_categories(self, categories):
        to_dict = lambda x: { 'TOOL': '{:s}'.format(x.tool), 'CONTEXT': '{:s}'.format(x.context) }
        category_dict_list = list(map(to_dict, categories))
        print(json.dumps(category_dict_list))

    def report_job(self, job):
        category = '{:s}->{:s}'.format(job.tool, job.type)
        self._report_job(job.timestamp, '{:s}.STATUS'.format(category), '{:d} ({:s})'.format(job.status, 'SUCCESS' if job.status else 'FAILURE'))
        self._report_job(job.timestamp, '{:s}.DURATION'.format(category), job.duration)

    def _report_job(self, timestamp, metric_name, metric_value):
        print('timestamp: {:%Y:%m:%dT:%H:%M:%S:%z} | metric_name: {:s} | metric_value: {}'.format(timestamp, metric_name, metric_value))