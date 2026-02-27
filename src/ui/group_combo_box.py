# source:
# https://stackoverflow.com/questions/57437204/qcombobox-add-bold-parent-items

from PyQt6 import QtCore, QtGui, QtWidgets

GroupRole = QtCore.Qt.ItemDataRole.UserRole


class GroupDelegate(QtWidgets.QStyledItemDelegate):

    def initStyleOption(
            self, option: QtWidgets.QStyleOptionViewItem,
            index: QtCore.QModelIndex) -> None:
        """
        Initialize the style option for the item delegate.

        :param self: The instance of the delegate.
        :param option: The style option to initialize.
        :param index: The model index of the item.
        :return: None
        :rtype: None
        """
        super(GroupDelegate, self).initStyleOption(option, index)
        if not index.data(GroupRole):
            option.text = "   " + option.text

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem,
              index: QtCore.QModelIndex) -> None:
        """
        Prevent highlight for group items

        :param self: The instance of the delegate.
        :param option: The style option to initialize.
        :param index: The model index of the item.
        :return: None
        :rtype: None
        """
        if index.data(GroupRole):
            # Remove State_MouseOver and State_Selected for group items
            option2 = QtWidgets.QStyleOptionViewItem(option)
            option2.state &= ~QtWidgets.QStyle.StateFlag.State_MouseOver
            option2.state &= ~QtWidgets.QStyle.StateFlag.State_Selected
            super(GroupDelegate, self).paint(painter, option2, index)
        else:
            super(GroupDelegate, self).paint(painter, option, index)


class GroupItem(QtGui.QStandardItem):

    def __init__(self, text: str):
        super(GroupItem, self).__init__(text)
        self.setData(True, GroupRole)
        self._number_of_children = 0
        font = self.font()
        font.setBold(True)
        self.setFont(font)
        self.setFlags(self.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)

    def addChild(self, text: str, data: any) -> QtGui.QStandardItem:
        """
        Add a child item to the group.

        :param self: The instance of the group item.
        :param text: The text of the child item.
        :param data: The custom data associated with the child item.
        :type data: Any
        :return: The created child item.
        :rtype: QtGui.QStandardItem
        """
        it = QtGui.QStandardItem(text)
        it.setData(False, GroupRole)
        it.setData(data, QtCore.Qt.ItemDataRole.UserRole + 1)
        self._number_of_children += 1
        self.model().insertRow(self.row() + self._number_of_children, it)
        return it


class GroupComboBox(QtWidgets.QComboBox):

    def __init__(self, parent=None):
        super(GroupComboBox, self).__init__(parent)
        self.setModel(QtGui.QStandardItemModel(self))
        delegate = GroupDelegate(self)
        self.setItemDelegate(delegate)

    def addGroup(self, text: str) -> GroupItem:
        """
        Add a group item to the combo box.

        :param self: The instance of the combo box.
        :param text: The text of the group item.
        :return: The created group item.
        :rtype: GroupItem
        """
        it = GroupItem(text)
        self.model().appendRow(it)
        return it

    def addChild(self, text: str) -> QtGui.QStandardItem:
        """
        Add a child item to the combo box.
        :param self: The instance of the combo box.
        :param text: The text of the child item.
        :return: The created child item.
        :rtype: QtGui.QStandardItem
        """
        it = QtGui.QStandardItem(text)
        it.setData(True, GroupRole)
        self.model().appendRow(it)
        return it


class Example(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface.

        :return None: 
        """
        combo = GroupComboBox()

        combo.addChild(" ")

        group1 = combo.addGroup("group_1")
        group1.addChild("option_2", 2)
        group1.addChild("option_3", 3)

        group2 = combo.addGroup("group_2")
        group2.addChild("option_4", 4)
        group2.addChild("option_5", 5)

        combo.currentIndexChanged.connect(
            lambda: self.on_selection_changed(combo))

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(combo)

        self.resize(160, 60)

    def on_selection_changed(self, combo):
        # Retrieve custom data for the selected item
        data = combo.currentData(QtCore.Qt.ItemDataRole.UserRole + 1)
        print("Selected item data:", data)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
