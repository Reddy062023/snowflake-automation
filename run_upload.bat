@echo off
REM Stage the CSV file (SnowSQL CLI command)
snowsql -c cicd_snowflake -q "!put file://C:/Users/Geetu/PythonScripts/employees.csv @my_stage auto_compress=true"

REM Run SQL to load CSV into table
snowsql -c cicd_snowflake -f C:/Users/Geetu/PythonScripts/scripts/upload_csv.sql

echo Finished uploading CSV to Snowflake
pause