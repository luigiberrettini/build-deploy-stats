#!/usr/bin/env python3

from statsSend.octopusDeploy.octopusDeployProject import OctopusDeployProject

class OctopusDeployProjectGroup:
    def __init__(self, session, json_dict):
        self.session = session
        self.id = json_dict['Id']
        self.projects_hypermedia_link = json_dict['Links']['Projects']

    #{
    #    "Items": [
    #        {
    #            "Id": "Projects-682",
    #            "Name": "My project",
    #            "Slug": "my-project",
    #            ...
    #            "Links": { "Releases": "/api/projects/Projects-682/releases{/version}{?skip}", ... }
    #        },
    #        ...
    #    ],
    #    ...
    #    "Links": { ... }
    #}
    async def retrieve_projects(self):
        relative_url_factory = lambda skip, limit: '{:s}?skip={:d}'.format(self.projects_hypermedia_link, skip)
        result_key = 'Items'
        async for project_json_dict in self.session.get_url_paginated_as_json(relative_url_factory, result_key):
            yield OctopusDeployProject(self.session, project_json_dict)