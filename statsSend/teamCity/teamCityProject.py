#!/usr/bin/env python3

import ijson.backends.asyncio as ijson

from statsSend.teamCity.teamCityBuildConfiguration import TeamCityBuildConfiguration

class TeamCityProject:
    def __init__(self, session_factory, id):
        self.session_factory = session_factory
        self.id = id

    #{
    #    "nextHref": "/httpAuth/app/rest/buildTypes?locator=affectedProject:PRJ-Aff,start:500,count:100&fields=nextHref,buildType(id,builds)",
    #    "buildType": [
    #        { "id": "PRJ-A_BT-1", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-A_BT-1/builds/" } },
    #        ...
    #    ]
    #}
    async def retrieve_build_configurations(self):
        resource_factory = lambda skip, limit: self._url_of_build_configurations(skip, limit)
        result_key = 'buildType'
        async with self.session_factory() as session:
            async for build_configuration_json_dict in session.get_resource_paginated_as_json(resource_factory, result_key):
                yield TeamCityBuildConfiguration(session, build_configuration_json_dict)

    def _url_of_build_configurations(self, skip, limit):
        locator_query_string_fragment = 'locator=affectedProject:{:s},start:{:d},count:{:d}'.format(self.id, skip, limit)
        fields_query_string_fragment = 'fields=nextHref,buildType(id,builds)'
        query_string = '{:s}&{:s}'.format(locator_query_string_fragment, fields_query_string_fragment)
        return '{:s}?{:s}'.format('buildTypes', query_string)