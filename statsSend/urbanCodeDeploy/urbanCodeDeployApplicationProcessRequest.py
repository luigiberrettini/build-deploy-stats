#!/usr/bin/env python3

from datetime import datetime, timezone

from reporting.category import Category
from reporting.activity import Activity

#{
#    "id": "669bfeea-92e8-47f8-a9e7-03497253bd21",
#    "state": "CLOSED",
#    "result": "SUCCEEDED",
#    "rootTrace": { "startDate": 1494844210865, "endDate": 1494844229113, "duration": 18248, ... },
#    "application": { "id": "3d6b2596-e0c3-48d0-ad23-abfd84640acd", "name": "MyApp", ... },
#    "environment": { "id": "61d39ff5-e3ea-4eb2-99f3-2acef67c1525", "name": "MyEnv", ... },
#    ...
#}
class UrbanCodeDeployApplicationProcessRequest:
    def __init__(self, json_dict):
        self.id = json_dict['id']
        self.application = json_dict['application']['name']
        self.environment = json_dict['environment']['name']
        self.state = json_dict['state']
        self.result = json_dict['result']
        self.numeric_result = 1 if json_dict['result'] in ['SCHEDULED FOR FUTURE', 'SUCCEEDED', 'COMPENSATED', 'AWAITING APPROVAL'] else 0
        self.start_timestamp = self._posix_timestamp_to_local(json_dict['rootTrace']['startDate'])
        self.finish_timestamp = self._posix_timestamp_to_local(json_dict['rootTrace']['endDate'])
        self.duration = json_dict['rootTrace']['duration']

    def to_activity(self):
        category = Category('UrbanCodeDeploy', self.application, self.environment)
        return Activity(category, self.id, self.numeric_result, self.start_timestamp, self.finish_timestamp, self.duration)

    def _posix_timestamp_to_local(self, posix_timestamp_in_ms):
        posix_timestamp_in_s = posix_timestamp_in_ms / 1000
        utc_timestamp = datetime.fromtimestamp(posix_timestamp_in_s)
        local_timestamp = utc_timestamp.replace(tzinfo = timezone.utc).astimezone(tz = None)
        return local_timestamp.isoformat()