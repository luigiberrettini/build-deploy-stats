#!/usr/bin/env python3

import aiohttp

class TeamCityConnection:
    def __init__(self, user, password):
        self.basic_auth_credentials = aiohttp.BasicAuth(login = user, password = password)
        self.headers = { 'Accept': 'application/json' }
        
    def get_session(self):
        return aiohttp.ClientSession(auth = self.basic_auth_credentials, headers = self.headers)