#!/usr/bin/env python3

class Category:
    def __init__(self, tool, context):
        self.tool_id = tool
        self.context_id = context

    @property
    def tool(self):
        return self.tool_id

    @property
    def context(self):
        return self.context_id