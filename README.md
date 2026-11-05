# Cleaning Bank Marketing Campaign Data

A DataCamp data-cleaning project using **Python**, **pandas**, and **NumPy**. The goal is to standardize the bank marketing dataset and split it into three structured tables suitable for downstream analysis or loading into a PostgreSQL database.

## Project objectives

- Separate client, campaign, and economic indicators into distinct CSV files.
- Apply the required column names, ordering, and data types.
- Normalize categorical values by replacing periods with underscores.
- Convert selected categorical outcome fields into Boolean indicators.
- Build a standardized contact date using day, month, and the project-specified year (2022).
- Validate table schemas and row counts before exporting.

## Output tables

| File | Rows | Columns | Contents |
|---|---:|---:|---|
| `client.csv` | 41,188 | 7 | Client attributes and Boolean credit-default/mortgage indicators |
| `campaign.csv` | 41,188 | 7 | Contact counts, campaign outcomes, and last contact date |
| `economics.csv` | 41,188 | 3 | Consumer price index and three-month Euribor rate |

## Repository structure

```text
.
├── README.md
├── clean_bank_marketing.py
├── requirements.txt
└── .gitignore
```

The original `bank_marketing.csv` dataset is not included. Place the source file in the project directory before running the script. The three generated output CSVs are also excluded from version control by default; the script recreates them locally.

## Run the project

1. Install Python 3.9+.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Put `bank_marketing.csv` beside the script.
4. Run:

   ```bash
   python clean_bank_marketing.py
   ```

The script writes `client.csv`, `campaign.csv`, and `economics.csv` to the current project directory.

## Validation

The script checks the expected column names and order, confirms that each output has the same number of rows as the source, and prints the resulting shapes and data types.

## Tools

- Python
- pandas
- NumPy
- CSV data preparation for a PostgreSQL-ready workflow

## Project context

Completed as part of the DataCamp project **Cleaning Bank Marketing Campaign Data**. The work focuses on data cleaning, schema consistency, type conversion, and export validation rather than predictive modeling.
