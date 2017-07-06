#!/usr/bin/env python3

from dateutil import parser

class Job:
    def __init__(self, id, name, status, start_timestamp, finish_timestamp, duration):
        self.id = id
        self.name = name
        self.status = status
        self.start_timestamp = parser.parse(start_timestamp)
        self.finish_timestamp = parser.parse(finish_timestamp)
        self.duration = (int(duration) / float(1000)) if duration else (self.finish_timestamp - self.start_timestamp).total_seconds()

    def report(self, reporter):
        reporter.send_status(self.finish_timestamp, self.name, self.status)
        reporter.send_duration(self.finish_timestamp, self.name, self.duration)