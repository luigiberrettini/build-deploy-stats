#!/usr/bin/env python3

from dateutil import parser
from datetime import timezone

from reporting.category import Category
from reporting.job import Job

#{
#    "Id": "ServerTasks-156597",
#    "IsCompleted": true,
#    "State": "Success",
#    "StartTime": "2017-06-12T13:03:18.345+00:00",
#    "CompletedTime": "2017-06-12T13:03:51.923+00:00",
#    ...
#    "Links": { ... }
#}
class OctopusDeployTask:
    def __init__(self, project, environment, json_dict):
        self.id = json_dict['Id']
        self.project = project
        self.environment = environment
        self.completed = json_dict['IsCompleted']
        self.state = json_dict['State']
        self.numeric_state = 1 if self.state == 'Success' else 0
        self.start_timestamp = json_dict['StartTime']
        self.finish_timestamp = json_dict['CompletedTime']

    @property
    def is_completed(self):
        return self.completed

    def to_job(self):
        category = Category('OctopusDeploy', self.project, self.environment)
        start_timestamp = self._utc_timestamp_to_local(self.start_timestamp)
        finish_timestamp = self._utc_timestamp_to_local(self.finish_timestamp)
        return Job(category, self.id, self.numeric_state, start_timestamp, finish_timestamp)
        
    def _utc_timestamp_to_local(self, timestamp):
        parsed = parser.parse(timestamp)
        local = parsed.replace(tzinfo = timezone.utc).astimezone(tz = None)
        return local.isoformat()