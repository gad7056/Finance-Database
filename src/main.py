# Running the app

from database.connection import get_connection
from database.schema import initialize_schema
from ui.app import TransactionApp
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys


def main():

    # Create application
    app = QApplication(sys.argv)

    # Open database
    connection = get_connection()
    if not connection:
        QMessageBox.critical(None, "Database Error",
                             "Unable to establish a database connection.")
        sys.exit(1)
    else:
        initialize_schema(connection)

    # Launch application
    window = TransactionApp(connection)
    window.show()

    sys.exit(app.exec())

    return


if __name__ == "__main__":
    main()
