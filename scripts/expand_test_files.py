import os
import random

def generate_rfm_csv(file_path, row_count, behavior_type):
    headers = "Country,RecencyDays,TenureDays,Frequency,Monetary,AvgBasketValue,AvgBasketQuantity,UniqueProducts,AverageUnitPrice"
    countries = ["United Kingdom", "France", "Germany", "Spain"]
    
    rows = [headers]
    
    for _ in range(row_count):
        country = random.choice(countries)
        
        if behavior_type == "normal":
            recency = random.randint(1, 30)
            tenure = random.randint(100, 400)
            freq = random.randint(2, 15)
            monetary = round(random.uniform(50.0, 500.0), 2)
            avg_basket_v = round(monetary / freq, 2)
            avg_basket_q = round(random.uniform(2, 10), 1)
            unique_p = random.randint(2, 20)
            avg_unit_p = round(random.uniform(1.0, 10.0), 2)
        elif behavior_type == "high_value":
            recency = random.randint(1, 7)
            tenure = random.randint(300, 600)
            freq = random.randint(20, 100)
            monetary = round(random.uniform(1000.0, 10000.0), 2)
            avg_basket_v = round(monetary / freq, 2)
            avg_basket_q = round(random.uniform(10, 50), 1)
            unique_p = random.randint(20, 100)
            avg_unit_p = round(random.uniform(5.0, 50.0), 2)
        elif behavior_type == "ood":
            recency = random.randint(300, 500) # Old/Inactive
            tenure = random.randint(500, 1000)
            freq = random.randint(200, 500) # Extreme freq
            monetary = round(random.uniform(50000.0, 200000.0), 2) # Extreme monetary
            avg_basket_v = round(monetary / freq, 2)
            avg_basket_q = round(random.uniform(100, 1000), 1) # Extreme quantity
            unique_p = random.randint(100, 500)
            avg_unit_p = round(random.uniform(100.0, 5000.0), 2) # Extreme prices
            
        rows.append(f"{country},{recency},{tenure},{freq},{monetary},{avg_basket_v},{avg_basket_q},{unique_p},{avg_unit_p}")
                
    with open(file_path, "w") as f:
        f.write("\n".join(rows))

os.makedirs("Test files", exist_ok=True)
generate_rfm_csv("Test files/normal_behavior.csv", 60, "normal")
generate_rfm_csv("Test files/high_value_customer.csv", 60, "high_value")
generate_rfm_csv("Test files/ood_behavior.csv", 60, "ood")

print("Generated 60 RFM rows per file.")
