import abc

from ar.doc.WtComponent import WtComponent


class WtRenderGlobalComponent(WtComponent):
    @abc.abstractmethod
    def render(self):
        pass