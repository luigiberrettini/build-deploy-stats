#!/usr/bin/env python3

class UrlBuilder:
    def __init__(self, server_url, api_url_prefix, page_size):
        self.server_url = server_url
        self.api_url_prefix = api_url_prefix
        self.page_size = page_size
        
    def relative_url_from_resource(self, resource):
        return self.api_url_prefix + resource

    def absolute_url_from_relative(self, relative_url):
        url = self.server_url + relative_url.strip('/')
        return url.format(self.page_size)

    def absolute_url_from_relative_factory(self, relative_url_factory):
        return self.server_url + relative_url_factory(self.page_size).strip('/')