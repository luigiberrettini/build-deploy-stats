#!/usr/bin/env python3

import requests
import teamCityApiProxy

from teamCityBuildConfiguration import TeamCityBuildConfiguration

class TeamCityProject:
    def __init__(self, api_proxy, project_id):
        self.api_proxy = api_proxy
        self.project_id = project_id

    def retrieve_build_configurations(self, skip, limit):
        build_configurations = self._build_configurations(skip, limit)
        return list(map(lambda x: TeamCityBuildConfiguration(self.api_proxy, x), build_configurations))

    #{
    #    "nextHref": "/httpAuth/app/rest/buildTypes?locator=affectedProject:PRJ-Aff,start:500,count:100&fields=nextHref,buildType(id,builds)",
    #    "buildType": [
    #        { "id": "PRJ-A_BT-1", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-A_BT-1/builds/" } },
    #        { "id": "PRJ-B_BT-2", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-B_BT-2/builds/" } }
    #    ]
    #}
    def _build_configurations(self, skip, limit):
        build_configurations_url = self._url_of_build_configurations(skip, limit)
        try:
            return self.api_proxy.get_resource(build_configurations_url).json()['buildType']
        except Exception:
            print('Exception retrieving build configurations for project {:s}'.format(self.project_id))
            raise

    def _url_of_build_configurations(self, skip, limit):
        locator_query_string_fragment = 'locator=affectedProject:{:s},start:{:d},count:{:d}'.format(self.project_id, skip, limit)
        fields_query_string_fragment = 'fields=nextHref,buildType(id,builds)'
        query_string = '{:s}&{:s}'.format(locator_query_string_fragment, fields_query_string_fragment)
        return '{:s}?{:s}'.format(self.api_proxy.full_url_from_resource_url('buildTypes'), query_string)