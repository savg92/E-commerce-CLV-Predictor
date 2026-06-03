import datetime
from typing import List, Optional

class Transaction:
    def __init__(
        self,
        invoice_no: str,
        stock_code: str,
        description: str,
        quantity: int,
        invoice_date: datetime.datetime,
        unit_price: float,
        customer_id: str,
        country: str
    ):
        self.invoice_no = invoice_no
        self.stock_code = stock_code
        self.description = description
        self.quantity = quantity
        self.invoice_date = invoice_date
        self.unit_price = unit_price
        self.customer_id = customer_id
        self.country = country

    @property
    def line_amount(self) -> float:
        return self.quantity * self.unit_price

class Customer:
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        if transaction.customer_id != self.customer_id:
            raise ValueError("Transaction customer_id does not match customer's customer_id")
        self.transactions.append(transaction)

    @property
    def country(self) -> Optional[str]:
        if not self.transactions:
            return None
        # Return the country of the first transaction as default
        return self.transactions[0].country
