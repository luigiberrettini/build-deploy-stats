#!/usr/bin/env python

import requests
import teamCityApiProxy

from teamCityBuildConfiguration import TeamCityBuildConfiguration

class TeamCityProject:
    def __init__(self, api_proxy, project_id):
        self.api_proxy = api_proxy
        self.project_id = project_id

    def retrieve_build_configurations(self):
        return list(map(lambda build_configuration: TeamCityBuildConfiguration(self.api_proxy, build_configuration), self._build_configurations()))

    #{
    #    "buildType": [
    #        { "id": "PRJ-A_BT-1", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-A_BT-1/builds/" } },
    #        { "id": "PRJ-B_BT-2", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-B_BT-2/builds/" } }
    #    ]
    #}
    def _build_configurations(self):
        build_types_res_url = 'buildTypes?locator=affectedProject:%s&fields=buildType(id,builds)' % self.project_id
        build_types_full_url = self.api_proxy.full_url_from_resource_url(build_types_res_url)
        try:
            return self.api_proxy.get_resource(build_types_full_url).json()['buildType']
        except Exception:
            print 'Exception retrieving build configurations for project %s' % self.project_id
            raise