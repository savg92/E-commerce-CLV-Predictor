"""Domain entities for the E-commerce CLV Predictor."""

import datetime
from typing import List, Optional

class Transaction:
    """Represents a single transactional record in the system.

    Args:
        invoice_no: Unique identifier for the invoice.
        stock_code: Unique identifier for the product.
        description: Description of the product.
        quantity: Number of units purchased.
        invoice_date: Timestamp of the transaction.
        unit_price: Price per unit of the product.
        customer_id: Unique identifier for the customer.
        country: Country where the transaction originated.
    """
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
        """Calculates the total amount for this transaction line."""
        return self.quantity * self.unit_price

class Customer:
    """Represents a customer in the system with their transaction history.

    Args:
        customer_id: Unique identifier for the customer.
    """
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Adds a transaction to the customer's history.

        Args:
            transaction: The transaction record to add.

        Raises:
            ValueError: If the transaction's customer_id does not match.
        """
        if transaction.customer_id != self.customer_id:
            raise ValueError("Transaction customer_id does not match customer's customer_id")
        self.transactions.append(transaction)

    @property
    def country(self) -> Optional[str]:
        """Determines the customer's country based on their first transaction."""
        if not self.transactions:
            return None
        # Return the country of the first transaction as default
        return self.transactions[0].country
