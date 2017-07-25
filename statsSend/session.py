#!/usr/bin/env python3

import aiohttp
import ijson.backends.asyncio

class Session:
    def __init__(self, url_builder, headers, user = None, password = None, verify_ssl_certs = True):
        self.url_builder = url_builder
        self.headers = headers
        self.basic_auth_credentials = None if (user is None or password is None) else aiohttp.BasicAuth(login = user, password = password)
        self.verify_ssl_certs = verify_ssl_certs

    async def __aenter__(self):
        tcp_connector = None if self.verify_ssl_certs else aiohttp.TCPConnector(verify_ssl = False)
        self.session = aiohttp.ClientSession(auth = self.basic_auth_credentials, headers = self.headers, connector = tcp_connector)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    def get_resource(self, resource):
        relative_url = self.url_builder.relative_url_from_resource(resource)
        return self.get_url(relative_url)

    def get_resource_at_once_as_json(self, resource):
        relative_url = self.url_builder.relative_url_from_resource(resource)
        return self.get_url_at_once_as_json(relative_url)

    def get_resource_paginated_as_json(self, resource_factory, result_key):
        relative_url_factory = lambda skip, limit: self.url_builder.relative_url_from_resource(resource_factory(skip, limit))
        return self.get_url_paginated_as_json(relative_url_factory, result_key)

    def get_url(self, relative_url):
        return self.session.get(self.url_builder.absolute_url_from_relative(relative_url))

    async def get_url_at_once_as_json(self, relative_url):
        async with self.session.get(self.url_builder.absolute_url_from_relative(relative_url)) as response:
            return await response.json()

    async def get_url_paginated_as_json(self, relative_url_factory, result_key, page = 0):
        relative_url_lambda = lambda page_size: relative_url_factory(page * page_size, page_size)
        url = self.url_builder.absolute_url_from_relative_factory(relative_url_lambda)
        async with self.session.get(url) as response:
            count = 0
            result_selector = '{:s}{:s}item'.format(result_key, '.' if result_key else '')
            async for result in ijson.backends.asyncio.items(response.content, result_selector):
                count += 1
                yield result
            if not count:
                return
            async for result in self.get_url_paginated_as_json(relative_url_factory, result_key, page + 1):
                yield result