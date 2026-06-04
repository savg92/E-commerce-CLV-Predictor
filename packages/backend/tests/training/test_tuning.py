import os
import tempfile
from pathlib import Path

from backend.training import tuning


def test_run_hyperparameter_search_saves_best_artifacts():
    lines = ["Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country"]

    for i in range(10):
        cust_id = f"1000{i}"
        lines.append(f"100{i},85123A,Prod,5,2009-12-05 10:00:00,2.5,{cust_id},UK")
        lines.append(f"101{i},85123A,Prod,2,2010-01-05 11:00:00,2.5,{cust_id},UK")
        lines.append(f"102{i},85123A,Prod,10,2010-10-05 12:00:00,3.0,{cust_id},UK")

    csv_content = "\n".join(lines)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            result = tuning.run_hyperparameter_search(
                data_path=temp_path,
                learning_rates=[0.01, 0.001],
                dropout_rates=[0.0],
                dense_units=[4],
                epochs=1,
                batch_size=4,
                output_dir=Path(temp_dir),
                seed=7,
            )

            assert len(result.history) == 2
            assert result.best_weights_path.exists()
            assert result.scaler_path.exists()
            assert result.best_config.learning_rate in {0.01, 0.001}
            assert result.best_config.dropout == 0.0
            assert result.best_config.dense_units == 4
        finally:
            os.remove(temp_path)
