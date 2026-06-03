import datetime
import pandas as pd
from typing import List
from backend.domain.entities import Transaction
from backend.domain.repositories import TransactionRepository

class CSVTransactionRepository(TransactionRepository):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_transactions(self) -> List[Transaction]:
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
            df["CustomerID"] = df["CustomerID"].apply(lambda x: x.split('.')[0] if '.' in x else x)

        # Convert to Domain Transactions
        transactions = []
        for _, row in df.iterrows():
            t = Transaction(
                invoice_no=row.get("InvoiceNo", ""),
                stock_code=row.get("StockCode", ""),
                description=row.get("Description", ""),
                quantity=int(row.get("Quantity", 0)),
                invoice_date=row["InvoiceDate"].to_pydatetime() if isinstance(row["InvoiceDate"], pd.Timestamp) else row["InvoiceDate"],
                unit_price=float(row.get("UnitPrice", 0.0)),
                customer_id=row.get("CustomerID", ""),
                country=row.get("Country", "")
            )
            transactions.append(t)
            
        return transactions

class DBTransactionRepository(TransactionRepository):
    def __init__(self, db_url: str):
        self.db_url = db_url

    def load_transactions(self) -> List[Transaction]:
        # Return empty list or raise NotImplementedError
        # In a real system this would connect to DB using SQLAlchemy or similar
        raise NotImplementedError("Database transaction loader is not yet implemented.")
