#!/usr/bin/env python

from configuration import Configuration
from shellReporter import ShellReporter
from zabbixReporter import ZabbixReporter
from teamCityStatisticsSender import TeamCityStatisticsSender
from jenkinsStatisticsSender import JenkinsStatisticsSender
from octopusDeployStatisticsSender import OctopusDeployStatisticsSender
from urbanCodeDeployStatisticsSender import UrbanCodeDeployStatisticsSender

class Main:
    reporter_factories = {
        (lambda cfg: not cfg.is_enabled('ZabbixReporter')): (lambda cfg: ShellReporter()),
        (lambda cfg: cfg.is_enabled('ZabbixReporter')): (lambda cfg: ZabbixReporter(cfg.section('Zabbix')['user'], cfg.section('Zabbix')['user']))
    }

    stats_sender_factories = {
        (lambda cfg: cfg.is_enabled('TeamCity')): (lambda cfg, reporter: TeamCityStatisticsSender(cfg.section('TeamCity'), reporter)),
        (lambda cfg: cfg.is_enabled('Jenkins')): (lambda cfg, reporter: JenkinsStatisticsSender(cfg.section('Jenkins'), reporter)),
        (lambda cfg: cfg.is_enabled('OctopusDeploy')): (lambda cfg, reporter: OctopusDeployStatisticsSender(cfg.section('OctopusDeploy'), reporter)),
        (lambda cfg: cfg.is_enabled('UrbanCodeDeploy')): (lambda cfg, reporter: UrbanCodeDeployStatisticsSender(cfg.section('UrbanCodeDeploy'), reporter))
    }

    def __init__(self):
        self.config = Configuration()
        self._create_stats_senders()

    def send_stats(self):
        for sender in self.statisticsSenders:
            sender.send()

    def _create_stats_senders(self):
        self.statisticsSenders = []
        reporter = self._create_reporter()
        for key, value in self.stats_sender_factories.iteritems():
            if key(self.config):
                self.statisticsSenders.append(value(self.config, reporter))

    def _create_reporter(self):
        for key, value in self.reporter_factories.iteritems():
            if key(self.config):
                return value(self.config)


sender = Main()
sender.send_stats()