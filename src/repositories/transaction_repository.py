# repositories/transaction_repository.py

from datetime import date, datetime
from typing import Optional
from database.connection import get_connection
from models.models import Transaction
from sqlite3 import Connection


class TransactionRepository:

    # ----------------------------
    # Initialize
    #  ----------------------------
    def __init__(self, connection: Connection):
        self.connection = connection

    # ----------------------------
    # Create
    # ----------------------------
    def add(self, tx: Transaction) -> int:
        """
        Adds a new transaction to the database.

        :param self: The instance of the repository.
        :param tx: The transaction to add.
        :type tx: Transaction
        :return: The ID of the newly added transaction.
        :rtype: int
        """
        with self.connection as conn:
            cursor = conn.execute("""
                INSERT INTO transactions (
                    account_id,
                    date_added,
                    date_modified,
                    source,
                    transaction_date,
                    post_date,
                    description,
                    amount,
                    category_id,
                    verified_receipt,
                    verified_statement,
                    comment
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tx.account_id,
                tx.date_added.isoformat(),
                tx.date_modified.isoformat(),
                tx.source,
                tx.transaction_date.isoformat(),
                tx.post_date.isoformat() if tx.post_date else None,
                tx.description,
                tx.amount,
                tx.category_id,
                int(tx.verified_receipt),
                int(tx.verified_statement),
                tx.comment
            ))
        return cursor.lastrowid

    # ----------------------------
    # Read
    # ----------------------------
    def get_by_id(self, tx_id: int) -> Transaction | None:
        """
        Retrieves a transaction by its ID.

        :param self: The instance of the repository.
        :param tx_id: The ID of the transaction to retrieve.
        :type tx_id: int
        :return: The transaction with the specified ID, or None if not found.
        :rtype: Transaction | None
        """
        with self.connection as conn:
            row = conn.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (tx_id,)
            ).fetchone()

        if not row:
            return None

        return Transaction(
            id=row["id"],
            account_id=row["account_id"],
            date_added=datetime.fromisoformat(row["date_added"]),
            date_modified=datetime.fromisoformat(row["date_modified"]),
            source=row["source"],
            transaction_date=date.fromisoformat(row["transaction_date"]),
            amount=row["amount"],
            post_date=date.fromisoformat(row["post_date"])
            if row["post_date"] else None, description=row["description"],
            category_id=row["category_id"],
            verified_receipt=bool(row["verified_receipt"]),
            verified_statement=bool(row["verified_statement"]),
            comment=row["comment"]
        )

    def list_all(self) -> list[Transaction]:
        """
        Retrieves all transactions from the database.

        :param self: The instance of the repository.
        :return: A list of all transactions.
        :rtype: list[Transaction]
        """
        with self.connection as conn:
            rows = conn.execute(
                "SELECT * FROM transactions ORDER BY transaction_date DESC"
            ).fetchall()

        return [
            Transaction(
                id=row["id"],
                account_id=row["account_id"],
                date_added=datetime.fromisoformat(row["date_added"]),
                date_modified=datetime.fromisoformat(row["date_modified"]),
                source=row["source"],
                transaction_date=date.fromisoformat(row["transaction_date"]),
                amount=row["amount"],
                post_date=date.fromisoformat(
                    row["post_date"]) if row["post_date"] else None,
                description=row["description"],
                category_id=row["category_id"],
                verified_receipt=bool(row["verified_receipt"]),
                verified_statement=bool(row["verified_statement"]),
                comment=row["comment"]
            )
            for row in rows
        ]

    def list_by_account(self, account_id: int) -> list[Transaction]:
        """
        Retrieves all transactions for a specific account.

        :param self: The instance of the repository.
        :param account_id: The ID of the account to retrieve transactions for.
        :type account_id: int
        :return: A list of transactions for the specified account.
        :rtype: list[Transaction]
        """
        with self.connection as conn:
            rows = conn.execute("""
                SELECT * FROM transactions
                WHERE account_id = ?
                ORDER BY transaction_date DESC
            """, (account_id,)).fetchall()

        return [
            Transaction(
                id=row["id"],
                account_id=row["account_id"],
                date_added=datetime.fromisoformat(row["date_added"]),
                date_modified=datetime.fromisoformat(row["date_modified"]),
                source=row["source"],
                transaction_date=date.fromisoformat(row["transaction_date"]),
                amount=row["amount"],
                post_date=date.fromisoformat(
                    row["post_date"]) if row["post_date"] else None,
                description=row["description"],
                category_id=row["category_id"],
                verified_receipt=bool(row["verified_receipt"]),
                verified_statement=bool(row["verified_statement"]),
                comment=row["comment"]
            )
            for row in rows
        ]

    # ----------------------------
    # Filter
    # ----------------------------
    def filter_transactions(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        account_id: Optional[int] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        description_contains: Optional[str] = None
    ) -> list[Transaction]:
        """
        Filters transactions based on the provided criteria.

        :param self: The instance of the repository.
        :param start_date: The start date for filtering transactions.
        :type start_date: Optional[date]
        :param end_date: The end date for filtering transactions.
        :type end_date: Optional[date]
        :param account_id: The ID of the account to filter transactions.
        :type account_id: Optional[int]
        :param min_amount: The minimum amount for filtering transactions.
        :type min_amount: Optional[float]
        :param max_amount: The maximum amount for filtering transactions.
        :type max_amount: Optional[float]
        :param description_contains: A substring to filter transactions by description.
        :type description_contains: Optional[str]
        :return: A list of transactions matching the filter criteria.
        :rtype: list[Transaction]
        """
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if start_date:
            query += " AND transaction_date >= ?"
            params.append(start_date.isoformat())

        if end_date:
            query += " AND transaction_date <= ?"
            params.append(end_date.isoformat())

        if account_id is not None:
            query += " AND account_id = ?"
            params.append(account_id)

        if min_amount is not None:
            query += " AND amount >= ?"
            params.append(min_amount)

        if max_amount is not None:
            query += " AND amount <= ?"
            params.append(max_amount)

        if description_contains:
            query += " AND description LIKE ?"
            params.append(f"%{description_contains}%")

        query += " ORDER BY transaction_date DESC"

        with self.connection as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            Transaction(
                id=row["id"],
                account_id=row["account_id"],
                transaction_date=date.fromisoformat(row["transaction_date"]),
                amount=row["amount"],
                post_date=date.fromisoformat(row["post_date"]) if row["post_date"] else None,
                description=row["description"],
                category_id=row["category_id"],
                cleared=bool(row["cleared"]),
                effective_date=date.fromisoformat(row["effective_date"]) if row["effective_date"] else None,
                verified_receipt=bool(row["verified_receipt"]),
                verified_statement=bool(row["verified_statement"]),
                comment=row["comment"]
            )
            for row in rows
        ]

    # ----------------------------
    # Update
    # ----------------------------
    def update(self, tx: Transaction) -> None:
        """
        Updates an existing transaction in the database.

        :param self: The instance of the repository.
        :param tx: The transaction to update.
        :type tx: Transaction
        """
        with self.connection as conn:
            conn.execute("""
                UPDATE transactions
                SET account_id = ?,
                    date_modified = ?,
                    transaction_date = ?,
                    post_date = ?,
                    description = ?,
                    amount = ?,
                    category_id = ?,
                    verified_receipt = ?,
                    verified_statement = ?,
                    comment = ?
                WHERE id = ?
            """, (
                tx.account_id,
                datetime.now().isoformat(),  # Update the modified date to now
                tx.transaction_date.isoformat(),
                tx.post_date.isoformat() if tx.post_date else None,
                tx.description,
                tx.amount,
                tx.category_id,
                int(tx.verified_receipt),
                int(tx.verified_statement),
                tx.comment,
                tx.id
            ))

    # ----------------------------
    # Delete
    # ----------------------------
    def delete(self, tx_id: int) -> None:
        """
        Deletes a transaction from the database.

        :param self: The instance of the repository.
        :param tx_id: The ID of the transaction to delete.
        :type tx_id: int
        """
        with self.connection as conn:
            conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
