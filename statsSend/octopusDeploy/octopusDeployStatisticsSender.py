#!/usr/bin/env python3

import ijson.backends.asyncio

from dateutil import parser
from statsSend.session import Session
from statsSend.utils import print_exception
from statsSend.urlBuilder import UrlBuilder
from statsSend.octopusDeploy.octopusDeployProjectGroupSet import OctopusDeployProjectGroupSet

class OctopusDeployStatisticsSender:
    def __init__(self, settings, reporter):
        page_size = 30
        url_builder = UrlBuilder(settings['server_url'], settings['api_url_prefix'], page_size)
        headers = { 'Accept': 'application/json', 'X-Octopus-ApiKey': settings['api_key'] }
        verify_ssl_certs = settings['verify_ssl_certs']
        self.session_factory = lambda: Session(url_builder, headers, verify_ssl_certs)
        self.project_group_filter = settings['project_group_filter']
        self.since_timestamp = parser.parse(settings['since_timestamp'])
        self.reporter = reporter

    async def send(self):
        if ("report_categories" in dir(self.reporter)):
            async with self.session_factory() as session:
                try:
                    project_group_set = OctopusDeployProjectGroupSet(session, self.project_group_filter)
                    categories = [cat async for cat in self._categories(project_group_set)]
                    self.reporter.report_categories(categories)
                except Exception:
                    print_exception('Error sending categories')
    
        async with self.session_factory() as session:
            try:
                project_group_set = OctopusDeployProjectGroupSet(session, self.project_group_filter)
                async for project_group in project_group_set.items():
                    async for project in project_group.retrieve_projects():
                        async for task in project.retrieve_tasks_since_timestamp(self.since_timestamp):
                            try:
                                job = task.to_job()
                                self.reporter.report_job(job)
                            except Exception:
                                print_exception('Error reporting job')
            except Exception:
                print_exception('Error reporting jobs')

    async def _categories(self, project_group_set):
        async for project_group in project_group_set.items():
            async for project in project_group.retrieve_projects():
                async for category in project.retrieve_categories():
                    yield category