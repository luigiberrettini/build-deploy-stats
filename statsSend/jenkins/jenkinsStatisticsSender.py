#!/usr/bin/env python3

import xml.etree.ElementTree

from datetime import datetime, timedelta, timezone
from dateutil import parser

from statsSend.session import Session
from statsSend.utils import print_exception
from statsSend.urlBuilder import UrlBuilder
from statsSend.jenkins.jenkinsJob import JenkinsJob

class JenkinsStatisticsSender:
    epoch = datetime(1970, 1, 1, tzinfo = timezone.utc)
    one_second = timedelta(seconds = 1)

    def __init__(self, settings, reporter):
        self.xml_api_url_suffix = settings['xml_api_url_suffix']
        self.json_api_url_suffix = settings['json_api_url_suffix']
        page_size = int(settings['page_size'])
        url_builder_factory = lambda suffix: UrlBuilder(settings['server_url'], '', suffix, page_size)
        headers = { 'Accept': 'application/json'}
        user = settings['user']
        password_or_auth_token = settings['password_or_auth_token']
        verify_ssl_certs = settings['verify_ssl_certs']
        self.session_factory = lambda suffix: Session(url_builder_factory(suffix), headers, user, password_or_auth_token, verify_ssl_certs)
        self.job_name = settings['job_name']
        self.since_posix_timestamp = (parser.parse(settings['since_timestamp']) - self.epoch) // self.one_second * 1000
        self.reporter = reporter

    async def send(self):
        root_job_resource = await self.retrieve_root_job_resource()

        if ("report_categories" in dir(self.reporter)):
            async with self.session_factory(self.json_api_url_suffix) as session:
                try:
                    job = JenkinsJob(session, root_job_resource)
                    categories = [job.to_category() async for job in job.retrieve_buildable_descendants()]
                    self.reporter.report_categories(categories)
                except Exception as err:
                    print_exception('Error sending categories')

        async with self.session_factory(self.json_api_url_suffix) as session:
            try:
                job = JenkinsJob(session, root_job_resource)
                async for job in job.retrieve_buildable_descendants():
                    for build in job.retrieve_builds_since_posix_timestamp(self.since_posix_timestamp):
                        try:
                            activity = build.to_activity()
                            self.reporter.report_activity(activity)
                        except Exception as err:
                            print_exception('Error reporting activity')
            except Exception as err:
                print_exception('Error reporting activities')

    async def retrieve_root_job_resource(self):
        async with self.session_factory(self.xml_api_url_suffix) as session:
            resource = "?xpath=//job[name='{:s}']/url".format(self.job_name)
            async with session.get_resource(resource) as response:
                text = await response.text()
                url_node = xml.etree.ElementTree.fromstring(text)
                return url_node.text