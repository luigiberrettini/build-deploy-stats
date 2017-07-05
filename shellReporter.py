#!/usr/bin/env python

class ShellReporter:
    def send_status(self, timestamp, context, metric_value):
        self._send(timestamp, context + '.STATUS', metric_value + ' (%s)' % 'SUCCESS' if metric_value else 'FAILURE')

    def send_duration(self, timestamp, context, metric_value):
        self._send(timestamp, context + '.DURATION', metric_value)

    def _send(self, timestamp, metric_name, metric_value):
        print 'timestamp: %s - metric_name: %s - metric_value: %s' % (timestamp, metric_name, metric_value)