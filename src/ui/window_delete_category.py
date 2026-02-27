# New transaction dialog

from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from models.models import Category
from repositories.category_repository import CategoryRepository
from ui.category_dropdown import CategoryDropdown


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
        self.setWindowTitle("Delete Category")
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
        self.category = CategoryDropdown(self.category_repository)
        # Buttons
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete)
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
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.category)

        # Row 2
        row2.addWidget(self.btn_delete)
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

    def delete(self):
        """
        Description

        :param None:
        :return None:
        """

        category_id = self.category.currentData()

        if category_id is None:
            QMessageBox.warning(self, "Input Error", "Please provide category.")
            return
        else:
            print(f"Deleting category with ID: {category_id}")

        self.value = category_id
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
