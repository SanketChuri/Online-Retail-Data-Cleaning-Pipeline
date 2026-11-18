from pipeline import extract, transform

df = extract.read_raw_data()
clean_df, rejected, log = transform.clean(df)
print(clean_df.head())
print(rejected["reject_reason"].value_counts())

from pipeline import validate
validate.validate(clean_df)

from pipeline import load
load.save_csv_files(clean_df, rejected)
load.load_to_database(clean_df, rejected, log)