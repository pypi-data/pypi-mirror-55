class UseCaseContext(object):

    def __init__(self, strategy):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def execute(self) -> None:
        return self._strategy.do()


class UseCaseStrategy(object):

    def __init__(self, storage_bridge):
        self.storage_data_bridge = storage_bridge

    def execute(self):
        raise Exception("Not implemented yet")
