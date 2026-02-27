# repositories/tags_repository.py

from database.connection import get_connection
from models.models import Tag
from sqlite3 import Connection


class TagRepository:

    # ----------------------------
    # Initialize
    #  ----------------------------
    def __init__(self, connection: Connection):
        self.connection = connection

    # ----------------------------
    # Create
    # ----------------------------
    def add(self, tag: Tag) -> int:
        """
        Adds a new tag to the database.

        :param self: The instance of the repository.
        :param tag: The tag to add.
        :type tag: Tag
        :return: The ID of the newly added tag.
        :rtype: int
        """
        with self.connection as conn:
            cursor = conn.execute(
                "INSERT INTO tags (name) VALUES (?)",
                (tag.name,)
            )
        return cursor.lastrowid

    def assign_to_transaction(self, transaction_id: int, tag_id: int) -> None:
        """
        Assigns a tag to a transaction.

        :param self: The instance of the repository.
        :param transaction_id: The ID of the transaction.
        :type transaction_id: int
        :param tag_id: The ID of the tag.
        :type tag_id: int
        """
        with self.connection as conn:
            conn.execute("""
                INSERT OR IGNORE INTO transaction_tags (transaction_id, tag_id)
                VALUES (?, ?)
            """, (transaction_id, tag_id))

    # ----------------------------
    # Read
    # ----------------------------
    def list_tags_for_transaction(self, transaction_id: int) -> list[Tag]:
        """
        Retrieves all tags assigned to a specific transaction.

        :param self: The instance of the repository.
        :param transaction_id: The ID of the transaction.
        :type transaction_id: int
        :return: A list of tags assigned to the transaction.
        :rtype: list[Tag]
        """
        with self.connection as conn:
            rows = conn.execute("""
                SELECT t.id, t.name
                FROM tags t
                JOIN transaction_tags tt ON t.id = tt.tag_id
                WHERE tt.transaction_id = ?
            """, (transaction_id,)).fetchall()

        return [Tag(id=row["id"], name=row["name"]) for row in rows]

    # ----------------------------
    # Update
    # ----------------------------
    def update(self, tag: Tag) -> None:
        """
        Updates an existing tag in the database.

        :param self: The instance of the repository.
        :param tag: The tag to update.
        :type tag: Tag
        """
        with self.connection as conn:
            conn.execute("""
                UPDATE tags
                SET name = ?
                WHERE id = ?
            """, (tag.name, tag.id))

    # ----------------------------
    # Delete
    # ----------------------------
    def delete(self, tag_id: int) -> None:
        """
        Deletes a tag from the database.

        :param self: The instance of the repository.
        :param tag_id: The ID of the tag to delete.
        :type tag_id: int
        """
        with self.connection as conn:
            conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
            conn.execute(
                "DELETE FROM transaction_tags WHERE tag_id = ?", (tag_id,))
