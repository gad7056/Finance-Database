# repositories/category_repository.py

from sqlite3 import Connection

from models.models import Category


class CategoryRepository:

    # ----------------------------
    # Initialize
    #  ----------------------------
    def __init__(self, connection: Connection):
        self.connection = connection

    # ----------------------------
    # Create
    # ----------------------------
    def add(self, category: Category) -> int:
        """
        Adds a new category to the database.
        The newly added category cannot have a parent that already has a parent.

        :param self: The instance of the repository.
        :param category: The category to add.
        :type category: Category
        :return: The ID of the newly added category.
        :rtype: int
        """
        # if category.parent_id is not None:
        #     parent = self.get_by_id(category.parent_id)
        #     if parent is None or parent.parent_id is not None:
        #         raise ValueError("Invalid parent category.")
        with self.connection as conn:
            cursor = conn.execute(
                """
                INSERT INTO categories (name, parent_id)
                VALUES (?, ?)
            """,
                (category.name, category.parent_id),
            )
        return cursor.lastrowid

    # ----------------------------
    # Read
    # ----------------------------
    def get_by_id(self, category_id: int) -> Category | None:
        """
        Retrieves a category by its ID.

        :param self: The instance of the repository.
        :param category_id: The ID of the category to retrieve.
        :type category_id: int
        :return: The category with the specified ID, or None if not found.
        :rtype: Category | None
        """
        with self.connection as conn:
            row = conn.execute(
                "SELECT * FROM categories WHERE id = ?", (category_id,)
            ).fetchone()

        if not row:
            return None

        return Category(
            id=row["id"], name=row["name"], parent_id=row["parent_id"]
        )

    def get_id_by_name(self, name: str) -> int | None:
        """
        Retrieves a category ID by its name.

        :param self: The instance of the repository.
        :param name: The name of the category to retrieve.
        :type name: str
        :return: The ID of the category with the specified name, or None if not found.
        :rtype: int | None
        """
        with self.connection as conn:
            row = conn.execute(
                "SELECT id FROM categories WHERE name = ?", (name,)
            ).fetchone()

        if not row:
            return None

        return row["id"]

    def list_all(self) -> list[Category]:
        """
        Retrieves all categories from the database.

        :param self: The instance of the repository.
        :return: A list of all categories.
        :rtype: list[Category]
        """
        with self.connection as conn:
            rows = conn.execute(
                "SELECT * FROM categories ORDER BY name"
            ).fetchall()

        return [
            Category(id=row["id"], name=row["name"], parent_id=row["parent_id"])
            for row in rows
        ]

    def list_parent_categories(self) -> list[Category]:
        """
        Retrieves all root categories (categories without a parent) from the database.

        :param self: The instance of the repository.
        :return: A list of all root categories.
        :rtype: list[Category]
        """
        with self.connection as conn:
            rows = conn.execute(
                """
                SELECT * FROM categories
                WHERE parent_id IS NULL
                ORDER BY name
            """
            ).fetchall()

        return [
            Category(id=row["id"], name=row["name"], parent_id=None)
            for row in rows
        ]

    def list_children_categories(self) -> list[Category]:
        """
        Retrieves all child categories from the database.

        :param self: The instance of the repository.
        :return: A list of all child categories.
        :rtype: list[Category]
        """
        with self.connection as conn:
            rows = conn.execute(
                """
                SELECT * FROM categories
                WHERE parent_id IS NOT NULL
                ORDER BY name
            """
            ).fetchall()

        return [
            Category(id=row["id"], name=row["name"], parent_id=row["parent_id"])
            for row in rows
        ]

    def list_children_of(self, parent_id: int) -> list[Category]:
        """
        Retrieves all child categories of a given parent category.

        :param self: The instance of the repository.
        :param parent_id: The ID of the parent category.
        :type parent_id: int
        :return: A list of child categories for the specified parent.
        :rtype: list[Category]
        """
        with self.connection as conn:
            rows = conn.execute(
                """
                SELECT * FROM categories
                WHERE parent_id = ?
                ORDER BY name
            """,
                (parent_id,),
            ).fetchall()

        return [
            Category(id=row["id"], name=row["name"], parent_id=row["parent_id"])
            for row in rows
        ]

    def get_parent(self, category_id: int) -> Category | None:
        """
        Retrieves the parent category of a given category.

        :param self: The instance of the repository.
        :param category_id: The ID of the category whose parent is to be retrieved.
        :type category_id: int
        :return: The parent category, or None if the category has no parent or does not exist.
        :rtype: Category | None
        """
        with self.connection as conn:
            row = conn.execute(
                """
                SELECT parent.*
                FROM categories AS child
                JOIN categories AS parent ON child.parent_id = parent.id
                WHERE child.id = ?
            """,
                (category_id,),
            ).fetchone()

        if not row:
            return None

        return Category(
            id=row["id"], name=row["name"], parent_id=row["parent_id"]
        )

    def category_exists(self, parent_id: int, name: str) -> bool:
        """
        Checks if a category with the given name exists in the database.

        :param self: The instance of the repository.
        :param parent_id: The ID of the parent category.
        :type parent_id: int
        :param name: The name of the category to check.
        :type name: str
        :return: True if a category with the given name exists, False otherwise.
        :rtype: bool
        """
        with self.connection as conn:
            row = conn.execute(
                """
                SELECT 1 FROM categories
                WHERE parent_id = ? AND name = ?
                LIMIT 1
            """,
                (parent_id, name),
            ).fetchone()

        return bool(row)

    def pretty_print(self) -> None:
        """
        Prints the category hierarchy in a human-readable format.

        :param self: The instance of the repository.
        :return None:
        """

        def print_category(category: Category, level=0):
            print("  " * level + f"- {category.name} (ID: {category.id})")
            children = self.list_children_of(category.id)
            for child in children:
                print_category(child, level + 1)

        root_categories = self.list_parent_categories()
        for root in root_categories:
            print_category(root)
        return

    # ----------------------------
    # Update
    # ----------------------------
    def update(self, category: Category) -> None:
        """
        Updates an existing category in the database.

        :param self: The instance of the repository.
        :param category: The category to update.
        :type category: Category
        :return None:
        """
        if category.id is None:
            raise ValueError("Category must have an id to update")

        with self.connection as conn:
            conn.execute(
                """
                UPDATE categories
                SET name = ?, parent_id = ?
                WHERE id = ?
            """,
                (category.name, category.parent_id, category.id),
            )
        return

    # ----------------------------
    # Delete
    # ----------------------------
    def delete(self, category_id: int) -> bool:
        """
        Deletes a category only if it has no children.
        Prevents accidental orphan trees.

        :param self: The instance of the repository.
        :param category_id: The ID of the category to delete.
        :type category_id: int
        :return: True if the category was deleted, False otherwise.
        :rtype: bool
        """

        with self.connection as conn:
            child = conn.execute(
                """
                SELECT 1 FROM categories
                WHERE parent_id = ?
                LIMIT 1
            """,
                (category_id,),
            ).fetchone()

            if child:
                raise ValueError("Cannot delete category with subcategories")

            cursor = conn.execute(
                "DELETE FROM categories WHERE id = ?", (category_id,)
            )
            return cursor.rowcount > 0
