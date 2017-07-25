#!/usr/bin/env python3

from reporting.category import Category

class UrbanCodeDeployApplication:
    def __init__(self, session, json_dict):
        self.session = session
        self.id = json_dict['id']
        self.name = json_dict['name']
        self.active = json_dict['active']
        self.tags = json_dict['tags']

    async def retrieve_categories(self):
        for environment_json_dict in await self._related_environments():
            yield Category('UrbanCodeDeploy', self.name, environment_json_dict['name'])

    #[
    #    {
    #        "id": "61d39ff5-e3ea-4eb2-99f3-2acef67c1525",
    #        "name": "MyEnv",
    #        "active": true,
    #        ...
    #    },
    #    ...
    #]
    async def _related_environments(self):
        query_string = 'filterType_{0}=eq&filterClass_{0}=UUID&filterFields={0}&filterValue_{0}={1}'.format('application.id', self.id)
        resource = '{:s}?{:s}'.format('environment', query_string)
        return await self.session.get_resource_at_once_as_json(resource)