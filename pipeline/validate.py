def run_checks(df):
    """Return a list of (check_name, passed, detail)."""
    required = ["invoice_no", "stock_code", "description", "quantity",
                "invoice_date", "unit_price", "country"]
    checks = []

    def add(name, passed, detail):
        checks.append((name, bool(passed), detail))

    nulls = df[required].isna().sum()
    add("No missing values in required columns", nulls.sum() == 0, "all filled" if nulls.sum() == 0 else nulls[nulls > 0].to_dict())

    dups = df.duplicated().sum()
    add("No duplicate rows", dups == 0, f"{dups} duplicates")

    add("All quantities are positive", (df["quantity"] > 0).all(), f"min = {df['quantity'].min()}")
    add("All prices are positive", (df["unit_price"] > 0).all(), f"min = {df['unit_price'].min()}")

    cancelled = df["invoice_no"].str.startswith("C").sum()
    add("No cancelled invoices left", cancelled == 0, f"{cancelled} found")

    names_per_code = df.groupby("stock_code")["description"].nunique().max()
    add("Each stock code has one product name", names_per_code == 1,f"max names per code = {names_per_code}")

    start, end = df["invoice_date"].min(), df["invoice_date"].max()
    add("Dates within Dec 2010 - Dec 2011", start.year >= 2010 and end.year <= 2011,f"{start:%Y-%m-%d} to {end:%Y-%m-%d}")

    totals_ok = ((df["quantity"] * df["unit_price"]).round(2) == df["line_total"]).all()
    add("line_total = quantity x unit_price", totals_ok, "checked every row")

    return checks


def validate(df):
    checks = run_checks(df)
    for name, passed, detail in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}  ({detail})")

    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise ValueError(f"Data quality checks failed: {failed}")
    return checks


import pandas as pd

toy = pd.DataFrame({
    "invoice":     ["1001", "1001"],
    "stock_code":  ["22423", "22423"],
    "description": ["REGENCY CAKESTAND 3 TIER", "REGENCY CAKESTND 3 TIER"],  # one typo
    "qty":         [2, 2],
})

print("Duplicates BEFORE fixing names:", toy.duplicated().sum())   # 0  -> both rows survive

# Fix the name, like standardise_descriptions does
toy["description"] = "REGENCY CAKESTAND 3 TIER"

print("Duplicates AFTER fixing names:", toy.duplicated().sum())    # 1  -> a new duplicate appeared!