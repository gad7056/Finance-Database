import csv
from models.models import Transaction
from datetime import datetime


def get_transactions_from_csv(file_path):
    """
    Description

    :param None:
    :return None:
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        match file_path:
            case _ if 'wealthfront' in file_path.lower():
                return handle_csv_from_wealthfront(reader)
            case _:
                return []


def handle_csv_from_wealthfront(reader):
    """
    Description

    :param None:
    :return None:
    """
    # Wealthfront Date format in CSV: "MM/DD/YYYY"

    transactions = []
    for row in reader:
        date_unformatted = datetime.strptime(
            row['Transaction date'].strip('"'), "%m/%d/%Y").date()
        transaction = Transaction(
            post_date=date_unformatted.strftime("%b-%d-%y"),
            statement_description=row['Description'].strip('"'),
            amount=float(row['Amount'].strip('"')),
            category="",
            account='Wealthfront Cash Account'
        )
        transactions.append(transaction)
    return transactions
