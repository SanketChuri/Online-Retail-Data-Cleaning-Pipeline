from pathlib import Path

# Folders (built from this file's location, so it works on any computer)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEAN_DIR = PROJECT_ROOT / "data" / "clean"
REPORTS_DIR = PROJECT_ROOT / "reports"
SQL_DIR = PROJECT_ROOT / "sql"

# Files
RAW_FILE = RAW_DIR / "online_retail.csv"
CLEAN_FILE = CLEAN_DIR / "sales_clean.csv"
REJECTED_FILE = CLEAN_DIR / "rejected_rows.csv"
DATABASE_FILE = PROJECT_ROOT / "data" / "retail.db"

DATA_URL = (
    "https://raw.githubusercontent.com/databricks/Spark-The-Definitive-Guide/"
    "refs/heads/master/data/retail-data/all/online-retail-dataset.csv"
)

# Stock codes that are NOT real products
NON_PRODUCT_CODES = {
    'AMAZONFEE', 'B', 'BANK CHARGES', 'C2', 'CRUK', 'D', 
    'DOT', 'M', 'PADS', 'POST', 'S'
}

GIFT_VOUCHER_PREFIX = "GIFT_"   # gift_0001_20 etc. (upper case after cleaning)

MAX_REASONABLE_QUANTITY = 10_000   # above this = data-entry error

COUNTRY_FIXES = {
    "EIRE": "Ireland",
    "RSA": "South Africa",
    "USA": "United States",
    "Unspecified": "Unknown",
}

DATE_FORMAT = "%m/%d/%Y %H:%M"   # 12/1/2010 8:26


