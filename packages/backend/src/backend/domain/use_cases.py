"""Use cases for the E-commerce CLV Predictor domain."""

import datetime
from typing import List, Dict, Any, Optional
from backend.domain.entities import Transaction

class CalculateRFM:
    """Orchestrates the calculation of RFM features for a single customer.
    
    This use case aggregates transaction logs into high-level features suitable
    for CLV prediction.
    """
    def execute(
        self,
        customer_id: str,
        obs_transactions: List[Transaction],
        future_transactions: Optional[List[Transaction]] = None,
        cutoff_date: Optional[datetime.datetime] = None
    ) -> Dict[str, Any]:
        """Calculates RFM and auxiliary metrics for a customer.

        Args:
            customer_id: Unique identifier for the customer.
            obs_transactions: List of transactions in the observation window.
            future_transactions: List of transactions in the target window.
            cutoff_date: The date that separates observation from target.

        Returns:
            A dictionary containing aggregated features and target CLV.
        """
        if not obs_transactions:
            return {
                "CustomerID": customer_id,
                "FirstPurchase": None,
                "LastPurchase": None,
                "Frequency": 0,
                "Monetary": 0.0,
                "AvgBasketValue": 0.0,
                "AvgBasketQuantity": 0.0,
                "AvgProductsPerInvoice": 0.0,
                "UniqueProducts": 0,
                "AverageUnitPrice": 0.0,
                "RecencyDays": 0,
                "TenureDays": 0,
                "Future_CLV": 0.0,
                "Country": None
            }

        # Step 1: Aggregate at Invoice level
        invoices: Dict[str, Dict[str, Any]] = {}
        for t in obs_transactions:
            inv_no = t.invoice_no
            if inv_no not in invoices:
                invoices[inv_no] = {
                    "InvoiceNo": inv_no,
                    "InvoiceDate": t.invoice_date,
                    "InvoiceAmount": 0.0,
                    "InvoiceQuantity": 0,
                    "StockCodes": set(),
                    "Country": t.country
                }
            
            # Update values
            if t.invoice_date > invoices[inv_no]["InvoiceDate"]:
                invoices[inv_no]["InvoiceDate"] = t.invoice_date
            invoices[inv_no]["InvoiceAmount"] += t.line_amount
            invoices[inv_no]["InvoiceQuantity"] += t.quantity
            invoices[inv_no]["StockCodes"].add(t.stock_code)

        # Step 2: Aggregate at Customer level
        invoice_list = list(invoices.values())
        dates = [inv["InvoiceDate"] for inv in invoice_list]
        first_purchase = min(dates)
        last_purchase = max(dates)
        frequency = len(invoice_list)
        monetary = sum(inv["InvoiceAmount"] for inv in invoice_list)
        
        avg_basket_value = monetary / frequency if frequency > 0 else 0.0
        avg_basket_qty = sum(inv["InvoiceQuantity"] for inv in invoice_list) / frequency if frequency > 0 else 0.0
        avg_products_per_inv = sum(len(inv["StockCodes"]) for inv in invoice_list) / frequency if frequency > 0 else 0.0
        country = invoice_list[0]["Country"] if invoice_list else None

        # Additional metrics
        all_stock_codes = set()
        sum_unit_price = 0.0
        tx_count = len(obs_transactions)
        for t in obs_transactions:
            all_stock_codes.add(t.stock_code)
            sum_unit_price += t.unit_price

        unique_products = len(all_stock_codes)
        avg_unit_price = sum_unit_price / tx_count if tx_count > 0 else 0.0

        # Temporal metrics
        if cutoff_date is not None:
            # Match Pandas behavior: difference in days
            recency_days = (cutoff_date.date() - last_purchase.date()).days
        else:
            recency_days = 0

        tenure_days = (last_purchase.date() - first_purchase.date()).days + 1

        # Target CLV
        future_clv = 0.0
        if future_transactions:
            future_clv = sum(t.line_amount for t in future_transactions)

        return {
            "CustomerID": customer_id,
            "FirstPurchase": first_purchase,
            "LastPurchase": last_purchase,
            "Frequency": frequency,
            "Monetary": monetary,
            "AvgBasketValue": avg_basket_value,
            "AvgBasketQuantity": avg_basket_qty,
            "AvgProductsPerInvoice": avg_products_per_inv,
            "UniqueProducts": unique_products,
            "AverageUnitPrice": avg_unit_price,
            "RecencyDays": recency_days,
            "TenureDays": tenure_days,
            "Future_CLV": future_clv,
            "Country": country
        }
