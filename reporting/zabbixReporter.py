#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone

from pyzabbix import ZabbixMetric, ZabbixSender

class ZabbixReporter:
    epoch = datetime(1970, 1, 1, tzinfo = timezone.utc)
    one_second = timedelta(seconds = 1)

    def __init__(self, settings):
        self.sender = ZabbixSender(settings['server'], settings['port'])
        self.hostname = settings['hostname']
        self.discovery_rule_key = settings['discovery_rule_key']
        self.category_tool_macro = settings['category_tool_macro']
        self.category_context_macro = settings['category_context_macro']

    def report_categories(self, categories):
        to_dict = lambda x: { self.category_tool_macro: '{:s}'.format(x.tool), self.category_context_macro: '{:s}'.format(x.context) }
        category_dict_list = list(map(to_dict, categories))
        discovery_rule_payload = json.dumps({ 'data': category_dict_list })
        packet = [ ZabbixMetric(self.hostname, self.discovery_rule_key, discovery_rule_payload) ]
        self.sender.send(packet)

    def report_job(self, job):
        posix_timestamp = (job.timestamp - self.epoch) // self.one_second
        category = '{:s}.{:s}'.format(job.tool, job.type)
        packet = [
          ZabbixMetric(self.hostname, 'STATUS[{:s}]'.format(category), job.status, posix_timestamp),
          ZabbixMetric(self.hostname, 'DURATION[{:s}]'.format(category), job.duration, posix_timestamp),
        ]
        self.sender.send(packet)