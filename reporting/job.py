#!/usr/bin/env python3

from dateutil import parser

class Job:
    def __init__(self, category, id, status, start_timestamp, finish_timestamp, duration = None):
        self.tool_id = category.tool
        self.type_id = category.context
        self.id = id
        self.status_bit = int(status)
        self.start_timestamp = parser.parse(start_timestamp)
        self.finish_timestamp = parser.parse(finish_timestamp)
        self.duration_seconds = (self.finish_timestamp - self.start_timestamp).total_seconds() if duration is None else (int(duration) / float(1000))

    @property
    def timestamp(self):
        return self.finish_timestamp

    @property
    def tool(self):
        return self.tool_id

    @property
    def type(self):
        return self.type_id

    @property
    def status(self):
        return self.status_bit

    @property
    def duration(self):
        return self.duration_seconds