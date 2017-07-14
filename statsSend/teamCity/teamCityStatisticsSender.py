#!/usr/bin/env python3

import asyncio

from dateutil import parser

from statsSend.teamCity.teamCityConnection import TeamCityConnection
from statsSend.teamCity.teamCityUrlBuilder import TeamCityUrlBuilder
from statsSend.teamCity.teamCityProject import TeamCityProject

class TeamCityStatisticsSender:
    def __init__(self, cfg, reporter):
        self.page_size = int(cfg['page_size'])
        connection = TeamCityConnection(cfg['user'], cfg['password'])
        url_builder = TeamCityUrlBuilder(cfg['server_url'], cfg['api_url_prefix'])
        self.project = TeamCityProject(cfg['project_id'], connection, url_builder, self.page_size)
        self.since_timestamp = parser.parse(cfg['since_timestamp']).strftime('%Y%m%dT%H%M%S%z')
        self.reporter = reporter

    def send_categories(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._send_categories())
        loop.close()

    def send_values(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._send_values())
        loop.close()

    async def _send_categories(self):
        categories = [build_configuration.toCategory() async for build_configuration in self.project.retrieve_build_configurations()]
        self.reporter.report_categories(categories)

    async def _send_values(self):
        async for build_configuration in self.project.retrieve_build_configurations():
            async for build_run in build_configuration.retrieve_build_runs_since_timestamp(self.since_timestamp):
                job = build_run.toJob()
                job.report(self.reporter)