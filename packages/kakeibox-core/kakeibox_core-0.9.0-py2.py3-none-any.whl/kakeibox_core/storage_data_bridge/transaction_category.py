class TransactionCategoryBridge(object):

    def __init__(self, storage_bridge):
        self.bridge = storage_bridge.transaction_category_data_bridge

    def list(self):
        try:
            return self.bridge.list()
        except Exception as e:
            raise

    def new(self, transaction_category):
        result = self.bridge.new(transaction_category)
        if not result:
            raise Exception("An error occurred creating a new "
                            "TransactionCategory ")
        return result

    def delete(self, transaction_category_code):
        result = self.bridge.delete(transaction_category_code)
        if not result:
            raise Exception(
                "An error occurred deleting a "
                "TransactionCategory with code".format(
                    transaction_category_code))
        return result

    def get_by_code(self, transaction_category_code):
        result = self.bridge.get_by_code(transaction_category_code)
        if not result:
            raise Exception(
                "TransactionCategory with code {} doesn't exists".format(
                    transaction_category_code))
        return result

    def update(self, code, transaction_category):
        result = self.bridge.update(code, transaction_category)
        if not result:
            raise Exception("An error occurred creating a new "
                            "TransactionCategory ")
        return result
