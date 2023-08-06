class TransactionSubcategoryBridge(object):

    def __init__(self, storage_bridge):
        self.bridge = storage_bridge.transaction_subcategory_data_bridge

    def list(self):
        try:
            return self.bridge.list()
        except Exception as e:
            raise

    def list_per_category(self, transaction_category):
        try:
            category = transaction_category
            return self.bridge.list_per_category(category)
        except Exception as e:
            raise

    def get_by_code(self, transaction_subcategory_code):
        result = self.bridge.get_by_code(transaction_subcategory_code)
        if not result:
            raise Exception(
                "TransactionSubcategory with code {} doesn't exists".format(
                    transaction_subcategory_code))
        return result

    def delete(self, transaction_subcategory_code):
        result = self.bridge.delete(transaction_subcategory_code)
        if not result:
            raise Exception(
                "An error occurred deleting a "
                "TransactionSubcategory with code".format(
                    transaction_subcategory_code))
        return result

    def new(self, transaction_subcategory):
        result = self.bridge.new(transaction_subcategory)
        if not result:
            raise Exception("An error occurred creating a new "
                            "TransactionSubcategory")
        return result

    def update(self, code, transaction_subcategory):
        result = self.bridge.update(code, transaction_subcategory)
        if not result:
            raise Exception("An error occurred creating a new "
                            "TransactionSubcategory ")
        return result
