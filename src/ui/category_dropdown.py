# A custom Qt widget for category dropdown

# from PyQt6.QtWidgets import QComboBox
from models.models import Category
from repositories.category_repository import CategoryRepository
from ui.group_combo_box import GroupComboBox


class CategoryDropdown(GroupComboBox):

    def __init__(self, category_repository: CategoryRepository, parent=None):
        super().__init__(parent)
        self.category_repository = category_repository
        self.populate_categories()
        return

    def populate_categories(self):
        """
        Description

        :param None:
        :return None:
        """
        self.clear()
        # Add empty option to the beginning
        self.addChild(" ")
        parents = self.category_repository.list_parent_categories()
        for parent in parents:
            children = self.category_repository.list_children_of(parent.id)
            # do not add parent category as group if it has no children
            if not children:
                continue
            group = self.addGroup(parent.name)
            for child in children:
                group.addChild(child.name, child.id)
        return

    def populate_parent_categories(self):
        """
        Description

        :param None:
        :return None:
        """
        # TODO: forcing the caller to call this method after instantiating the
        # object is unintuitive and bad design but works for now
        self.clear()
        categories = self.category_repository.list_parent_categories()
        print(categories)
        # Add empty option to the beginning
        categories.insert(0, Category(id=None, name="", parent_id=None))
        for category in categories:
            self.addItem(category.name, category.id)
        return
