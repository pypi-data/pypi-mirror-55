class TransactionBridge(object):

    def __init__(self, storage_bridge):
        self.bridge = storage_bridge.transaction_data_bridge

    def list(self, start_time, end_time):
        try:
            return self.bridge.list(start_time, end_time)
        except Exception as e:
            raise

    def list_per_type(self, start_time, end_time, type):
        try:
            return self.bridge.list_per_type(start_time, end_time, type)
        except Exception as e:
            raise

    def new(self, transaction):
        result = self.bridge.new(transaction)
        if not result:
            raise Exception("An error occurred creating a new Transaction")
        return result

    def delete(self, transaction_uuid):
        result = self.bridge.delete(transaction_uuid)
        if not result:
            raise Exception(
                "An error occurred deleting a Transaction with uuid".format(
                    transaction_uuid))
        return result

    def update(self, uuid, transaction):
        result = self.bridge.update(uuid, transaction)
        if not result:
            raise Exception("An error occurred updating a Transaction")
        return result

    def get_by_uuid(self, transaction_uuid):
        result = self.bridge.get_by_uuid(transaction_uuid)
        if not result:
            raise Exception("Transaction with uuid {} doesn't "
                            "exists".format(transaction_uuid))
        return result
