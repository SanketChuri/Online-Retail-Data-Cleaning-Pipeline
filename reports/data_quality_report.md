# Data Quality Report

## Summary

- Raw rows: **541,909**
- Clean rows kept: **522,533** (96.4%)
- Rows rejected: **19,376** (3.6%)
- Clean rows with no customer ID (kept): **131,387**

## Cleaning steps

| step | rows_before | rows_after | rows_removed | note |
| --- | --- | --- | --- | --- |
| Tidy text fields | 541,909 | 541,909 | 0 | no rows removed |
| Standardise product names | 541,909 | 541,909 | 0 | one name per stock code |
| Remove rows with no product name | 541,909 | 541,799 | 110 |  |
| Remove duplicate rows | 541,799 | 536,529 | 5,270 |  |
| Remove cancelled orders | 536,529 | 527,278 | 9,251 |  |
| Remove non-product codes | 527,278 | 524,917 | 2,361 |  |
| Remove quantity <= 0 | 524,917 | 523,678 | 1,239 |  |
| Remove price <= 0 | 523,678 | 522,535 | 1,143 |  |
| Remove extreme quantities | 522,535 | 522,533 | 2 |  |
| Fix country names | 522,533 | 522,533 | 0 | EIRE -> Ireland, RSA -> South Africa, etc. |
| Fix data types, add columns | 522,533 | 522,533 | 0 | LineTotal, InvoiceMonth, DayOfWeek, Hour |

## Why rows were rejected

| reason | rows |
| --- | --- |
| cancelled_order | 9,251 |
| duplicate_row | 5,270 |
| non_product_code | 2,361 |
| quantity_not_positive | 1,239 |
| price_not_positive | 1,143 |
| missing_description | 110 |
| extreme_quantity | 2 |

## Checks on the clean data

| Check | Result | Detail |
| --- | --- | --- |
| No missing values in required columns | PASS | all filled |
| No duplicate rows | PASS | 0 duplicates |
| All quantities are positive | PASS | min = 1 |
| All prices are positive | PASS | min = 0.04 |
| No cancelled invoices left | PASS | 0 found |
| Each stock code has one product name | PASS | max names per code = 1 |
| Dates within Dec 2010 - Dec 2011 | PASS | 2010-12-01 to 2011-12-09 |
| line_total = quantity x unit_price | PASS | checked every row |
