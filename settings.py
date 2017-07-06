#!/usr/bin/env python3

import json
import tzlocal

from datetime import datetime, timedelta

class Settings:
    def __init__(self):
        self.configuration = self._load_configuration()
        yesterday = datetime.now(tzlocal.get_localzone()) - timedelta(days = 1)
        beginning_of_yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        self.since_timestamp = beginning_of_yesterday.isoformat()

    def is_enabled(self, key):
        return (key in self.configuration) and self.configuration[key]['enabled']

    def section(self, key):
        section = self.configuration[key]
        since_timestamp_key = 'since_timestamp'
        if since_timestamp_key not in section:
            section[since_timestamp_key] = self.since_timestamp
        return section

    def _load_configuration(self):
        with open('settings.json') as configuration:
            return json.load(configuration)