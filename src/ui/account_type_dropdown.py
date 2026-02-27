# A custom Qt widget for account dropdown

from PyQt6.QtWidgets import QComboBox
from models.models import AccountType


class AccountTypeDropdown(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.populate_account_types()
        return

    def populate_account_types(self):
        """
        Description

        :param None:
        :return None:
        """
        self.clear()
        account_types = [atype for atype in AccountType]
        account_types.sort(key=lambda atype: atype.name)
        # Add empty option
        self.addItem("", None)
        for atype in account_types:
            display_text = atype.name
            self.addItem(display_text, atype)
        return
