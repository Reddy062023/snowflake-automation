import os
import snowflake.connector

# Snowflake credentials from GitHub Secrets
conn = snowflake.connector.connect(
    user=os.environ['JAPENDRAS06'],
    password=os.environ['Medway@01282026'],
    account=os.environ['ewzqeyy-iic66448'],
    database='MY_DB',
    schema='PUBLIC',
    warehouse='COMPUTE_WH'
)

cursor = conn.cursor()

# 1️⃣ Create file format (if not exists)
cursor.execute("""
CREATE OR REPLACE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    DATE_FORMAT = 'YYYY-MM-DD';
""")
print("File format created.")

# 2️⃣ Create stage (if not exists)
cursor.execute("""
CREATE OR REPLACE STAGE my_stage
    FILE_FORMAT = my_csv_format;
""")
print("Stage created.")

# 3️⃣ Upload CSV from local repo into stage
# The Python connector allows PUT via `cursor.execute`
csv_file = os.path.join(os.getcwd(), "employees.csv")

# For local file PUT, Snowflake requires SnowSQL, so we use an alternative:
# We will use the Python connector's "write_pandas" as a modern approach
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

df = pd.read_csv(csv_file)
success, nchunks, nrows, _ = write_pandas(conn, df, 'EMPLOYEES_CICD')
print(f"Uploaded {nrows} rows in {nchunks} chunks to EMPLOYEES_CICD table.")

# 4️⃣ Close connection
cursor.close()
conn.close()
print("Done.")