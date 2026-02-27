# New transaction dialog

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models.models import Account
from ui.account_type_dropdown import AccountTypeDropdown


class NewAccountDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.settings()
        self.init_ui()
        self.show()
        return

    def settings(self):
        """
        Description

        :param None:
        :return None:
        """
        self.setWindowTitle("Add New Account")
        self.setGeometry(850, 350, 400, 200)
        return

    def init_ui(self):
        """
        Description

        :param None:
        :return None:
        """
        # Create all objects

        # Account Details
        self.name = QLineEdit()
        self.institution = QLineEdit()
        self.type = AccountTypeDropdown()
        self.number = QLineEdit()
        # Buttons
        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.add)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.cancel)

        # Layout and styles
        self.setup_layout()
        self.apply_styles()
        return

    def setup_layout(self):
        """
        Description

        :param None:
        :return None:
        """
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel("Name"))
        row1.addWidget(self.name)
        row1.addWidget(QLabel("Institution"))
        row1.addWidget(self.institution)
        row1.addWidget(QLabel("Type"))
        row1.addWidget(self.type)
        row1.addWidget(QLabel("Number"))
        row1.addWidget(self.number)

        # Row 2
        row2.addWidget(self.btn_add)
        row2.addWidget(self.btn_cancel)

        master.addLayout(row1)
        master.addLayout(row2)
        self.setLayout(master)
        return

    def apply_styles(self):
        """
        Description

        :param None:
        :return None:
        """
        with open("src\\ui\\style.qss", "r") as f:
            _style = f.read()
            self.setStyleSheet(_style)
        return

    def add(self):
        """
        Description

        :param None:
        :return None:
        """
        name = self.name.text()
        institution = self.institution.text()
        type = self.type.currentData()
        number = self.number.text()

        if not name or not institution or not type or not number:
            QMessageBox.warning(self, "Input Error",
                                "Please provide all account details.")
            return
        account: Account = Account(
            id=None, name=name, institution=institution, type=type,
            number=number, is_active=True)
        self.value = account
        self.accept()
        return

    def cancel(self):
        """
        Description

        :param None:
        :return None:
        """
        self.reject()
        return
