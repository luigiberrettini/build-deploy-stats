#!/usr/bin/env python3

from datetime import datetime, timezone

from reporting.category import Category
from reporting.activity import Activity

#{
#    "_class": "org.jenkinsci.plugins.workflow.job.WorkflowRun",
#    "id": "1",
#    "url": "http://jk.domain/job/ancestor/job/grandfather/job/father/1/",
#    "result": "SUCCESS",
#    "timestamp": 1493222401537,
#    "duration": 51364
#}
class JenkinsBuild:
    def __init__(self, hierarchy_id, json_dict):
        self.id = json_dict['id']
        self.hierarchy_id = hierarchy_id
        self.url = json_dict['url']
        self.result = json_dict['result']
        self.numeric_result = 1 if json_dict['result'] == 'SUCCESS' else 0
        self.start_timestamp = self._posix_timestamp_to_local(json_dict['timestamp'])
        self.finish_timestamp = self._posix_timestamp_to_local(json_dict['timestamp'] + json_dict['duration'])
        self.duration = json_dict['duration']

    def to_activity(self):
        category = Category('Jenkins', self.hierarchy_id)
        return Activity(category, self.id, self.numeric_result, self.start_timestamp, self.finish_timestamp, self.duration)

    def _posix_timestamp_to_local(self, posix_timestamp_in_ms):
        posix_timestamp_in_s = posix_timestamp_in_ms / 1000
        utc_timestamp = datetime.fromtimestamp(posix_timestamp_in_s)
        local_timestamp = utc_timestamp.replace(tzinfo = timezone.utc).astimezone(tz = None)
        return local_timestamp.isoformat()