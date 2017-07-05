#!/usr/bin/env python

from dateutil import parser

from teamCityApiProxy import TeamCityApiProxy
from teamCityProject import TeamCityProject

class TeamCityStatisticsSender:
    def __init__(self, cfg, reporter):
        api_proxy = TeamCityApiProxy(cfg['user'], cfg['password'], cfg['server_url'], cfg['api_url_prefix'])
        self.project = TeamCityProject(api_proxy, cfg['project_id'])
        self.since_timestamp = parser.parse(cfg['since_timestamp']).strftime('%Y%m%dT%H%M%S%z')
        self.reporter = reporter

    def send(self):
        build_configurations = self.project.retrieve_build_configurations()
        list(map(lambda x: self._send_for_build_configuration(x), build_configurations))

    def _send_for_build_configuration(self, build_configuration):
        jobs = build_configuration.retrieve_jobs_since_timestamp(self.since_timestamp)
        list(map(lambda x: x.report(self.reporter), jobs))