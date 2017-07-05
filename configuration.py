#!/usr/bin/env python

import json
import tzlocal

from datetime import datetime, timedelta

class Configuration:
    def __init__(self):
        self.settings = self._load_settings()
        yesterday = datetime.now(tzlocal.get_localzone()) - timedelta(days = 1)
        beginning_of_yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        self.since_timestamp = beginning_of_yesterday.isoformat()

    def is_enabled(self, key):
        return (key in self.settings) and self.settings[key]['enabled']

    def section(self, key):
        section = self.settings[key]
        since_timestamp_key = 'since_timestamp'
        if since_timestamp_key not in section:
            section[since_timestamp_key] = self.since_timestamp
        return section

    def _load_settings(self):
        with open('settings.json') as settings:    
            return json.load(settings)