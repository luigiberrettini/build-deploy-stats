#!/usr/bin/env python3

import json

from datetime import datetime, timedelta, timezone

from pyzabbix import ZabbixMetric, ZabbixSender

class ZabbixReporter:
    epoch = datetime(1970, 1, 1, tzinfo = timezone.utc)
    one_second = timedelta(seconds = 1)

    def __init__(self, settings):
        self.sender = ZabbixSender(settings['server'], settings['port'])
        self.hostname = settings['hostname']
        self.discovery_rule_key_prefix = settings['discovery_rule_key_prefix']
        self.category_tool_macro = settings['category_tool_macro']
        self.category_context_macro = settings['category_context_macro']

    def report_categories(self, categories):
        if (len(categories) <= 0):
            return
        to_dict = lambda x: { self.category_tool_macro: '{:s}'.format(x.tool), self.category_context_macro: '{:s}'.format(x.context) }
        category_dict_list = list(map(to_dict, categories))
        discovery_rule_key = '{:s}{:s}'.format(self.discovery_rule_key_prefix, categories[0].tool).lower()
        discovery_rule_payload = json.dumps({ 'data': category_dict_list })
        packet = [ ZabbixMetric(self.hostname, discovery_rule_key, discovery_rule_payload) ]
        self.sender.send(packet)

    def report_activity(self, activity):
        posix_timestamp = (activity.timestamp - self.epoch) // self.one_second
        packet = [
            ZabbixMetric(self.hostname, self._zabbixMetricKey('STATUS', activity), activity.status, posix_timestamp),
            ZabbixMetric(self.hostname, self._zabbixMetricKey('DURATION', activity), activity.duration, posix_timestamp)
        ]
        self.sender.send(packet)

    def _zabbixMetricKey(self, metricKind, activity):
        return '{0}_{1}[{0}.{2}]'.format(activity.tool, metricKind, activity.type)