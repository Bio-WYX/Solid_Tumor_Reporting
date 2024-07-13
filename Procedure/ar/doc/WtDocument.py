import traceback

from ar.common.WtArError import WtArError
from ar.common.singleton import singleton
from ar.config import initial
from ar.db.WtDatabaseInstance import db
from ar.doc.WtComponentFactory import WtComponentFactory
from ar.doc.WtRenderEvent import WtRenderEvent

"""
文档信息，用于渲染报告模板
和docx文档对应
文档中可以包含多个组件
"""


@singleton
class WtDocument:
    def __init__(self, event_type=WtRenderEvent):
        self.input_info = None
        self.isInstance = False
        self.db = db

        # debug
        self.no_render = False
        self.render_event = event_type()

    def instance(self):
        """
        加载配置项，如果是外部自定义的组件信息，可以在代码其它位置进行注册调用
        :return:
        """
        if self.isInstance:
            return

        self.isInstance = True
        initial()

    def render_component(self, t, id):
        """
        渲染组件数据
        :param t:  string 组件类型
        :param id: string 组件id
        :return: dict 组件渲染数据
        """

        self.render_event.event_start_component(t, id)
        try:
            if self.no_render:  # 预加载模式不渲染组件，仅仅提取报告模板中的信息
                data = None
            else:
                data = self.get_component(t, id).render()
        except Exception as e:
            print("error", e)
            print(traceback.format_exc().rstrip())
            self.render_event.event_end_component(t, id, None, e)
            return None

        self.render_event.event_end_component(t, id, data)
        return data

    def get_component(self, t, id):
        """
        获取组件实例
        :param t: string   组件类型
        :param id: string  组件id
        :return: WtComponent  组件对象
        """
        c = WtComponentFactory().make(t, id, self)
        if not c:
            raise WtArError('无法实例化类型为{}的组件'.format(t))

        return c

    def get_input(self):
        """
        获取输入信息
        :return: WtInputInfo
        """
        return self.input_info

    def get_table(self, category, sub):
        """
        获取数据库表格数据
        :param category: string 对应excel
        :param sub: string 对应sheet
        :return: WtTable 表实例
        """
        return self.db.get_table(category, sub)

    def get_event_data(self):
        """
        获取事件监控收集的数据
        :return: list
        """
        return self.render_event.get_event_data()

    def render(self, output_path, input_info,
               custom_render_data=None, global_component_type=None, no_render=False, tpl=None):
        """
        docx渲染方法
        :param global_component_type:
        :param tpl: 报告模板对象
        :param output_path: string  报告生成路径
        :param input_info: WtInputInfo 输入信息对象
        :param custom_render_data: dict 兼容原来的报告，部分参数可能无法组件化，需要传递额外字段
        :param no_render: bool 为True时不会生成正确，仅仅获取报告模板中的信息
        """
        self.no_render = no_render
        self.render_event.event_start_document()

        self.input_info = input_info

        render_data = {'get': self.render_component}

        if custom_render_data:
            render_data.update(custom_render_data)

        if global_component_type:
            self.render_event.event_start_component('global', 'global')
            if self.no_render:
                render_data['g'] = None
            else:
                render_data['g'] = global_component_type('global', 'global', self).render()
            self.render_event.event_end_component('global', 'global', render_data['g'])
        else:
            render_data['g'] = None

        tpl.render(render_data)
        tpl.save(output_path)

        self.render_event.event_end_document()

        self.input_info = None

