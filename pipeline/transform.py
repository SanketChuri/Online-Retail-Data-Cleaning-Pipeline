import pandas as pd
from pipeline import config

class Cleaner:
    """Holds the data while it is cleaned and keeps a log of every step."""

    def __init__(self, df):
        self.df = df.copy()   # copy, so the raw data is never changed
        self.rejected = []    # removed rows go here
        self.log = []  

    def _record(self, step, rows_before, note=""):
        rows_after = len(self.df)
        self.log.append({
            "step": step,
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_removed": rows_before - rows_after,
            "note": note,
        })
        print(f"  {step:<38} {rows_before - rows_after:>8,} removed  -> {rows_after:,} rows")

    def _reject(self, mask, reason, step):
        before = len(self.df)
        bad = self.df[mask].copy()
        bad["reject_reason"] = reason
        self.rejected.append(bad)
        self.df = self.df[~mask]
        self._record(step, before)

# toy = pd.DataFrame({"Item": ["cup", "plate", "bowl", "spoon", "fork"],
#     "Quantity": [6, -2, 3, 0, 10]})

# c = Cleaner(toy)
# c._reject(c.df["Quantity"] <= 0, "quantity_not_positive", "Remove quantity <= 0")

# print(c.df)            # good basket: cup, bowl, fork
# print(c.rejected[0])   # rejected basket: plate, spoon + their reason
# print(c.log)

    def tidy_text(self):
        before = len(self.df)
        self.df["Description"] = (
            self.df["Description"].str.strip().str.replace(r"\s+", " ", regex=True)
        )
        self.df["StockCode"] = self.df["StockCode"].str.strip().str.upper()
        self.df["InvoiceNo"] = self.df["InvoiceNo"].str.strip()
        self.df["Country"] = self.df["Country"].str.strip()
        self._record("Tidy text fields", before, "no rows removed")
        return self

    def standardise_descriptions(self):
        before = len(self.df)
        most_common_name = (
            self.df.dropna(subset=["Description"])
            .groupby("StockCode")["Description"]
            .agg(lambda names: names.value_counts().index[0])
        )
        self.df["Description"] = self.df["StockCode"].map(most_common_name)
        self._record("Standardise product names", before, "one name per stock code")

        # Anything still without a name can't be identified
        self._reject(self.df["Description"].isna(), "missing_description", "Remove rows with no product name")
        return self

    def remove_duplicates(self):
        self._reject(self.df.duplicated(keep="first"), "duplicate_row", "Remove duplicate rows")
        return self

    def remove_cancellations(self):
        mask = self.df["InvoiceNo"].str.startswith("C")
        self._reject(mask, "cancelled_order", "Remove cancelled orders")
        return self

    def remove_non_products(self):
        code = self.df["StockCode"]
        mask = code.isin(config.NON_PRODUCT_CODES) | code.str.startswith(config.GIFT_VOUCHER_PREFIX)
        self._reject(mask, "non_product_code", "Remove non-product codes")
        return self

    def remove_invalid_quantity(self):
        self._reject(self.df["Quantity"] <= 0, "quantity_not_positive", "Remove quantity <= 0")
        return self

    def remove_invalid_price(self):
        self._reject(self.df["UnitPrice"] <= 0, "price_not_positive", "Remove price <= 0")
        return self

    def remove_extreme_quantity(self):
        mask = self.df["Quantity"] > config.MAX_REASONABLE_QUANTITY
        self._reject(mask, "extreme_quantity", "Remove extreme quantities")
        return self

    

    def fix_countries(self):
        before = len(self.df)
        self.df["Country"] = self.df["Country"].replace(config.COUNTRY_FIXES)
        self._record("Fix country names", before, "EIRE -> Ireland, RSA -> South Africa, etc.")
        return self

    def fix_types_and_add_columns(self):
        before = len(self.df)
        df = self.df
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format=config.DATE_FORMAT)
        df["CustomerID"] = df["CustomerID"].str.replace(r"\.0$", "", regex=True)
        df["HasCustomerID"] = df["CustomerID"].notna()
        df["LineTotal"] = (df["Quantity"] * df["UnitPrice"]).round(2)
        df["InvoiceMonth"] = df["InvoiceDate"].dt.strftime("%Y-%m")
        df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
        df["Hour"] = df["InvoiceDate"].dt.hour
        self.df = df
        self._record("Fix data types, add columns", before, "LineTotal, InvoiceMonth, DayOfWeek, Hour")
        return self

    def rename_columns(self):
        self.df = self.df.rename(columns={
            "InvoiceNo": "invoice_no", 
            "StockCode": "stock_code",
            "Description": "description", 
            "Quantity": "quantity",
            "InvoiceDate": "invoice_date", 
            "UnitPrice": "unit_price",
            "CustomerID": "customer_id", 
            "Country": "country",
            "HasCustomerID": "has_customer_id", 
            "LineTotal": "line_total",
            "InvoiceMonth": "invoice_month", 
            "DayOfWeek": "day_of_week", 
            "Hour": "hour",
        }).reset_index(drop=True)
        return self

    def run_all(self):
        (self.tidy_text()
            .standardise_descriptions()
             .remove_duplicates()
             .remove_cancellations()
             .remove_non_products()
             .remove_invalid_quantity()
             .remove_invalid_price()
             .remove_extreme_quantity()
             .fix_countries()
             .fix_types_and_add_columns()
             .rename_columns())
        rejected = pd.concat(self.rejected, ignore_index=True) if self.rejected else pd.DataFrame()
        return self.df, rejected, pd.DataFrame(self.log)


def clean(df):
    """Run every cleaning step. Returns (clean_df, rejected_df, log_df)."""
    return Cleaner(df).run_all()