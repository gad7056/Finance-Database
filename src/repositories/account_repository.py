# repositories/account_repository.py

from sqlite3 import Connection

from models.models import Account, AccountType


class AccountRepository:

    # ----------------------------
    # Initialize
    #  ----------------------------
    def __init__(self, connection: Connection):
        self.connection = connection

    # ----------------------------
    # Create
    # ----------------------------
    def add(self, account: Account) -> int:
        """
        Adds a new account to the database.

        :param self: The instance of the repository.
        :param account: The account to add.
        :type account: Account
        :return: The ID of the newly added account.
        :rtype: int
        """
        with self.connection as conn:
            cursor = conn.execute(
                """
                INSERT INTO accounts (name, institution, type, number, is_active)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    account.name,
                    account.institution,
                    account.type.value,
                    account.number,
                    int(account.is_active),
                ),
            )
        return cursor.lastrowid

    # ----------------------------
    # Read
    # ----------------------------
    def get_by_id(self, account_id: int) -> Account | None:
        """
        Retrieves an account by its ID.

        :param self: The instance of the repository.
        :param account_id: The ID of the account to retrieve.
        :type account_id: int
        :return: The account with the specified ID, or None if not found.
        :rtype: Account | None
        """
        with self.connection as conn:
            row = conn.execute(
                "SELECT * FROM accounts WHERE id = ?", (account_id,)
            ).fetchone()

        if not row:
            return None

        return Account(
            id=row["id"],
            name=row["name"],
            institution=row["institution"],
            type=AccountType(row["type"]),
            number=row["number"],
            is_active=bool(row["is_active"]),
        )

    def list_all(self) -> list[Account]:
        """
        Retrieves all accounts from the database.

        :param self: The instance of the repository.
        :return: A list of all accounts.
        :rtype: list[Account]
        """
        with self.connection as conn:
            rows = conn.execute("SELECT * FROM accounts").fetchall()

        return [
            Account(
                id=row["id"],
                name=row["name"],
                institution=row["institution"],
                type=AccountType(row["type"]),
                number=row["number"],
                is_active=bool(row["is_active"]),
            )
            for row in rows
        ]

    def list_banks(self) -> list[str]:
        """
        Retrieves a list of unique bank names from the accounts.

        :param self: The instance of the repository.
        :return: A list of unique bank names.
        :rtype: list[str]
        """
        with self.connection as conn:
            rows = conn.execute(
                "SELECT DISTINCT institution FROM accounts"
            ).fetchall()

        return [row["institution"] for row in rows if row["institution"]]

    def list_accounts_by_bank(self, bank_name: str) -> list[Account]:
        """
        Retrieves a list of accounts associated with a specific bank.

        :param self: The instance of the repository.
        :param bank_name: The name of the bank to filter accounts by.
        :type bank_name: str
        :return: A list of accounts associated with the specified bank.
        :rtype: list[Account]
        """
        with self.connection as conn:
            rows = conn.execute(
                "SELECT * FROM accounts WHERE institution = ?", (bank_name,)
            ).fetchall()

        return [
            Account(
                id=row["id"],
                name=row["name"],
                institution=row["institution"],
                type=AccountType(row["type"]),
                number=row["number"],
                is_active=bool(row["is_active"]),
            )
            for row in rows
        ]

    def get_id_by_name(self, name: str) -> int | None:
        """
        Retrieves the ID of an account based on its name.

        :param self: The instance of the repository.
        :param name: The name of the account to search for.
        :type name: str
        :return: The ID of the account with the specified name, or None if not found.
        :rtype: int | None
        """
        with self.connection as conn:
            row = conn.execute(
                "SELECT id FROM accounts WHERE name = ?", (name,)
            ).fetchone()

        return row["id"] if row else None

    def pretty_print(self) -> None:
        """
        Prints a formatted list of accounts grouped by bank.

        :param self: The instance of the repository.
        :return None:
        """
        banks = self.list_banks()
        for bank in banks:
            print(bank)
            accounts = self.list_accounts_by_bank(bank)
            for acc in accounts:
                print(f" - {acc.name} (x{acc.number[-4:]})")

    # ----------------------------
    # Update
    # ----------------------------
    def update(self, account: Account) -> None:
        """
        Updates an existing account in the database.

        :param self: The instance of the repository.
        :param account: The account to update.
        :type account: Account
        :return None:
        """
        if account.id is None:
            raise ValueError("Account must have an id to update")

        with self.connection as conn:
            conn.execute(
                """
                UPDATE accounts
                SET name = ?, institution = ?, type = ?, number = ?, is_active = ?
                WHERE id = ?
            """,
                (
                    account.name,
                    account.institution,
                    account.type.value,
                    account.number,
                    int(account.is_active),
                    account.id,
                ),
            )

    # ----------------------------
    # Delete
    # ----------------------------
    def delete(self, account_id: int) -> None:
        """
        Deletes an account from the database.

        :param self: The instance of the repository.
        :param account_id: The ID of the account to delete.
        :type account_id: int
        :return None:
        """
        with self.connection as conn:
            conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
