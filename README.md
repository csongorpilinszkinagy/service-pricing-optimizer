# Service Pricing Optimizer

A small data analysis project that explores the relationship between service pricing and revenue,
based on historical, customer-level usage data.  
The goal is to identify **optimal price to maximize revenue** using observed behavior rather than
theoretical demand assumptions.

## Clean and anonymize

### Input format
Raw CSV files are wide-format timesheets:
- one row per customer
- one column per date
- values represent hours worked

Example (simplified):

| Customer | Price  | 2024-01-10 | 2024-01-17 |
|----------|--------|------------|------------|
| Alice    | 9000   | 2          | 1          |
| Brian    | 11000  | 1          | 0          |

### Processing steps
- Drops irrelevant billing and address fields
- Renames columns for internal consistency
- Anonymizes customers using a salted SHA-256 hash

### Output
A unified anonymized minimal wide table in data/processed/clean_anonymized.csv

## Reshape wide to long

### Input format
Example (simplified):

| cursomer_id | price  | 2024-01-10 | 2024-01-17 |
|----------|--------|------------|------------|
| a9f31c2e    | 9000   | 2          | 1          |
| f31aa812    | 11000  | 1          | 0          |

### Processing steps
- Converts wide date columns into event-level rows
- Filters out zero or missing hours

### Output
A normalized, event-level dataset, saved to data/processed/long_format.csv

Example (simplified):

| customer_id | date       | price | hours |
|------------|------------|-------|--------|
| a9f31c2e   | 2024-01-10 | 9000  | 2      |
| a9f31c2e   | 2024-01-17 | 9000  | 1      |
| f31aa812   | 2024-01-10 | 11000 | 1      |

## Optimize revenue

### Feature engineering
- Revenue is calculated as `price × hours`
- Each event is assigned to a calendar quarter
- Data is aggregated per customer per quarter

Resulting analytical table:

| customer_id | quarter | total_hours | total_revenue | avg_price |
|------------|---------|-------------|---------------|-----------|
| a9f31c2e   | Q1      | 12          | 108000        | 9000      |
| f31aa812   | Q1      | 6           | 66000         | 11000     |

### Pricing model
For each quarter:
- A quadratic curve is fitted between average price and total revenue
- This reflects the intuition that:
  - prices that are too low limit revenue
  - prices that are too high reduce demand
- If a clear maximum exists, the analytical optimum is used
- Otherwise, the price with the best observed revenue is selected as a fallback

### Output
- Printed optimal price and predicted revenue per quarter
- Scatter plot of observed prices vs revenue
- Fitted revenue curve and highlighted optimal price
- One PNG chart per quarter

## Reproducibility
Raw csv data in folder:

`data/raw/...`

Install requirements:

`pip install -r requirements.txt`

Run data cleaning:

`python clean_anonymize.py`

Cleaned data in csv:

`data/processed/clean_anonymized.csv`

Run transform:

`python reshape_wide_to_long.py`

Transformed data in csv:

`data/processed/long_format.csv`

Run transform:

`python optimize_revenue.py`

Results in folder

`pics/...`

## Possible Extensions
- Elasticity estimation using log-log models
- Packaging the pipeline as a reusable pricing module
