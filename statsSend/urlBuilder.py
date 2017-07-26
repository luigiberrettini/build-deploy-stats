#!/usr/bin/env python3

class UrlBuilder:
    def __init__(self, server_url, api_url_prefix, api_url_suffix, page_size):
        self.server_url = server_url
        self.api_url_prefix = api_url_prefix
        self.api_url_suffix = api_url_suffix
        self.page_size = page_size

    def relative_url_from_resource(self, resource):
        return self._add_suffix(self.api_url_prefix + resource)

    def absolute_url_from_relative(self, relative_url):
        url = self.server_url + relative_url.strip('/')
        return self._add_suffix(url.format(self.page_size))

    def absolute_url_from_relative_factory(self, relative_url_factory):
        return self._add_suffix(self.server_url + relative_url_factory(self.page_size).strip('/'))

    def _add_suffix(self, url):
        splitted = url.split('?')
        before = splitted[0]
        after = '' if len(splitted) == 1 else splitted[1]
        return '{:s}{:s}?{:s}'.format(before, self.api_url_suffix, after)