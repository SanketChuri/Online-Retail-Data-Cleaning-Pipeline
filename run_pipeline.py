"""
Run the whole pipeline:  python run_pipeline.py
Extract -> Transform (clean) -> Validate -> Load -> Report
"""
import time

from pipeline import extract, load, report, transform, validate


def main():
    start = time.time()

    print("\n[1/5] Extract")
    extract.download_raw_data()
    raw_df = extract.read_raw_data()

    print("\n[2/5] Transform (clean)")
    clean_df, rejected_df, log_df = transform.clean(raw_df)

    print("\n[3/5] Validate")
    checks = validate.validate(clean_df)

    print("\n[4/5] Load")
    load.save_csv_files(clean_df, rejected_df)
    load.load_to_database(clean_df, rejected_df, log_df)

    print("\n[5/5] Report")
    report.write_quality_report(len(raw_df), clean_df, rejected_df, log_df, checks)
    report.write_analysis_report()

    print(f"\nDone in {time.time() - start:.1f} seconds.")


if __name__ == "__main__":
    main()