import sqlite3

import matplotlib
matplotlib.use("Agg")   # save charts to a file without opening a window
import matplotlib.pyplot as plt
import pandas as pd

from pipeline import config


def _read_queries():
    """Split analysis.sql into (name, sql) pairs using the '-- name:' lines."""
    queries = []
    name, lines = None, []
    for line in (config.SQL_DIR / "analysis.sql").read_text().splitlines():
        if line.startswith("-- name:"):
            if name:
                queries.append((name, "\n".join(lines)))
            name, lines = line.replace("-- name:", "").strip(), []
        elif name:
            lines.append(line)
    if name:
        queries.append((name, "\n".join(lines)))
    return queries


def _to_markdown(df):
    """Turn a DataFrame into a Markdown table that GitHub displays."""
    header = "| " + " | ".join(df.columns) + " |"
    divider = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = []
    for row in df.itertuples(index=False):
        cells = []
        for column, value in zip(df.columns, row):
            if pd.isna(value):
                cells.append("")
            elif pd.api.types.is_integer_dtype(df[column]):
                cells.append(f"{int(value):,}")
            elif pd.api.types.is_float_dtype(df[column]):
                cells.append(f"{value:,.2f}")
            else:
                cells.append(str(value))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, divider] + rows)


def write_quality_report(raw_rows, clean_df, rejected_df, log_df, checks):
    config.REPORTS_DIR.mkdir(exist_ok=True)
    kept = len(clean_df)
    reasons = (rejected_df["reject_reason"].value_counts()
               .rename_axis("reason").reset_index(name="rows"))
    missing_cust = int((~clean_df["has_customer_id"]).sum())
    lines = [
        "# Data Quality Report", "",
        "## Summary", "",
        f"- Raw rows: **{raw_rows:,}**",
        f"- Clean rows kept: **{kept:,}** ({kept / raw_rows:.1%})",
        f"- Rows rejected: **{len(rejected_df):,}** ({len(rejected_df) / raw_rows:.1%})",
        f"- Clean rows with no customer ID (kept): **{missing_cust:,}**", "",
        "## Cleaning steps", "", _to_markdown(log_df), "",
        "## Why rows were rejected", "", _to_markdown(reasons), "",
        "## Checks on the clean data", "",
        "| Check | Result | Detail |", "| --- | --- | --- |",
    ]
    for name, passed, detail in checks:
        lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} | {detail} |")
    (config.REPORTS_DIR / "data_quality_report.md").write_text("\n".join(lines) + "\n")
    print("  Wrote reports/data_quality_report.md")


def write_analysis_report():
    config.REPORTS_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_FILE)
    lines = ["# Analysis Results", "", "![Monthly revenue](monthly_revenue.png)", ""]
    monthly = None
    try:
        for name, sql in _read_queries():
            result = pd.read_sql_query(sql, conn)
            if name == "Revenue by month":
                monthly = result
            lines += [f"## {name}", "", _to_markdown(result), ""]
    finally:
        conn.close()
    (config.REPORTS_DIR / "analysis_results.md").write_text("\n".join(lines))
    print("  Wrote reports/analysis_results.md")
    if monthly is not None:
        _save_monthly_chart(monthly)


def _save_monthly_chart(monthly):
    # Dec 2011 only has data up to the 9th, so mark it as partial
    labels = [m + ("*" if m == "2011-12" else "") for m in monthly["invoice_month"]]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(labels, monthly["revenue_gbp"] / 1000, color="#2b6cb0")
    ax.set_title("Monthly revenue (£ thousands)")
    ax.set_ylabel("£ thousands")
    ax.tick_params(axis="x", rotation=45)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "* Dec 2011 is a partial month (data ends 9 Dec)", fontsize=8, color="grey")
    fig.tight_layout()
    fig.savefig(config.REPORTS_DIR / "monthly_revenue.png", dpi=120)
    plt.close(fig)
    print("  Wrote reports/monthly_revenue.png")