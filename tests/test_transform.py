import pandas as pd

from pipeline import transform


def make_row(description, quantity=2):
    return {
        "InvoiceNo": "1001",
        "StockCode": "22423",
        "Description": description,
        "Quantity": quantity,
        "InvoiceDate": "12/1/2010 8:26",
        "UnitPrice": 12.75,
        "CustomerID": "17850",
        "Country": "United Kingdom",
    }


def test_typo_duplicates_are_caught_after_names_are_standardised():
    # Rows that differ only by a typo are not duplicates in the raw data...
    raw = pd.DataFrame([
        make_row("REGENCY CAKESTAND 3 TIER"),
        make_row("REGENCY CAKESTAND 3 TIER"),
        make_row("REGENCY CAKESTND 3 TIER"),   # same product, one typo
    ])
    assert raw.duplicated().sum() == 1

    # ...but once names are standardised, the typo row becomes a duplicate too.
    # This only works because remove_duplicates runs AFTER standardise_descriptions.
    clean_df, rejected, _ = transform.clean(raw)

    assert len(clean_df) == 1
    assert clean_df["description"].iloc[0] == "REGENCY CAKESTAND 3 TIER"
    assert (rejected["reject_reason"] == "duplicate_row").sum() == 2
