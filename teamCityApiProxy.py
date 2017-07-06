#!/usr/bin/env python3

import requests

from requests.auth import HTTPBasicAuth

class TeamCityApiProxy:
    def __init__(self, user, password, server_url, api_url_prefix):
        self.server_url = server_url
        self.api_url_prefix = api_url_prefix
        self.basic_auth_credentials = HTTPBasicAuth(user, password)
        self.headers = { 'Accept': 'application/json' }

    def full_url_from_hypermedia_link(self, link_url):
        return self.server_url + link_url

    def full_url_from_resource_url(self, resource_url):
        return self.server_url + self.api_url_prefix + resource_url

    def get_resource(self, url):
        return requests.get(url, headers = self.headers, auth = self.basic_auth_credentials)