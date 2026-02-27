# models.py

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional


class AccountType(Enum):
    INVESTMENT = "Investment"
    CHECKING = "Checking"
    SAVINGS = "Savings"
    CREDIT = "Credit"
    CASH = "Cash"


@dataclass
class Account:
    id: Optional[int]
    name: str
    institution: Optional[str]
    type: AccountType
    number: str
    is_active: bool = True


@dataclass
class Category:
    id: Optional[int]
    name: str
    parent_id: Optional[int] = None


@dataclass
class Tag:
    id: Optional[int]
    name: str


@dataclass
class Transaction:
    id: Optional[int]
    date_added: datetime
    date_modified: datetime
    source: Optional[str]
    account_id: int
    transaction_date: date
    amount: float
    verified_receipt: bool = False
    verified_statement: bool = False
    post_date: Optional[date] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    comment: Optional[str] = None
