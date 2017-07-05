#!/usr/bin/env python

from job import Job

#{
#    "id": 2081741,
#    "status": "SUCCESS",
#    "buildType": { "id": "PRJ-A_BT-1", "projectId": "PRJ-A" },
#    "startDate": "20160916T110951+0200",
#    "finishDate": "20160916T111011+0200",
#    "statistics": { "property": [ { "name": "BuildDuration", "value": "20316" }, { "name": "SuccessRate", "value": "1" } ] }
#}
class TeamCityBuildRun:
    def __init__(self, json_dict):
        properties = { name_value_pair['name']: name_value_pair['value'] for name_value_pair in json_dict['statistics']['property'] }
        self.id = json_dict['id']
        self.build_type_id = json_dict['buildType']['id']
        self.project_id = json_dict['buildType']['projectId']
        self.status = json_dict['status']
        self.numeric_status = properties['SuccessRate']
        self.start_timestamp = json_dict['startDate']
        self.finish_timestamp = json_dict['finishDate']
        self.duration = properties['BuildDuration']

    def toJob(self):
        return Job(self.id, self.build_type_id, self.numeric_status, self.start_timestamp, self.finish_timestamp, self.duration)