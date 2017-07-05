#!/usr/bin/env python

import requests
import teamCityApiProxy

from teamCityBuildRun import TeamCityBuildRun

class TeamCityBuildConfiguration:
    def __init__(self, api_proxy, build_configuration):
        self.api_proxy = api_proxy
        self.build_configuration = build_configuration

    def retrieve_jobs_since_timestamp(self, since_timestamp):
        return list(map(lambda build_run: TeamCityBuildRun(build_run).toJob(), self._build_runs_since_timestamp(since_timestamp)))

    #{
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
    def _build_runs_since_timestamp(self, since_timestamp):
        builds_url = self._url_of_build_runs_since_timestamp(since_timestamp)
        try:
            return self.api_proxy.get_resource(builds_url).json()['build']
        except Exception:
            print 'Exception retrieving build runs at URL %s' % builds_url
            raise

    def _url_of_build_runs_since_timestamp(self, since_timestamp):
        locator_query_string_fragment = 'state:finished,sinceDate:%s' % self._url_encode_timestamp(since_timestamp)
        fields_query_string_fragment = 'build(id,status,buildType(id,projectId),startDate,finishDate,statistics(property))'
        query_string = 'locator=%s&fields=%s' % (locator_query_string_fragment, fields_query_string_fragment)
        return '%s?%s' % (self.api_proxy.full_url_from_hypermedia_link(self.build_configuration['builds']['href']), query_string)

    def _url_encode_timestamp(self, timestamp):
        return timestamp.replace('+', '%2b')