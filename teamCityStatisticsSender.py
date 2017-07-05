#!/usr/bin/env python

from dateutil import parser

from teamCityApiProxy import TeamCityApiProxy
from teamCityProject import TeamCityProject

class TeamCityStatisticsSender:
    def __init__(self, cfg, reporter):
        self.page_size = int(cfg['page_size'])
        api_proxy = TeamCityApiProxy(cfg['user'], cfg['password'], cfg['server_url'], cfg['api_url_prefix'])
        self.project = TeamCityProject(api_proxy, cfg['project_id'])
        self.since_timestamp = parser.parse(cfg['since_timestamp']).strftime('%Y%m%dT%H%M%S%z')
        self.reporter = reporter

    def send(self):
        self._send_all_project_stats()

    def _send_all_project_stats(self):
        i = 0
        while self._send_subset_of_project_stats(i * self.page_size, self.page_size):
            i += 1

    def _send_subset_of_project_stats(self, skip, limit):
        build_configurations = self.project.retrieve_build_configurations(skip, limit)
        list(map(lambda x: self._send_all_build_configuration_stats(x), build_configurations))
        return len(build_configurations)

    def _send_all_build_configuration_stats(self, build_configuration):
        i = 0
        while self._send_subset_of_build_configuration_stats(build_configuration, i * self.page_size, self.page_size):
            i += 1

    def _send_subset_of_build_configuration_stats(self, build_configuration, skip, limit):
        jobs = build_configuration.retrieve_jobs_since_timestamp(self.since_timestamp, skip, limit)
        list(map(lambda x: x.report(self.reporter), jobs))
        return len(jobs)