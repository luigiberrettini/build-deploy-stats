#!/usr/bin/env python3

import ijson.backends.asyncio as ijson

from statsSend.teamCity.teamCityBuildConfiguration import TeamCityBuildConfiguration

class TeamCityProject:
    def __init__(self, id, connection, url_builder, page_size):
        self.id = id
        self.connection = connection
        self.url_builder = url_builder
        self.page_size = page_size

    async def retrieve_build_configurations(self):
        async with self.connection.get_session() as session:
            async for build_configuration_json_dict in self._paginated_build_configurations(session, 0, self.page_size):
                yield TeamCityBuildConfiguration(build_configuration_json_dict, self.connection, self.url_builder, self.page_size)

    #{
    #    "nextHref": "/httpAuth/app/rest/buildTypes?locator=affectedProject:PRJ-Aff,start:500,count:100&fields=nextHref,buildType(id,builds)",
    #    "buildType": [
    #        { "id": "PRJ-A_BT-1", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-A_BT-1/builds/" } },
    #        { "id": "PRJ-B_BT-2", "builds": { "href": "/httpAuth/app/rest/buildTypes/id:PRJ-B_BT-2/builds/" } }
    #    ]
    #}
    async def _paginated_build_configurations(self, session, skip, limit):
        build_configurations_url = self._url_of_build_configurations(skip, limit)
        async with session.get(build_configurations_url) as response:
            #print(await response.text())
            count = 0
            #async for build_configuration in ijson.items(response.content, 'buildType.item', yajl_backend = yajl2_cffi):
            #async for build_configuration in ijson.items(response.content, 'buildType.item', yajl_backend = yajl2):
            async for build_configuration in ijson.items(response.content, 'buildType.item'):
                count += 1
                yield build_configuration
            if not count:
                return
            async for build_configuration in self._paginated_build_configurations(session, skip + limit, limit):
                yield build_configuration

    def _url_of_build_configurations(self, skip, limit):
        locator_query_string_fragment = 'locator=affectedProject:{:s},start:{:d},count:{:d}'.format(self.id, skip, limit)
        fields_query_string_fragment = 'fields=nextHref,buildType(id,builds)'
        query_string = '{:s}&{:s}'.format(locator_query_string_fragment, fields_query_string_fragment)
        return '{:s}?{:s}'.format(self.url_builder.full_url_from_resource_url('buildTypes'), query_string)