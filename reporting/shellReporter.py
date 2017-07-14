#!/usr/bin/env python3

import json

class ShellReporter:
    def report_categories(self, categories):
        to_dict = lambda x: { '{#TOOL}}': '{:s}'.format(x.tool), '{#TYPE}': '{:s}'.format(x.context) }
        category_dict_list = list(map(to_dict, categories))
        print(json.dumps(category_dict_list))

    def report_job_stats(self, job):
        category = '{:s}-{:s}'.format(job.tool, job.type)
        self._report_job_stat(job.timestamp, '{:s}.STATUS'.format(category), '{:d} ({:s})'.format(job.status, 'SUCCESS' if job.status else 'FAILURE'))
        self._report_job_stat(job.timestamp, '{:s}.DURATION'.format(category), job.duration)

    def _report_job_stat(self, timestamp, metric_name, metric_value):
        print('timestamp: {:%Y:%m:%dT:%H:%M:%S:%z} - metric_name: {:s} - metric_value: {}'.format(timestamp, metric_name, metric_value))