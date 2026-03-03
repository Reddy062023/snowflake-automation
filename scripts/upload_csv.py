import os
import pandas as pd
import pyarrow
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# -------------------------------
# 1. Snowflake credentials from GitHub Secrets
# -------------------------------
SNOWSQL_ACCOUNT = os.environ['SNOWSQL_ACCOUNT']
SNOWSQL_USER = os.environ['SNOWSQL_USER']
SNOWSQL_PASSWORD = os.environ['SNOWSQL_PASSWORD']

# -------------------------------
# 2. Connect to Snowflake
# -------------------------------
conn = snowflake.connector.connect(
    user=SNOWSQL_USER,
    password=SNOWSQL_PASSWORD,
    account=SNOWSQL_ACCOUNT,
    warehouse='COMPUTE_WH',
    database='MY_DB',
    schema='PUBLIC'
)
print("✅ Connected to Snowflake")

# -------------------------------
# 3. Create file format & stage (optional, idempotent)
# -------------------------------
with conn.cursor() as cur:
    cur.execute("""
        CREATE OR REPLACE FILE FORMAT my_csv_format
        TYPE = 'CSV'
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        DATE_FORMAT = 'YYYY-MM-DD';
    """)
    print("✅ File format created")

    cur.execute("""
        CREATE OR REPLACE STAGE my_stage
        FILE_FORMAT = my_csv_format;
    """)
    print("✅ Stage created")

# -------------------------------
# 4. Load CSV
# -------------------------------
csv_file = os.path.join(os.getcwd(), 'employees.csv')
df = pd.read_csv(csv_file)

# -------------------------------
# 5. Fix column names to match Snowflake table
# -------------------------------
# Converts 'Name' -> 'NAME', 'Joining Date' -> 'JOINING_DATE', etc.
df.columns = [c.upper().replace(" ", "_") for c in df.columns]

print(f"✅ CSV loaded with {len(df)} rows")

# -------------------------------
# 6. Upload data using write_pandas
# -------------------------------
success, nchunks, nrows, _ = write_pandas(conn, df, 'EMPLOYEES_CICD')
print(f"✅ Uploaded {nrows} rows in {nchunks} chunks: success={success}")