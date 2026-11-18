import urllib.request
import pandas as pd
from pipeline import config


def download_raw_data():
    """Download the raw file once. Later runs reuse the saved copy."""
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    if config.RAW_FILE.exists():
        print(f"  Raw file already downloaded: {config.RAW_FILE.name}")
        return

    print("  Downloading raw data (about 45 MB)...")
    urllib.request.urlretrieve(config.DATA_URL, config.RAW_FILE)
    print(f"  Saved to {config.RAW_FILE}")


def read_raw_data():
    """Read IDs as text so 'C536379', '85123A' and '17850' stay as they are."""
    df = pd.read_csv(
        config.RAW_FILE,
        dtype={"InvoiceNo": str, "StockCode": str, "CustomerID": str},
    )
    print(f"  Read {len(df):,} rows and {len(df.columns)} columns")
    return df