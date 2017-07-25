#!/usr/bin/env python3

from statsSend.urbanCodeDeploy.urbanCodeDeployApplication import UrbanCodeDeployApplication
from statsSend.urbanCodeDeploy.urbanCodeDeployApplicationProcessRequest import UrbanCodeDeployApplicationProcessRequest

class UrbanCodeDeployTag:
    def __init__(self, session, name):
        self.session = session
        self.name = name

    #[
    #    {
    #        "id": "3d6b2596-e0c3-48d0-ad23-abfd84640acd",
    #        "name": "MyApp",
    #        "active": true,
    #        "tags": [
    #            { "id": "bd8b2f52-c465-4308-addf-77b74758ccc2", "name": "MyTag", ... },
    #            ...
    #        ],
    #        ...
    #    },
    #    ...
    #]
    async def retrieve_applications(self):
        resource_factory = lambda skip, limit: self._url_of_applications(skip, limit)
        result_key = ''
        async for application_json_dict in self.session.get_resource_paginated_as_json(resource_factory, result_key):
            yield UrbanCodeDeployApplication(self.session, application_json_dict)

    #[
    #    {
    #        "id": "f6b5a43b-9d8a-4315-8a38-03ad574d9c98",
    #        "state": "CLOSED",
    #        "startTime": 1500986126238,
    #        ...
    #    },
    #    ...
    #]
    async def retrieve_application_process_requests_since_posix_timestamp(self, since_posix_timestamp):
        resource_factory = lambda skip, limit: self._url_of_summarized_applications_process_requests(skip, limit)
        result_key = ''
        async for summarized_app_proc_req_json_dict in self.session.get_resource_paginated_as_json(resource_factory, result_key):
            if (self._full_app_proc_req_should_be_retrieved(summarized_app_proc_req_json_dict, since_posix_timestamp)):
                full_app_proc_req_json_dict = await self._retrieve_full_app_proc_req(summarized_app_proc_req_json_dict['id'])
                yield UrbanCodeDeployApplicationProcessRequest(full_app_proc_req_json_dict)

    def _url_of_applications(self, skip, limit):
        active_query_string_fragment = 'active=true'
        filter_and_pagination_query_string_fragments = self._filter_and_pagination_query_string_fragments('tags.name', skip, limit)
        query_string = '{:s}&{:s}'.format(active_query_string_fragment, filter_and_pagination_query_string_fragments)
        return '{:s}?{:s}'.format('application', query_string)

    def _url_of_summarized_applications_process_requests(self, skip, limit):
        query_string = self._filter_and_pagination_query_string_fragments('application.tags.name', skip, limit)
        return '{:s}?{:s}'.format('applicationProcessRequest/table', query_string)

    def _filter_and_pagination_query_string_fragments(self, field_to_filter, skip, limit):
        filter_query_string_fragment = 'filterType_{0}=eq&filterClass_{0}=String&filterFields={0}&filterValue_{0}={1}'.format(field_to_filter, self.name)
        pagination_query_string_fragment = 'pageNumber={:d}&rowsPerPage={:d}'.format(skip // limit + 1, limit)
        return '{:s}&{:s}'.format(filter_query_string_fragment, pagination_query_string_fragment)

    def _full_app_proc_req_should_be_retrieved(self, summarized_app_proc_req_json_dict, since_posix_timestamp):
        return 'state' in summarized_app_proc_req_json_dict and \
            'startTime' in summarized_app_proc_req_json_dict and \
            summarized_app_proc_req_json_dict['state'] == 'CLOSED' and \
            summarized_app_proc_req_json_dict['startTime'] >= since_posix_timestamp
    #{
    #    "id": "669bfeea-92e8-47f8-a9e7-03497253bd21",
    #    "result": "SUCCEEDED",
    #    "rootTrace": { "startDate": 1494844210865, "endDate": 1494844229113, "duration": 18248, ... },
    #    "application": { "id": "3d6b2596-e0c3-48d0-ad23-abfd84640acd", "name": "MyApp", ... },
    #    "environment": { "id": "61d39ff5-e3ea-4eb2-99f3-2acef67c1525", "name": "MyEnv", ... },
    #    ...
    #}
    async def _retrieve_full_app_proc_req(self, id):
        full_app_proc_req_resource = '{:s}/{:s}'.format('applicationProcessRequest', id)
        full_app_proc_req_json_dict = await self.session.get_resource_at_once_as_json(full_app_proc_req_resource)
        return full_app_proc_req_json_dict