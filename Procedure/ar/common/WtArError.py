#异常类

class WtArError(RuntimeError):
    def __init__(self, arg):
        if type(arg) == str:
            arg = [arg]
        self.args = arg
