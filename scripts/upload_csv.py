import os
import sys
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# -------------------------------
# 1️⃣ Check required environment variables
# -------------------------------
required_env = ["SNOWSQL_ACCOUNT", "SNOWSQL_USER", "SNOWSQL_PASSWORD"]
missing = [var for var in required_env if var not in os.environ]
if missing:
    print(f"ERROR: Missing environment variables: {', '.join(missing)}")
    sys.exit(1)

# -------------------------------
# 2️⃣ Connect to Snowflake
# -------------------------------
conn = snowflake.connector.connect(
    user=os.environ['SNOWSQL_USER'],
    password=os.environ['SNOWSQL_PASSWORD'],
    account=os.environ['SNOWSQL_ACCOUNT'],
    database='MY_DB',
    schema='PUBLIC',
    warehouse='COMPUTE_WH'
)
cursor = conn.cursor()
print("✅ Connected to Snowflake")

# -------------------------------
# 3️⃣ Create file format
# -------------------------------
cursor.execute("""
CREATE OR REPLACE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    DATE_FORMAT = 'YYYY-MM-DD';
""")
print("✅ File format created")

# -------------------------------
# 4️⃣ Create stage
# -------------------------------
cursor.execute("""
CREATE OR REPLACE STAGE my_stage
    FILE_FORMAT = my_csv_format;
""")
print("✅ Stage created")

# -------------------------------
# 5️⃣ Upload CSV using pandas
# -------------------------------
csv_file = os.path.join(os.getcwd(), "employees.csv")
if not os.path.exists(csv_file):
    print(f"ERROR: CSV file not found at {csv_file}")
    sys.exit(1)

df = pd.read_csv(csv_file)
success, nchunks, nrows, _ = write_pandas(conn, df, 'EMPLOYEES_CICD')
print(f"✅ Uploaded {nrows} rows in {nchunks} chunks to EMPLOYEES_CICD table")

# -------------------------------
# 6️⃣ Close connection
# -------------------------------
cursor.close()
conn.close()
print("✅ Done")