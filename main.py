#!/usr/bin/env python3

import asyncio

from configuration.settings import Settings
from reporting.shellReporter import ShellReporter
from reporting.zabbixReporter import ZabbixReporter
from statsSend.teamCity.teamCityStatisticsSender import TeamCityStatisticsSender
from statsSend.jenkins.jenkinsStatisticsSender import JenkinsStatisticsSender
from statsSend.octopusDeploy.octopusDeployStatisticsSender import OctopusDeployStatisticsSender
from statsSend.urbanCodeDeploy.urbanCodeDeployStatisticsSender import UrbanCodeDeployStatisticsSender

class Main:
    reporter_factories = {
        (lambda x: not x.is_enabled('Zabbix')): (lambda x: ShellReporter()),
        (lambda x: x.is_enabled('Zabbix')): (lambda x: ZabbixReporter(x.section('Zabbix')))
    }

    stats_sender_factories = {
        (lambda x: x.is_enabled('TeamCity')): (lambda x, reporter: TeamCityStatisticsSender(x.section('TeamCity'), reporter)),
        (lambda x: x.is_enabled('Jenkins')): (lambda x, reporter: JenkinsStatisticsSender(x.section('Jenkins'), reporter)),
        (lambda x: x.is_enabled('OctopusDeploy')): (lambda x, reporter: OctopusDeployStatisticsSender(x.section('OctopusDeploy'), reporter)),
        (lambda x: x.is_enabled('UrbanCodeDeploy')): (lambda x, reporter: UrbanCodeDeployStatisticsSender(x.section('UrbanCodeDeploy'), reporter))
    }

    def __init__(self):
        self.settings = Settings()
        self._create_stats_senders()

    def send_stats(self):
        loop = asyncio.get_event_loop()
        to_future_send = lambda sender: asyncio.ensure_future(sender.send())
        future_send_list = list(map(to_future_send, self.statisticsSenders))
        loop.run_until_complete(asyncio.gather(*future_send_list))
        loop.close()

    def _create_stats_senders(self):
        self.statisticsSenders = []
        reporter = self._create_reporter()
        for key, value in self.stats_sender_factories.items():
            if key(self.settings):
                self.statisticsSenders.append(value(self.settings, reporter))

    def _create_reporter(self):
        for key, value in self.reporter_factories.items():
            if key(self.settings):
                return value(self.settings)


Main().send_stats()