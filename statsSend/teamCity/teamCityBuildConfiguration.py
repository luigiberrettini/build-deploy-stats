#!/usr/bin/env python3

import ijson.backends.asyncio as ijson

from reporting.category import Category
from statsSend.teamCity.teamCityBuildRun import TeamCityBuildRun

class TeamCityBuildConfiguration:
    def __init__(self, session, json_dict):
        self.session = session
        self.id = json_dict['id']
        self.build_runs_hypermedia_link = json_dict['builds']['href']

    def to_category(self):
        return Category('TeamCity', self.id)

    #{
    #    "nextHref": "/httpAuth/app/rest/builds?
    #                 locator=state:finished,sinceDate:20160622T121203%2B0200,start:500,count:100&
    #                 fields=nextHref,build(id,status,buildType(id,projectId),startDate,finishDate,statistics(property))",
    #    "build": [
    #        {
    #            "id": "2081741",
    #            "status": "SUCCESS",
    #            "buildType": { "id": "PRJ-A_BT-1", "projectId": "PRJ-A" },
    #            "startDate": "20160916T110951+0200",
    #            "finishDate": "20160916T111011+0200",
    #            "statistics": { "property": [ { "name": "BuildDuration", "value": "10362" }, { "name": "SuccessRate", "value": "0" } ] }
    #        },
    #        ...
    #    ]
    #}
    async def retrieve_build_runs_since_timestamp(self, since_timestamp):
        relative_url_factory = lambda skip, limit: self._url_of_build_runs_since_timestamp(since_timestamp, skip, limit)
        result_key = 'build'
        async for build_run_json_dict in self.session.get_url_paginated_as_json(relative_url_factory, result_key):
            yield TeamCityBuildRun(build_run_json_dict)

    def _url_of_build_runs_since_timestamp(self, since_timestamp, skip, limit):
        locator_query_string_fragment = 'locator=state:finished,sinceDate:{:s},start:{:d},count:{:d}'.format(self._url_encode_timestamp(since_timestamp), skip, limit)
        fields_query_string_fragment = 'fields=nextHref,build(id,status,buildType(id,projectId),startDate,finishDate,statistics(property))'
        query_string = '{:s}&{:s}'.format(locator_query_string_fragment, fields_query_string_fragment)
        return '{:s}?{:s}'.format(self.build_runs_hypermedia_link, query_string)

    def _url_encode_timestamp(self, timestamp):
        return timestamp.replace('+', '%2b')