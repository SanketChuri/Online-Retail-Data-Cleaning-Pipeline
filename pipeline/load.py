import sqlite3

from pipeline import config


def save_csv_files(clean_df, rejected_df):
    config.CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(config.CLEAN_FILE, index=False)
    rejected_df.to_csv(config.REJECTED_FILE, index=False)
    print(f"  Saved {config.CLEAN_FILE.name} and {config.REJECTED_FILE.name}")


def load_to_database(clean_df, rejected_df, log_df):
    # Start fresh each run, so running twice never loads the data twice
    if config.DATABASE_FILE.exists():
        config.DATABASE_FILE.unlink()

    conn = sqlite3.connect(config.DATABASE_FILE)
    try:
        conn.executescript((config.SQL_DIR / "schema.sql").read_text())

        sales = clean_df.copy()
        sales["invoice_date"] = sales["invoice_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
        sales["has_customer_id"] = sales["has_customer_id"].astype(int)
        sales.to_sql("sales", conn, if_exists="append", index=False)

        # Rejected rows still have the original column names, so rename them
        rejected = rejected_df.rename(columns=str.lower).rename(columns={
            "invoiceno": "invoice_no", "stockcode": "stock_code",
            "invoicedate": "invoice_date", "unitprice": "unit_price",
            "customerid": "customer_id",
        })
        rejected.to_sql("rejected_rows", conn, if_exists="append", index=False)

        log_df.to_sql("pipeline_log", conn, if_exists="append", index=False)
        conn.commit()

        for table in ["sales", "rejected_rows", "pipeline_log"]:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  Loaded {count:>8,} rows into '{table}'")
    finally:
        conn.close()