# Snowflake Backup & Restore Guide

## 1. Time Travel (Native Snowflake Feature)
- **What:** Instantly recover dropped tables or restore to a previous state (up to 1-90 days, depending on your Snowflake edition).
- **How:**
  - To restore a dropped table:
    ```sql
    UNDROP TABLE my_table;
    ```
  - To query a table as of a previous time:
    ```sql
    SELECT * FROM my_table AT (TIMESTAMP => '2024-07-01 12:00:00');
    ```
  - To restore a table to a previous state:
    ```sql
    CREATE OR REPLACE TABLE my_table_restore AS SELECT * FROM my_table AT (TIMESTAMP => '2024-07-01 12:00:00');
    ```

## 2. Manual/Scheduled Exports
- **What:** Export data to S3 or local for backup/archival.
- **How:**
  - Use `COPY INTO` to export data:
    ```sql
    COPY INTO 's3://your-bucket/backups/my_table_' FROM my_table FILE_FORMAT = (TYPE = CSV);
    ```
  - Schedule with Snowflake Tasks or external scheduler (e.g., cron, Airflow).

## 3. Restore from Export
- **How:**
  - Use `COPY INTO` to import data:
    ```sql
    COPY INTO my_table FROM 's3://your-bucket/backups/my_table_' FILE_FORMAT = (TYPE = CSV);
    ```

## 4. Best Practices
- Regularly test restores.
- Use versioned S3 buckets for backup.
- Document backup/restore procedures for your team.

## 5. References
- [Snowflake Time Travel Docs](https://docs.snowflake.com/en/user-guide/data-time-travel)
- [Snowflake Data Export Docs](https://docs.snowflake.com/en/user-guide/data-unload)