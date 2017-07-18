#!/usr/bin/env python3

from dateutil import parser

from statsSend.utils import print_exception
from statsSend.urlBuilder import UrlBuilder
from statsSend.teamCity.teamCityConnection import TeamCityConnection
from statsSend.teamCity.teamCityProject import TeamCityProject

class TeamCityStatisticsSender:
    def __init__(self, settings, reporter):
        self.page_size = int(settings['page_size'])
        connection = TeamCityConnection(settings['user'], settings['password'])
        url_builder = UrlBuilder(settings['server_url'], settings['api_url_prefix'])
        self.project = TeamCityProject(settings['project_id'], connection, url_builder, self.page_size)
        self.since_timestamp = parser.parse(settings['since_timestamp']).strftime('%Y%m%dT%H%M%S%z')
        self.reporter = reporter

    async def send(self):
        if ("report_categories" in dir(self.reporter)):
            try:
                categories = [build_configuration.toCategory() async for build_configuration in self.project.retrieve_build_configurations()]
                self.reporter.report_categories(categories)
            except Exception as err:
                print_exception('Error sending categories')

        try:
            async for build_configuration in self.project.retrieve_build_configurations():
                async for build_run in build_configuration.retrieve_build_runs_since_timestamp(self.since_timestamp):
                    try:
                        job = build_run.toJob()
                        self.reporter.report_job(job)
                    except Exception as err:
                        print_exception('Error reporting job')
        except Exception as err:
            print_exception('Error reporting jobs')