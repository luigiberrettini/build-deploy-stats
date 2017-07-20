#!/usr/bin/env python3

from dateutil import parser

from reporting.category import Category
from statsSend.octopusDeploy.octopusDeployTask import OctopusDeployTask

class OctopusDeployProject:
    def __init__(self, session, json_dict):
        self.session = session
        self.id = json_dict['Id']
        self.name = json_dict['Name']
        self.slug = json_dict['Slug']
        self.releases_hypermedia_link = json_dict['Links']['Releases'].split('{')[0]

    #{
    #   "Environments": [
    #       { "Id": "Environments-144", "Name": "MyEnvironment" }, ... 
    #   ],
    #   ...
    #}
    async def retrieve_categories(self):
        resource = 'progression/{:s}'.format(self.id)
        progression = await self.session.get_resource_at_once_as_json(resource)
        for environment_json_dict in progression['Environments']:
            yield Category('OctopusDeploy', self._task_name(environment_json_dict))

    #{
    #    "Items": [
    #        {
    #            "Id": "Releases-27318",
    #            "Version": "1.0.1",
    #            ...
    #            "Links": { "Deployments": "/api/releases/Releases-27318/deployments{?skip}", ... }
    #        },
    #        ...
    #    ],
    #    ...
    #    "Links": { ... }
    #}
    async def retrieve_tasks_since_timestamp(self, since_timestamp):
        async for deployment_json_dict in self._paginated_deployments():
            if (parser.parse(deployment_json_dict['Created']) > since_timestamp):
                environment_json_dict = await self._environment_related_to_deployment(deployment_json_dict)
                task_json_dict = await self._task_related_to_deployment(deployment_json_dict)
                task = OctopusDeployTask(self._task_name(environment_json_dict), task_json_dict)
                if (task.is_completed):
                    yield task

    def _task_name(self, environment_json_dict):
        return '{:s}-{:s}'.format(self.slug, environment_json_dict['Name'].lower())

    #{
    #    "Items": [
    #        {
    #            "Id": "Deployments-99654",
    #            "Name": "My deployment description",
    #            "Created": "2017-06-12T13:03:17.720+00:00",
    #            ...
    #            "Links": { "Task": "/api/tasks/ServerTasks-156597", "Environment": "/api/environments/Environments-111", ... }
    #        },
    #        ...
    #    ],
    #    ...
    #    "Links": { ... }
    #}
    async def _paginated_deployments(self):
        resource_factory = lambda skip, limit: 'deployments?projects={:s}&skip={:d}&take={:d}'.format(self.id, skip, limit)
        result_key = 'Items'
        async for deployment_json_dict in self.session.get_resource_paginated_as_json(resource_factory, result_key):
            yield deployment_json_dict

    #{ "Id": "Environments-111", "Name": "MyEnvironment", ... }
    async def _environment_related_to_deployment(self, deployment_json_dict):
        return await self.session.get_url_at_once_as_json(deployment_json_dict['Links']['Environment'])

    #{
    #    "Id": "ServerTasks-156597",
    #    "IsCompleted": true,
    #    "State": "Success",
    #    "StartTime": "2017-06-12T13:03:18.345+00:00",
    #    "CompletedTime": "2017-06-12T13:03:51.923+00:00",
    #    ...
    #    "Links": { ... }
    #}
    async def _task_related_to_deployment(self, deployment_json_dict):
        return await self.session.get_url_at_once_as_json(deployment_json_dict['Links']['Task'])