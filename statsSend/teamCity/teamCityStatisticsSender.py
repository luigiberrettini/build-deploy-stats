#!/usr/bin/env python3

from dateutil import parser

from statsSend.session import Session
from statsSend.utils import print_exception
from statsSend.urlBuilder import UrlBuilder
from statsSend.teamCity.teamCityProject import TeamCityProject

class TeamCityStatisticsSender:
    def __init__(self, settings, reporter):
        page_size = int(settings['page_size'])
        url_builder = UrlBuilder(settings['server_url'], settings['api_url_prefix'], '', page_size)
        headers = { 'Accept': 'application/json'}
        user = settings['user']
        password = settings['password']
        self.session_factory = lambda: Session(url_builder, headers, user, password)
        self.project_id = settings['project_id']
        self.since_timestamp = parser.parse(settings['since_timestamp']).strftime('%Y%m%dT%H%M%S%z')
        self.reporter = reporter

    async def send(self):
        if ("report_categories" in dir(self.reporter)):
            async with self.session_factory() as session:
                try:
                    project = TeamCityProject(session, self.project_id)
                    categories = [build_configuration.to_category() async for build_configuration in project.retrieve_build_configurations()]
                    self.reporter.report_categories(categories)
                except Exception as err:
                    print_exception('Error sending categories')
    
        async with self.session_factory() as session:
            try:
                project = TeamCityProject(session, self.project_id)
                async for build_configuration in project.retrieve_build_configurations():
                    async for build_run in build_configuration.retrieve_build_runs_since_timestamp(self.since_timestamp):
                        try:
                            activity = build_run.to_activity()
                            self.reporter.report_activity(activity)
                        except Exception as err:
                            print_exception('Error reporting activity')
            except Exception as err:
                print_exception('Error reporting activities')