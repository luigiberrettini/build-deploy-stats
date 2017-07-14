#!/usr/bin/env python3

import ijson.backends.asyncio as ijson

from teamCityBuildRun import TeamCityBuildRun

class TeamCityBuildConfiguration:
    def __init__(self, json_dict, connection, url_builder, page_size):
        self.id = json_dict['id']
        self.build_runs_hypermedia_link = json_dict['builds']['href']
        self.connection = connection
        self.url_builder = url_builder
        self.page_size = page_size

    async def retrieve_build_runs_since_timestamp(self, since_timestamp):
        async with self.connection.get_session() as session:
            async for build_run_json_dict in self._paginated_build_runs(session, since_timestamp, 0, self.page_size):
                yield TeamCityBuildRun(build_run_json_dict)

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
    async def _paginated_build_runs(self, session, since_timestamp, skip, limit):
        build_runs_url = self._url_of_build_runs_since_timestamp(since_timestamp, skip, limit)

        async with session.get(build_runs_url) as response:
            #print(await response.text())
            count = 0
            #async for build_run in ijson.items(response.content, 'build.item', yajl_backend = yajl2_cffi):
            #async for build_run in ijson.items(response.content, 'build.item', yajl_backend = yajl2):
            async for build_run in ijson.items(response.content, 'build.item'):
                count += 1
                yield build_run
            if not count:
                return
            async for build_run in self._paginated_build_runs(session, since_timestamp, skip + limit, limit):
                yield build_run

    def _url_of_build_runs_since_timestamp(self, since_timestamp, skip, limit):
        locator_query_string_fragment = 'locator=state:finished,sinceDate:{:s},start:{:d},count:{:d}'.format(self._url_encode_timestamp(since_timestamp), skip, limit)
        fields_query_string_fragment = 'fields=nextHref,build(id,status,buildType(id,projectId),startDate,finishDate,statistics(property))'
        query_string = '{:s}&{:s}'.format(locator_query_string_fragment, fields_query_string_fragment)
        return '{:s}?{:s}'.format(self.url_builder.full_url_from_hypermedia_link(self.build_runs_hypermedia_link), query_string)

    def _url_encode_timestamp(self, timestamp):
        return timestamp.replace('+', '%2b')