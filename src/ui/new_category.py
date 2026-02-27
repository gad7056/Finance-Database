# New transaction dialog

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from repositories.category_repository import CategoryRepository
from ui.category_dropdown import CategoryDropdown
from models.models import Category


class NewCategoryDialog(QDialog):

    def __init__(self, category_repository: CategoryRepository):
        super().__init__()
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
        self.setWindowTitle("Add New Category")
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
        self.parent_category = CategoryDropdown(self.category_repository)
        self.parent_category.populate_parent_categories()
        self.category = QLineEdit()
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
        row1.addWidget(QLabel("Parent"))
        row1.addWidget(self.parent_category)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.category)

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

        parent_id = self.parent_category.currentData()
        category = self.category.text()

        if not category:
            QMessageBox.warning(self, "Input Error", "Please provide category.")
            return

        if self.category_repository.category_exists(
                parent_id, category):
            QMessageBox.warning(self, "Input Error", "Category already exists.")
            return

        category: Category = Category(
            id=None, name=category, parent_id=parent_id)
        self.value = category
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
