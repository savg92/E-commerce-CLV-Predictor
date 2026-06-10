"""Infrastructure data loaders for the E-commerce CLV Predictor."""

from typing import List
import pandas as pd
from backend.domain.entities import Transaction
from backend.domain.repositories import TransactionRepository

class CSVTransactionRepository(TransactionRepository):
    """Loads transactions from a CSV file.

    Attributes:
        filepath: Path to the CSV file.
    """

    def __init__(self, filepath: str):
        """Initializes the repository with a file path."""
        self.filepath = filepath

    def load_transactions(self) -> List[Transaction]:
        """Loads and cleans transactions from the CSV file.

        Returns:
            A list of domain Transaction objects.
        """
        # Read raw CSV
        df = pd.read_csv(self.filepath)
        
        # Standardize columns based on notebook mappings
        column_mapping = {
            "Invoice": "InvoiceNo",
            "InvoiceNo": "InvoiceNo",
            "Customer ID": "CustomerID",
            "CustomerID": "CustomerID",
            "Price": "UnitPrice",
            "UnitPrice": "UnitPrice",
            "InvoiceDate": "InvoiceDate"
        }
        df = df.rename(columns=column_mapping)
        
        # Drop missing critical fields
        required_cols = ["CustomerID", "InvoiceDate", "Description"]
        for col in required_cols:
            if col in df.columns:
                df = df.dropna(subset=[col])
        
        # Ensure correct datatypes
        if "InvoiceDate" in df.columns:
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
            df = df.dropna(subset=["InvoiceDate"])
            
        if "InvoiceNo" in df.columns:
            df["InvoiceNo"] = df["InvoiceNo"].astype(str)
            # Filter cancellations
            df = df[~df["InvoiceNo"].str.startswith("C", na=False)]
            
        if "StockCode" in df.columns:
            df["StockCode"] = df["StockCode"].astype(str)
            
        if "Quantity" in df.columns:
            df["Quantity"] = df["Quantity"].astype(int)
            
        if "UnitPrice" in df.columns:
            df["UnitPrice"] = df["UnitPrice"].astype(float)
            
        if "CustomerID" in df.columns:
            df["CustomerID"] = df["CustomerID"].astype(str)
            # Remove decimal part if loaded as float e.g. 12345.0 -> 12345
            df["CustomerID"] = df["CustomerID"].apply(
                lambda x: x.split('.')[0] if '.' in x else x
            )

        # Convert to Domain Transactions
        transactions = []
        for _, row in df.iterrows():
            inv_date = row["InvoiceDate"]
            if isinstance(inv_date, pd.Timestamp):
                inv_date = inv_date.to_pydatetime()

            t = Transaction(
                invoice_no=row.get("InvoiceNo", ""),
                stock_code=row.get("StockCode", ""),
                description=row.get("Description", ""),
                quantity=int(row.get("Quantity", 0)),
                invoice_date=inv_date,
                unit_price=float(row.get("UnitPrice", 0.0)),
                customer_id=row.get("CustomerID", ""),
                country=row.get("Country", "")
            )
            transactions.append(t)
            
        return transactions

class DBTransactionRepository(TransactionRepository):
    """Loads transactions from a database.
    
    Attributes:
        db_url: Database connection URL.
    """

    def __init__(self, db_url: str):
        """Initializes the repository with a DB URL."""
        self.db_url = db_url

    def load_transactions(self) -> List[Transaction]:
        """Loads transactions from the database.

        Raises:
            NotImplementedError: Database loader is not yet implemented.
        """
        # TODO(savg): Implement database transaction loader using SQLAlchemy.
        raise NotImplementedError(
            "Database transaction loader is not yet implemented."
        )
