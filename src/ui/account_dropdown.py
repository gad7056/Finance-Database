# A custom Qt widget for account dropdown

from PyQt6.QtWidgets import QComboBox

from repositories.account_repository import AccountRepository


class AccountDropdown(QComboBox):

    def __init__(self, account_repository: AccountRepository, parent=None):
        super().__init__(parent)
        self.account_repository = account_repository
        self.populate_accounts()
        return

    def populate_accounts(self):
        """
        Description

        :param None:
        :return None:
        """
        self.clear()
        accounts = self.account_repository.list_all()
        # Add empty option
        self.addItem("", None)
        for acc in accounts:
            self.addItem(acc.name, acc)
        return
