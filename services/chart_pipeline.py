"""
Chart Pipeline

Coordinates all chart calculation services.
"""


class ChartPipeline:
    def __init__(self):
        self.result = {}

    def add(self, key, value):
        self.result[key] = value

    def build(self):
        return self.result