import json
import abc


class WtRenderEventBase:
    def __init__(self):
        self.data = [] #用于保存事件中的数据
    
    @abc.abstractmethod
    def event_start_component(self, t, id):
        """
        事件，当渲染组件前调用
        :param t:  string 组件类型
        :param id: string 组件id
        :return: None
        """

    @abc.abstractmethod
    def event_end_component(self, t, id, value, error=None):
        """
        事件，当渲染组件完成后调用
        :param t:  string 组件类型
        :param id: string 组件id
        :param value: dict 组件渲染生成的dict数据
        :error error: 异常数据，但渲染组件失败时报的异常
        :return: None
        """

    @abc.abstractmethod
    def event_start_document(self):
        """
        事件，一个文档渲染开始时
        :return: None
        """
        
    @abc.abstractmethod
    def event_end_document(self):
        """
        事件，一个文档渲染完成时
        :return: None
        """
        
    def get_event_data(self):
        """
        获取事件中收集的数据
        :return: list
        """
        return self.data
        


class WtRenderEvent(WtRenderEventBase):
    def __init__(self):
        super().__init__()

    def event_start_component(self, t, id):
        pass

    def event_end_component(self, t, id, value, error=None):
        if error:
            print('component:\033[41m[{}]-{}\033[0m'.format(t, id))
        else:
            print('component:\033[32m[{}]-{}\033[0m'.format(t, id))

        self.data.append({
            'type': t,
            'id': id,
            'data': value,
        })

    def event_start_document(self):
        self.data = []
        
    def event_end_document(self):
        pass

    def to_file(self, path):
        with open(path, 'wb', encoding='utf8') as f:
            f.write(json.dumps(self.data))
