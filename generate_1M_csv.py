import pandas as pd
from faker import Faker
import random

fake = Faker()
num_records = 1_000_000  # 1 million

data = {
    "ID": range(1, num_records + 1),
    "Name": [fake.name() for _ in range(num_records)],
    "Email": [fake.email() for _ in range(num_records)],
    "Salary": [round(random.uniform(30000, 150000), 2) for _ in range(num_records)],
    "Joining_Date": [fake.date_between(start_date='-10y', end_date='today') for _ in range(num_records)]
}

df = pd.DataFrame(data)

df.to_csv("employees_1M.csv", index=False)
print("CSV file with 1 million records created successfully!")