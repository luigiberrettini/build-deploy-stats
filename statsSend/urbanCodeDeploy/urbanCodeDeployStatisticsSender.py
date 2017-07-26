#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from dateutil import parser

from statsSend.session import Session
from statsSend.utils import print_exception
from statsSend.urlBuilder import UrlBuilder
from statsSend.urbanCodeDeploy.urbanCodeDeployTag import UrbanCodeDeployTag

class UrbanCodeDeployStatisticsSender:
    epoch = datetime(1970, 1, 1, tzinfo = timezone.utc)
    one_second = timedelta(seconds = 1)

    def __init__(self, settings, reporter):
        page_size = int(settings['page_size'])
        url_builder = UrlBuilder(settings['server_url'], settings['api_url_prefix'], '', page_size)
        headers = { 'Accept': 'application/json'}
        user = settings['user']
        password_or_auth_token = settings['password_or_auth_token']
        verify_ssl_certs = settings['verify_ssl_certs']
        self.session_factory = lambda: Session(url_builder, headers, user, password_or_auth_token, verify_ssl_certs)
        self.tag_name = settings['tag_name']
        self.since_posix_timestamp = (parser.parse(settings['since_timestamp']) - self.epoch) // self.one_second * 1000
        self.reporter = reporter

    async def send(self):
        if ("report_categories" in dir(self.reporter)):
            async with self.session_factory() as session:
                try:
                    tag = UrbanCodeDeployTag(session, self.tag_name)
                    categories = [cat async for cat in self._categories(tag)]
                    self.reporter.report_categories(categories)
                except Exception as err:
                    print_exception('Error sending categories')
    
        async with self.session_factory() as session:
            try:
                tag = UrbanCodeDeployTag(session, self.tag_name)
                async for app_process_request in tag.retrieve_application_process_requests_since_posix_timestamp(self.since_posix_timestamp):
                    try:
                        activity = app_process_request.to_activity()
                        self.reporter.report_activity(activity)
                    except Exception as err:
                        print_exception('Error reporting activity')
            except Exception as err:
                print_exception('Error reporting activities')


    async def _categories(self, tag):
        async for application in tag.retrieve_applications():
            async for category in application.retrieve_categories():
                yield category