import pandas as pd

from pipeline.transform import clean


def make_messy_data():
    return pd.DataFrame({
        "InvoiceNo":   ["1001", "1001", "C1002", "1003", "1004", "1005", "1006", "1007"],
        "StockCode":   ["85123a", "85123a", "85123A", "POST", "22423", "22423", "85123A", "22423"],
        "Description": ["  WHITE HEART  HOLDER ", "  WHITE HEART  HOLDER ", "WHITE HEART HOLDER",
                        "POSTAGE", "CAKESTAND", None, "WHITE HEART HOLDER", "CAKESTAND"],
        "Quantity":    [6, 6, -6, 1, 2, 3, 4, 0],
        "InvoiceDate": ["12/1/2010 8:26"] * 8,
        "UnitPrice":   [2.55, 2.55, 2.55, 18.0, 12.75, 12.75, 2.55, 12.75],
        "CustomerID":  ["17850", "17850", "17850", "12583", None, "13047", "17850", "13047"],
        "Country":     ["United Kingdom", "United Kingdom", "United Kingdom", "France",
                        "EIRE", "United Kingdom", "United Kingdom", "United Kingdom"],
    })


def test_bad_rows_are_rejected_with_reasons():
    clean_df, rejected, _ = clean(make_messy_data())
    reasons = set(rejected["reject_reason"])
    assert {"duplicate_row", "cancelled_order", "non_product_code", "quantity_not_positive"} <= reasons
    assert len(clean_df) + len(rejected) == 8   # nothing lost


def test_text_is_tidied_and_codes_upper_case():
    clean_df, _, _ = clean(make_messy_data())
    assert "WHITE HEART HOLDER" in set(clean_df["description"])
    assert (clean_df["stock_code"] == clean_df["stock_code"].str.upper()).all()


def test_missing_description_filled_from_same_stock_code():
    clean_df, _, _ = clean(make_messy_data())
    assert clean_df["description"].notna().all()


def test_country_fixed_and_missing_customer_kept():
    clean_df, _, _ = clean(make_messy_data())
    assert "Ireland" in set(clean_df["country"])
    assert (~clean_df["has_customer_id"]).sum() == 1


def test_line_total_calculated():
    clean_df, _, _ = clean(make_messy_data())
    row = clean_df[clean_df["invoice_no"] == "1004"].iloc[0]
    assert row["line_total"] == 25.50