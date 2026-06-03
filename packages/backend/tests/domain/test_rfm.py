import datetime
import pytest
from backend.domain.entities import Transaction, Customer
from backend.domain.use_cases import CalculateRFM

def test_transaction_and_customer_entities():
    # Write a test to ensure Transaction and Customer entities can be created and hold basic attributes
    t = Transaction(
        invoice_no="12345",
        stock_code="85123A",
        description="WHITE HANGING HEART T-LIGHT HOLDER",
        quantity=6,
        invoice_date=datetime.datetime(2009, 12, 1, 7, 45),
        unit_price=2.55,
        customer_id="17850",
        country="United Kingdom"
    )
    assert t.line_amount == pytest.approx(15.30)

    customer = Customer(customer_id="17850")
    customer.add_transaction(t)
    assert len(customer.transactions) == 1
    assert customer.country == "United Kingdom"

def test_calculate_rfm_use_case():
    # Prepare some mock transactions
    t1 = Transaction(
        invoice_no="12345",
        stock_code="A",
        description="Product A",
        quantity=2,
        invoice_date=datetime.datetime(2009, 12, 1, 8, 0),
        unit_price=5.0,
        customer_id="C1",
        country="UK"
    )
    t2 = Transaction(
        invoice_no="12346",
        stock_code="B",
        description="Product B",
        quantity=3,
        invoice_date=datetime.datetime(2009, 12, 3, 10, 0),
        unit_price=4.0,
        customer_id="C1",
        country="UK"
    )
    
    # We will compute RFM using a cutoff date of 2009-12-5
    cutoff_date = datetime.datetime(2009, 12, 5)
    
    # Target window transaction (for Future_CLV)
    t_target = Transaction(
        invoice_no="12347",
        stock_code="C",
        description="Product C",
        quantity=1,
        invoice_date=datetime.datetime(2009, 12, 6, 12, 0),
        unit_price=20.0,
        customer_id="C1",
        country="UK"
    )
    
    use_case = CalculateRFM()
    features = use_case.execute(
        customer_id="C1",
        obs_transactions=[t1, t2],
        future_transactions=[t_target],
        cutoff_date=cutoff_date
    )
    
    assert features["CustomerID"] == "C1"
    assert features["Frequency"] == 2
    assert features["Monetary"] == 22.0 # (2*5.0) + (3*4.0) = 10 + 12 = 22
    assert features["RecencyDays"] == 2 # 2009-12-5 minus 2009-12-3 (last purchase) is 2 days
    assert features["TenureDays"] == 3 # 2009-12-3 minus 2009-12-1 is 2 days + 1 = 3 days
    assert features["AvgBasketValue"] == 11.0 # 22 / 2
    assert features["AvgBasketQuantity"] == 2.5 # (2 + 3) / 2
    assert features["UniqueProducts"] == 2
    assert features["AverageUnitPrice"] == 4.5 # (5.0 + 4.0) / 2
    assert features["Future_CLV"] == 20.0 # From target window transaction
