import pandas as pd

# print(df.shape)        # (rows, columns)
# print(df.head())       # first 5 rows
# print(df.dtypes)       # the type of each column
# print(df.isna().sum()) # missing values per column

df = pd.read_csv(
    "data/raw/online_retail.csv",
)

dfCopy = df.copy()
dfCopy[["InvoiceNo", "StockCode", "CustomerID"]] = dfCopy[
    ["InvoiceNo", "StockCode", "CustomerID"]
].astype("string")

# print('duplicated',df.duplicated().sum())  # number of duplicate rows
# print('c', df['InvoiceNo'].str.startswith('C').sum())
# print('quantity < 0', (df['Quantity'] <= 0).sum())
# print('price < 0', (df['UnitPrice'] <= 0).sum())

is_product = dfCopy["StockCode"].str.match(r"^\d{5}")
not_products = dfCopy[~is_product]
print(not_products["StockCode"].unique())


# print(df["Country"].value_counts())
fix_names = {
    "EIRE": "Ireland",
    "RSA": "South Africa",
    "USA": "United States",
}
df["Country"] = df["Country"].replace(fix_names)


names = df["Description"].dropna()
clean_names = names.str.strip()
messy = names != clean_names
# print(messy.sum())


# print((df.groupby("StockCode")["Description"].nunique() > 1).sum())
