# New transaction dialog

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDateEdit,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from models.models import Transaction
from repositories.account_repository import AccountRepository
from repositories.category_repository import CategoryRepository
from services.transaction_factory import TransactionService
from ui.account_dropdown import AccountDropdown
from ui.category_dropdown import CategoryDropdown


class NewTransactionDialog(QDialog):

    def __init__(
        self,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
    ):
        super().__init__()
        self.account_repository = account_repository
        self.category_repository = category_repository
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
        self.setWindowTitle("Add New Transaction")
        self.setGeometry(850, 350, 400, 200)
        return

    def init_ui(self):
        """
        Description

        :param None:
        :return None:
        """
        # Create all objects

        # Date
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        # Amount
        self.amount = QLineEdit()
        # Description
        self.description = QLineEdit()
        # Categories
        self.category_dropdown = CategoryDropdown(self.category_repository)
        # Accounts
        self.account_dropdown = AccountDropdown(self.account_repository)
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
        row3 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Account"))
        row1.addWidget(self.account_dropdown)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.category_dropdown)

        # Row 2
        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        # Row 3
        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_cancel)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
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
        date = self.date_box.date().toPyDate()
        description = self.description.text()
        amount = self.amount.text()
        category = self.category_dropdown.currentText()

        # Get account info from dropdown
        account = self.account_dropdown.currentText()
        account = account.split("(")

        if not description or not amount:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please provide both description and amount.",
            )
            return
        transaction: Transaction = TransactionService.create_new(
            account_id=self.account_repository.get_id_by_name(account[0]),
            transaction_date=date,
            amount=float(amount),
            source="manual",
            description=description,
            category_id=self.category_repository.get_id_by_name(category),
        )
        self.value = transaction
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
