# services/transaction_service.py

from datetime import datetime, timezone

from models.models import Transaction


class TransactionService:

    @staticmethod
    def create_new(
        *,
        account_id: int,
        transaction_date,
        amount: float,
        source: str,
        post_date=None,
        description=None,
        category_id=None,
        comment=None,
        verified_receipt=False,
        verified_statement=False,
    ) -> Transaction:

        now = datetime.now(timezone.utc)

        return Transaction(
            id=None,
            date_added=now,
            date_modified=now,
            source=source,
            account_id=account_id,
            transaction_date=transaction_date,
            amount=amount,
            verified_receipt=verified_receipt,
            verified_statement=verified_statement,
            post_date=post_date,
            description=description,
            category_id=category_id,
            comment=comment,
        )
