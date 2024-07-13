import abc

import xlrd
import re


class WtVariantInfoLoader():
    def __init__(self):
        self.data = []

    def get(self, code):
        return {
            'variant': self.data,
        }

    def enumerate(self):
        for item in self.data:
            yield {'variant': item}

    @abc.abstractmethod
    def load(self, file, loader_config):
        pass


class WtVariantSubLoader():
    @abc.abstractmethod
    def load(self, xlsx):
        pass