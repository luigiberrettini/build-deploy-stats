#!/usr/bin/env python3

import fnmatch
import ijson.backends.asyncio

from statsSend.octopusDeploy.octopusDeployProjectGroup import OctopusDeployProjectGroup

class OctopusDeployProjectGroupSet:
    def __init__(self, session, project_group_filter):
        self.session = session
        self.project_group_filter = project_group_filter

    #[
    #   {
    #       "Id": "ProjectGroups-11",
    #       "Name": "PrjGrp-A",
    #       "Links": { "Projects": "/api/projectgroups/ProjectGroups-11/projects", ... }
    #   },
    #   ...
    #]
    async def items(self):
        async with self.session.get_resource('projectgroups/all') as response:
            async for project_group_json_dict in ijson.backends.asyncio.items(response.content, 'item'):
                if (fnmatch.fnmatch(project_group_json_dict['Name'], self.project_group_filter)):
                    yield OctopusDeployProjectGroup(self.session, project_group_json_dict)
                else:
                    pass