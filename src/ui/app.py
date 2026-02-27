# App design
# doc.qt.io

from PyQt6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QLineEdit, QDateEdit,
    QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem,
    QHeaderView)
from PyQt6.QtCore import QDate
from sqlite3 import Connection

from ui.account_dropdown import AccountDropdown
from ui.category_dropdown import CategoryDropdown
from csv.csv_importer import get_transactions_from_csv
from repositories.account_repository import AccountRepository
from repositories.category_repository import CategoryRepository
from repositories.transaction_repository import TransactionRepository
from models.models import Transaction


class TransactionApp(QWidget):

    def __init__(self, connection: Connection):
        super().__init__()
        self.account_repository = AccountRepository(connection)
        self.category_repository = CategoryRepository(connection)
        self.transaction_repository = TransactionRepository(connection)
        self.settings()
        self.init_ui()
        self.load_transactions()
        return

    def settings(self) -> None:
        """
        Description

        :param None:
        :return None:
        """
        self.setWindowTitle("Finances App")
        self.setGeometry(800, 300, 1200, 500)
        return

    def init_ui(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        # Create all objects

        # Filter button
        self.btn_filter = QPushButton("Filter Transactions")
        self.btn_filter.clicked.connect(self.load_transactions)
        # Filter Dates
        self.start_date_box = QDateEdit()
        self.start_date_box.setDate(QDate.currentDate())
        self.end_date_box = QDateEdit()
        self.end_date_box.setDate(QDate.currentDate())
        # Filter Amounts
        self.minimum_amount = QLineEdit()
        self.maximum_amount = QLineEdit()
        # Filter Description
        self.description = QLineEdit()
        # Filter Category
        self.category_dropdown = CategoryDropdown(self.category_repository)
        # Account
        self.account_dropdown = AccountDropdown(self.account_repository)

        # Add Transaction button
        self.btn_add = QPushButton("Add Transaction")
        self.btn_add.clicked.connect(self.add_transaction)
        # Delete Transaction button
        self.btn_delete = QPushButton("Delete Transaction")
        self.btn_delete.clicked.connect(self.delete_transaction)
        self.btn_delete.setObjectName("btn_delete")
        # Import CSV button
        self.btn_import_csv = QPushButton("Import CSV")
        self.btn_import_csv.clicked.connect(self.import_csv)
        # Add Account button
        self.btn_add_account = QPushButton("Add Account")
        self.btn_add_account.clicked.connect(self.add_account)
        # Add Category button
        self.btn_add_category = QPushButton("Add Category")
        self.btn_add_category.clicked.connect(self.add_category)

        # Table
        table_headers = ["Transaction Date", "Post Date",
                         "Description", "Comment",
                         "Amount", "Category", "Account",
                         "Receipt Verified", "Statement Verified"]
        self.table = QTableWidget(0, len(table_headers))
        self.table.setHorizontalHeaderLabels(table_headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Layout and styles
        self.setup_layout()
        self.apply_styles()
        return

    def setup_layout(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel("Start Date"))
        row1.addWidget(self.start_date_box)
        row1.addWidget(QLabel("End Date"))
        row1.addWidget(self.end_date_box)
        row1.addWidget(QLabel("Account"))
        row1.addWidget(self.account_dropdown)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.category_dropdown)

        # Row 2
        row2.addWidget(QLabel("Minimum Amount"))
        row2.addWidget(self.minimum_amount)
        row2.addWidget(QLabel("Maximum Amount"))
        row2.addWidget(self.maximum_amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        # Row 3
        row3.addWidget(self.btn_filter)
        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)
        row3.addWidget(self.btn_import_csv)
        row3.addWidget(self.btn_add_account)
        row3.addWidget(self.btn_add_category)

        # Row 4
        row4.addWidget(self.table)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addLayout(row4)
        self.setLayout(master)
        return

    def apply_styles(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        with open("src\\ui\\style.qss", "r") as f:
            _style = f.read()
            self.setStyleSheet(_style)
        return

    def load_transactions(self, transactions: list[Transaction] = None) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        self.table.setRowCount(0)
        if transactions is None:
            transactions = self.transaction_repository.list_all()
        for row_idx, transaction in enumerate(transactions):
            self.table.insertRow(row_idx)
            # for column_idx, data in enumerate(transaction):
            for column_idx in range(transaction.count()):
                data = transaction.value(column_idx)
                # Format amount column as currency
                if column_idx.fieldname() == "amount":
                    data = float(data)
                    if data < 0:
                        formatted_data = f"-${abs(data):.2f}"
                    else:
                        formatted_data = f"${abs(data):.2f}"
                    self.table.setItem(row_idx, column_idx,
                                       QTableWidgetItem(formatted_data))
                else:
                    self.table.setItem(row_idx, column_idx,
                                       QTableWidgetItem(str(data)))
        return

    def add_transaction(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        from ui.new_transaction import NewTransactionDialog

        new_transaction_dialog = NewTransactionDialog(
            self.account_repository, self.category_repository)
        if new_transaction_dialog.exec() == QDialog.DialogCode.Rejected:
            return
        if not self.transaction_repository.add(new_transaction_dialog.value):
            QMessageBox.critical(self, "Database Error",
                                 "Failed to add transaction.")
            return
        self.load_transactions()
        return

    def delete_transaction(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Selection Error",
                "Please select one or more transactions to delete.")
            return
        # Get unique row indices from selected items
        selected_rows = set(self.table.row(item) for item in selected_items)
        # Reverse order to avoid index shifting
        for row in sorted(selected_rows, reverse=True):
            transaction_id = int(self.table.item(row, column.ID).text())
            n_items_selected = "" if len(
                selected_items) == 0 else len(selected_items)
            confirm = QMessageBox.question(self, "Confirm Deletion",
                                           f"Are you sure you want to delete {n_items_selected} transaction?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                if not self.transaction_repository.delete(transaction_id):
                    QMessageBox.critical(
                        self, "Database Error",
                        "Failed to delete transaction ID {transaction_id}.")
                    return
                self.load_transactions()
        return

    def import_csv(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if not file_path:
            return  # User cancelled the dialog

        transactions = get_transactions_from_csv(file_path)
        for transaction in transactions:
            if not self.transaction_repository.add(transaction):
                QMessageBox.critical(
                    self, "Import Error",
                    "Failed to import transactions from CSV.")
                return

        # if not add_transactions_from_csv(file_path):

        self.load_transactions()

        QMessageBox.information(
            self, "Import Successful",
            "Transactions imported successfully from CSV.")
        return

    def add_account(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        from ui.new_account import NewAccountDialog

        new_account_dialog = NewAccountDialog()
        if new_account_dialog.exec() == QDialog.DialogCode.Rejected:
            return
        if not self.account_repository.add(new_account_dialog.value):
            QMessageBox.critical(self, "Database Error",
                                 "Failed to add account.")
            return
        # Refresh account dropdown
        self.account_dropdown.populate_accounts()
        return

    def add_category(self) -> None:
        """
        Description

        :param self: The instance of the application.
        :return None:
        """
        from ui.new_category import NewCategoryDialog

        new_category_dialog = NewCategoryDialog(self.category_repository)
        if new_category_dialog.exec() == QDialog.DialogCode.Rejected:
            return
        if not self.category_repository.add(new_category_dialog.value):
            QMessageBox.critical(self, "Database Error",
                                 "Failed to add category.")
            return
        # Refresh category dropdown
        self.category_dropdown.populate_categories()
        return
