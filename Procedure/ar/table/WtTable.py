import abc

"""
数据库表，对应一个sheet
"""


class WtTable:
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self, mode=0, limit=0):
        """
        获取table中的数据
        :param mode: int 报告类型
        :param limit: int 最大的返回条数
        :return: list
        """
        pass

    @abc.abstractmethod
    def first(self, mode=0):
        pass




