class MetaData:

    def __init__(self, **kwargs):
        self.data = kwargs

    @property
    def user(self):
        return self.data['data']['user']


class Message:
    def __init__(self, data: dict):
        self.data = data

    @property
    def message(self):
        pass

    def __repr__(self):
        # return send()
        pass
