#!/usr/bin/env python3

from urllib.parse import urlparse

class UrlBuilder:
    def __init__(self, server_url, api_url_prefix, api_url_suffix, page_size):
        self.server_url = server_url
        self.api_url_prefix = api_url_prefix
        self.api_url_suffix = api_url_suffix
        self.page_size = page_size

    def relative_url_from_resource(self, resource):
        return self._add_suffix(self._clean_join(self.api_url_prefix, resource))

    def absolute_url_from_relative_factory(self, url_factory):
        return self.absolute_url_from_relative(url_factory(self.page_size))

    def absolute_url_from_relative(self, url):
        prefix = self.server_url if self._is_relative(url) else ''
        return self._clean_join(prefix, url.format(self.page_size))

    def _is_relative(self, url):
        return not bool(urlparse(url).netloc)

    def _add_suffix(self, url):
        splitted = url.split('?')
        before = splitted[0]
        after = '' if len(splitted) == 1 else splitted[1]
        new_before = self._clean_join(before, self.api_url_suffix)
        return '{:s}?{:s}'.format(new_before, after)

    def _clean_join(self, a, b):
        if (a == ''):
            return b.strip('/');
        if (b == ''):
            return a.strip('/');
        return '{:s}/{:s}'.format(a.strip('/'), b.strip('/'))