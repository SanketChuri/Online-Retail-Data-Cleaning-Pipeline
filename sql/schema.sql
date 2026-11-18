-- Table 1: the clean sales (one row = one product line on an invoice)
CREATE TABLE sales (
    sale_id          INTEGER PRIMARY KEY,   -- unique number for each row (filled in automatically)
    invoice_no       TEXT,
    stock_code       TEXT,
    description      TEXT,
    quantity         INTEGER,
    invoice_date     TEXT,
    unit_price       REAL,
    customer_id      TEXT,                  -- can be empty (guest checkout)
    country          TEXT,
    has_customer_id  INTEGER,               -- 1 = yes, 0 = no
    line_total       REAL,
    invoice_month    TEXT,
    day_of_week      TEXT,
    hour             INTEGER
);

-- Table 2: every row removed during cleaning, with the reason
CREATE TABLE rejected_rows (
    rejected_id    INTEGER PRIMARY KEY,
    invoice_no     TEXT,
    stock_code     TEXT,
    description    TEXT,
    quantity       INTEGER,
    invoice_date   TEXT,
    unit_price     REAL,
    customer_id    TEXT,
    country        TEXT,
    reject_reason  TEXT
);

-- Table 3: row counts before and after each cleaning step
CREATE TABLE pipeline_log (
    log_id        INTEGER PRIMARY KEY,
    step          TEXT,
    rows_before   INTEGER,
    rows_after    INTEGER,
    rows_removed  INTEGER,
    note          TEXT
);