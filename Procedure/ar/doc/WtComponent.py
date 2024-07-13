import abc


class WtComponent:
    def __init__(self, t, id, doc):
        """
        :type id: str
        :type id: str
        :type doc: WtDocument
        """
        self.t = t
        self.id = id
        self.doc = doc

    @abc.abstractmethod
    def render(self):
        """
        用于编写，渲染组件所需要的变量
        :return: dict
        """
        pass

    def get_input(self):
        """
        可以获取三部分数据，样本信息，变异位点信息，自定义信息
        :return:
        """
        return self.doc.get_input()

    def get_table(self, db_name, table_name):
        """
        可以获取数据库信息，结构和excel保持一致，
        :param db_name: excel名称，可能是简写
        :param table_name: sheet名称
        :return: 返回table实例
        """
        return self.doc.get_table(db_name, table_name)

    def get_type(self):
        """
        组件类型
        :return:
        """
        return self.t

    def get_id(self):
        """
        组件id
        :return:
        """
        return self.id

