import os
from pathlib import Path
from backend.training import tuning

def generate_dummy_data(path: str):
    lines = ["Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country"]
    for i in range(20):
        cust_id = f"1000{i}"
        # Observation window
        lines.append(f"100{i},85123A,Prod,5,2009-12-05 10:00:00,2.5,{cust_id},UK")
        lines.append(f"101{i},85123A,Prod,2,2010-01-05 11:00:00,2.5,{cust_id},UK")
        # Target window (beyond 9 months)
        lines.append(f"102{i},85123A,Prod,10,2010-10-05 12:00:00,3.0,{cust_id},UK")
    
    with open(path, "w") as f:
        f.write("\n".join(lines))

def main():
    data_path = "dummy_data.csv"
    generate_dummy_data(data_path)
    
    output_dir = Path("artifacts/training")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Training placeholder model...")
    tuning.run_hyperparameter_search(
        data_path=data_path,
        learning_rates=[0.01],
        dropout_rates=[0.2],
        dense_units=[64],
        epochs=5,
        batch_size=4,
        output_dir=output_dir,
        seed=42,
    )
    
    print(f"Artifacts generated in {output_dir}")
    os.remove(data_path)

if __name__ == "__main__":
    main()
