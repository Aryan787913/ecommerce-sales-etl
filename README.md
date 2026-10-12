# E-Commerce Sales ETL Pipeline

Personal project: end-to-end ETL that ingests sales CSV data into PostgreSQL, runs on an Apache Airflow DAG, and applies SQL analytics plus data-quality checks.

## Stack
- Python
- PostgreSQL
- Apache Airflow
- SQL (CTEs, window functions)

## What it does
1. Ingests **100,000+ rows** of e-commerce sales data from CSV into PostgreSQL
2. Automates a daily refresh with an Airflow DAG (error handling + logging)
3. Runs revenue-trend analysis with CTEs and window functions
4. Flags nulls, duplicates, and schema violations in data-quality checks

## Results (from `data/sample/sales.csv`)

Ran the quality checks and revenue query logic against the sample CSV on 2026-10-12 (synthetic demo data, not a live retailer).

- Loaded **100,050** rows (unique `order_id`), date range **2025-01-01** to **2025-12-31** (365 days), **5,000** customers, **200** products
- Quality checks: **0** null `order_id`/`amount`, **0** duplicate `order_id`, **0** negative `amount`
- Aggregate `amount` sum: **25,304,089.56** across regions (East / South / North / West roughly balanced)

Sample data is synthetic. Treat these as pipeline proof, not business insights.

## Layout
```
dags/           Airflow DAG definitions
src/            Extract / transform / load scripts
sql/            Analytics and quality-check queries
data/sample/    Sample or anonymized demo data (not production customer data)
```

## Setup (local)
1. Create a PostgreSQL database and set `DATABASE_URL` in `.env`
2. `pip install -r requirements.txt`
3. Place Airflow home and point `AIRFLOW_HOME` at this project (or copy `dags/` into your Airflow dags folder)
4. `airflow dags trigger ecommerce_sales_etl` (after DAG is registered)

## Honesty note
This is a personal / learning project. Sample data may be synthetic or anonymized. Do not treat it as a client or employer deliverable.

## Author
Aaryan Singh — [GitHub](https://github.com/Aryan787913) · [LinkedIn](https://www.linkedin.com/in/aaryansingh-de/)
