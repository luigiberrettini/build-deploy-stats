#!/usr/bin/env python3

from configuration.settings import Settings
from reporting.shellReporter import ShellReporter
from reporting.zabbixReporter import ZabbixReporter
from statsSend.teamCity.teamCityStatisticsSender import TeamCityStatisticsSender
from statsSend.jenkins.jenkinsStatisticsSender import JenkinsStatisticsSender
from statsSend.octopusDeploy.octopusDeployStatisticsSender import OctopusDeployStatisticsSender
from statsSend.urbanCodeDeploy.urbanCodeDeployStatisticsSender import UrbanCodeDeployStatisticsSender

class Main:
    reporter_factories = {
        (lambda x: not x.is_enabled('ZabbixReporter')): (lambda x: ShellReporter()),
        (lambda x: x.is_enabled('ZabbixReporter')): (lambda x: ZabbixReporter(x.section('Zabbix')['hostname'], x.section('Zabbix')['discovery_rule_key']))
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
        for sender in self.statisticsSenders:
            sender.send_categories()
            sender.send_values()

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