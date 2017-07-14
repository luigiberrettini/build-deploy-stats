#!/usr/bin/env python3

class ZabbixReporter:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def send_status(self, timestamp, context, metric_value):
        self._send(timestamp, context + '.STATUS', metric_value)

    def send_duration(self, timestamp, context, metric_value):
        self._send(timestamp, context + '.DURATION', metric_value)

    def _send(self, timestamp, metric_name, metric_value):
        print('timestamp: {:s} - metric_name: {:s} - metric_value: {:s}'.format(timestamp, metric_name, metric_value))