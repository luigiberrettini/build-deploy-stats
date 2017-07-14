#!/usr/bin/env python3

class TeamCityUrlBuilder:
    def __init__(self, server_url, api_url_prefix):
        self.server_url = server_url
        self.api_url_prefix = api_url_prefix
        
    def full_url_from_hypermedia_link(self, link_url):
        return self.server_url + link_url

    def full_url_from_resource_url(self, resource_url):
        return self.server_url + self.api_url_prefix + resource_url