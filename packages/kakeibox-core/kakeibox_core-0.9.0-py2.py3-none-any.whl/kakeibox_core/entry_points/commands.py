from dependency_injector import containers, providers
from kakeibox_core import use_cases
from kakeibox_core.entry_points.adapters import Adapters, TestAdapters


class Commands(containers.DeclarativeContainer):

    adapters = providers.DependenciesContainer()

    # transaction_category use cases
    new_category = providers.Factory(
        use_cases.transaction_category.new.NewTransactionCategory,
        storage_bridge=adapters.storage_bridge)

    update_category = providers.Factory(
        use_cases.transaction_category.update.UpdateTransactionCategory,
        storage_bridge=adapters.storage_bridge)

    get_category = providers.Factory(
        use_cases.transaction_category.get.TransactionCategoryByCode,
        storage_bridge=adapters.storage_bridge
    )

    list_categories = providers.Factory(
        use_cases.transaction_category.list.ListTransactionCategories,
        storage_bridge=adapters.storage_bridge
    )

    delete_category = providers.Factory(
        use_cases.transaction_category.delete.DeleteTransactionCategory,
        storage_bridge=adapters.storage_bridge)

    # transaction_subcategory use cases
    new_subcategory = providers.Factory(
        use_cases.transaction_subcategory.new.NewTransactionSubcategory,
        storage_bridge=adapters.storage_bridge)

    update_subcategory = providers.Factory(
        use_cases.transaction_subcategory.update.UpdateTransactionSubcategory,
        storage_bridge=adapters.storage_bridge)

    get_subcategory = providers.Factory(
        use_cases.transaction_subcategory.get.TransactionSubcategoryByCode,
        storage_bridge=adapters.storage_bridge
    )

    list_all_subcategories = providers.Factory(
        use_cases.transaction_subcategory.list_all.
            ListAllTransactionSubcategories,
        storage_bridge=adapters.storage_bridge
    )

    list_per_category = providers.Factory(
        use_cases.transaction_subcategory.list_per_category.
            ListTransactionSubcategoriesPerCategory,
        storage_bridge=adapters.storage_bridge
    )

    delete_subcategory = providers.Factory(
        use_cases.transaction_subcategory.delete.DeleteTransactionSubcategory,
        storage_bridge=adapters.storage_bridge)

    # transaction use cases
    list_transactions = providers.Factory(
        use_cases.transaction.list.ListTransactions,
        storage_bridge=adapters.storage_bridge)

    # saving use cases
    calculate_savings = providers.Factory(
        use_cases.saving.total.CalculateSaving,
        storage_bridge=adapters.storage_bridge)

    # income use cases
    new_income = providers.Factory(
        use_cases.income.new.NewIncome,
        storage_bridge=adapters.storage_bridge)

    update_income = providers.Factory(
        use_cases.income.update.UpdateIncome,
        storage_bridge=adapters.storage_bridge)

    get_income = providers.Factory(
        use_cases.income.get.GetIncomeByUUID,
        storage_bridge=adapters.storage_bridge
    )

    calculate_total_income = providers.Factory(
        use_cases.income.total.GetTotalIncome,
        storage_bridge=adapters.storage_bridge
    )

    delete_income = providers.Factory(
        use_cases.income.delete.DeleteIncome,
        storage_bridge=adapters.storage_bridge)

    # expense use cases
    new_expense = providers.Factory(
        use_cases.expense.new.NewExpense,
        storage_bridge=adapters.storage_bridge)

    update_expense = providers.Factory(
        use_cases.expense.update.UpdateExpense,
        storage_bridge=adapters.storage_bridge)

    get_expense = providers.Factory(
        use_cases.expense.get.GetExpenseByUUID,
        storage_bridge=adapters.storage_bridge
    )

    calculate_total_expense = providers.Factory(
        use_cases.expense.total.GetTotalExpense,
        storage_bridge=adapters.storage_bridge
    )

    delete_expense = providers.Factory(
        use_cases.expense.delete.DeleteExpense,
        storage_bridge=adapters.storage_bridge)


commands = Commands(adapters=Adapters())
