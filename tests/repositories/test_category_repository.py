import pytest

from repositories.category_repository import CategoryRepository
from models.models import Category


@pytest.fixture
def category_repo():
    return CategoryRepository()


def test_add(category_repo):
    assert True
    return


# def test_get_by_id(category_repo):
#     return


# def test_list_all(category_repo):
#     return


# def test_update(category_repo):
#     return


# def test_delete(category_repo):
#     return
