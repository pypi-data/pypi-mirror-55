class Model(object):
    file = None
    data = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.data[key] = value
