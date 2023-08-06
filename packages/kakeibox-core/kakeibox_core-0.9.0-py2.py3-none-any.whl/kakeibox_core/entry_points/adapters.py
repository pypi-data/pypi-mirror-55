from dependency_injector import containers, providers
from kakeibox_storage_sqlite3.bridge import Bridge
from kakeibox_storage_memory.bridge import Bridge as TestBridge


class Adapters(containers.DeclarativeContainer):
    storage_bridge = providers.Factory(Bridge)


class TestAdapters(containers.DeclarativeContainer):
    storage_bridge = providers.Factory(TestBridge)
