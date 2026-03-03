-- upload_csv.sql
USE WAREHOUSE COMPUTE_WH;
USE DATABASE MY_DB;
USE SCHEMA PUBLIC;

-- Create file format (once)
CREATE OR REPLACE FILE FORMAT my_csv_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  DATE_FORMAT = 'YYYY-MM-DD';

-- Create stage (once)
CREATE OR REPLACE STAGE my_stage
  FILE_FORMAT = my_csv_format;

-- Load data into table
COPY INTO EMPLOYEES_CICD
FROM @my_stage/employees.csv.gz
FILE_FORMAT = (FORMAT_NAME = my_csv_format)
ON_ERROR = 'CONTINUE';