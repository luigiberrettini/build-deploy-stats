#!/usr/bin/env python3

import json
import tzlocal

from datetime import datetime, timedelta
from os import path

class Settings:
    def __init__(self):
        self.settings_dict = self._load_from_file()
        yesterday = datetime.now(tzlocal.get_localzone()) - timedelta(days = 1)
        beginning_of_yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        self.since_timestamp = beginning_of_yesterday.isoformat()

    def is_enabled(self, key):
        return (key in self.settings_dict) and self.settings_dict[key]['enabled']

    def section(self, key):
        section = self.settings_dict[key]
        since_timestamp_key = 'since_timestamp'
        if since_timestamp_key not in section:
            section[since_timestamp_key] = self.since_timestamp
        return section

    def _load_from_file(self):
        settings_directory = path.dirname(path.realpath(__file__))
        settings_file = path.join(settings_directory, 'settings.json')
        with open(settings_file) as file_contents:
            return json.load(file_contents)