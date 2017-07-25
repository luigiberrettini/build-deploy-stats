#!/usr/bin/env python3

class Category:
    def __init__(self, tool, name, environment = None):
        self.tool_id = tool
        self.context_id = name if (environment is None) else '{:s}-{:s}'.format(name, environment.lower())

    @property
    def tool(self):
        return self.tool_id

    @property
    def context(self):
        return self.context_id