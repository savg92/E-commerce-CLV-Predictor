import datetime
import tempfile
import os
import pytest
from backend.infrastructure.data_loaders import CSVTransactionRepository

def test_csv_transaction_repository_loads_and_cleans_data():
    # Create a temporary CSV file with mock transaction data
    # Header: Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country
    # (Note: standardizing names like in the notebook: 'Invoice' -> 'InvoiceNo', 'Price' -> 'UnitPrice', 'Customer ID' -> 'CustomerID')
    csv_content = """Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country
489434,85111,WHITE METAL LANTERN,6,2009-12-01 07:45:00,2.1,13085,United Kingdom
C489435,85112,RED METAL LANTERN,-1,2009-12-01 07:46:00,1.25,13085,United Kingdom
489436,22064,TOY TIDY PINK,10,2009-12-01 09:24:00,2.1,,United Kingdom
489437,21871,S/4 COFFEE MUGS + HOLDER,6,2009-12-01 09:28:00,1.25,13085,United Kingdom
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        repo = CSVTransactionRepository(filepath=temp_path)
        transactions = repo.load_transactions()
        
        # We expect:
        # - The missing Customer ID row (489436) to be dropped/filtered out or handled based on use cases.
        # Wait, the spec says "Handle missing CustomerIDs and outliers."
        # If we load transactions, do we drop missing CustomerIDs immediately in the repository or let the client handle it?
        # Let's drop them or handle them in the loader. In the notebook: `df = df.dropna(subset=["InvoiceDate", "CustomerID", "Description"])`
        # and filter cancelations: `df = df[~df["InvoiceNo"].str.startswith("C", na=False)]`
        # Let's verify that the CSV loader correctly handles standard column names, drops missing CustomerIDs, and handles cancelations.
        
        # Valid transactions expected:
        # Row 1: 489434 (Valid)
        # Row 2: C489435 (Canceled - should be filtered or loaded? In the notebook, cancellations are filtered out. Let's filter them in the repository loader)
        # Row 3: 489436 (Missing Customer ID - filtered)
        # Row 4: 489437 (Valid)
        
        assert len(transactions) == 2
        
        t1 = transactions[0]
        assert t1.invoice_no == "489434"
        assert t1.stock_code == "85111"
        assert t1.quantity == 6
        assert t1.invoice_date == datetime.datetime(2009, 12, 1, 7, 45)
        assert t1.unit_price == pytest.approx(2.1)
        assert t1.customer_id == "13085"
        assert t1.country == "United Kingdom"
        
        t2 = transactions[1]
        assert t2.invoice_no == "489437"
        assert t2.customer_id == "13085"
    finally:
        os.remove(temp_path)
