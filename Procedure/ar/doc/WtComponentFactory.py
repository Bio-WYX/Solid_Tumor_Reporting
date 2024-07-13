from ar.common.singleton import singleton
"""
组件工厂模式，用于注册组件类型，只有注册过的组件才可以在模板中使用
WtComponentFactory().register(<组件类型>,<具体的组件实现类>)
"""

@singleton
class WtComponentFactory:
    def __init__(self):
        self.components_map = {}

    def register(self, t, c):
        """
        :param t: string 组件类型
        :param c: object 组件实例类
        """
        self.components_map[t] = c

    def make(self, t, id, doc):
        """
        工厂的生成方法
        :param t: 组件类型
        :param id: 组件id
        :param doc: 文档对象
        :return: 返回实例化的组件对象
        """
        if t in self.components_map:
            return self.components_map[t](t, id, doc)

        return None