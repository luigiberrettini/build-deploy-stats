#!/usr/bin/env python3

import requests
import teamCityApiProxy

from teamCityBuildRun import TeamCityBuildRun

class TeamCityBuildConfiguration:
    def __init__(self, api_proxy, build_configuration):
        self.api_proxy = api_proxy
        self.build_configuration = build_configuration

    def retrieve_jobs_since_timestamp(self, since_timestamp, skip, limit):
        build_runs = self._build_runs_since_timestamp(since_timestamp, skip, limit)
        return list(map(lambda x: TeamCityBuildRun(x).toJob(), build_runs))

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
    #        {
    #            "id": "2081742",
    #            "status": "FAILURE",
    #            "buildType": { "id": "PRJ-A_BT-1", "projectId": "PRJ-A" },
    #            "startDate": "20171016T110951+0200",
    #            "finishDate": "20171116T111011+0200",
    #            "statistics": { "property": [ { "name": "BuildDuration", "value": "20316" }, { "name": "SuccessRate", "value": "1" } ] }
    #        }
    #    ]
    def _build_runs_since_timestamp(self, since_timestamp, skip, limit):
        build_runs_url = self._url_of_build_runs_since_timestamp(since_timestamp, skip, limit)
        try:
            return self.api_proxy.get_resource(build_runs_url).json()['build']
        except Exception:
            print('Exception retrieving build runs at URL {:s}'.format(build_runs_url))
            raise

    def _url_of_build_runs_since_timestamp(self, since_timestamp, skip, limit):
        locator_query_string_fragment = 'locator=state:finished,sinceDate:{:s},start:{:d},count:{:d}'.format(self._url_encode_timestamp(since_timestamp), skip, limit)
        fields_query_string_fragment = 'fields=nextHref,build(id,status,buildType(id,projectId),startDate,finishDate,statistics(property))'
        query_string = '{:s}&{:s}'.format(locator_query_string_fragment, fields_query_string_fragment)
        return '{:s}?{:s}'.format(self.api_proxy.full_url_from_hypermedia_link(self.build_configuration['builds']['href']), query_string)

    def _url_encode_timestamp(self, timestamp):
        return timestamp.replace('+', '%2b')