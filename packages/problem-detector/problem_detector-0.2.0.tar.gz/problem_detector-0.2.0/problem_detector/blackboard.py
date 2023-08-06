class BlackBoard(object):

    __instance = None

    @staticmethod
    def get_instance():
        if BlackBoard.__instance is None:
            BlackBoard.__instance = BlackBoard()
        return BlackBoard.__instance

    def __init__(self):
        if BlackBoard.__instance is not None:
            raise Exception('BlackBoard class instance should be created only once')
        else:
            BlackBoard.__instance = self

    def add_attr(self, attr, value):
        setattr(self, attr, value)

    def get_attr(self):
        return vars(self)

