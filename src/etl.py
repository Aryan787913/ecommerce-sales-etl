"""E-commerce sales ETL: CSV -> clean -> PostgreSQL."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample" / "sales.csv"


def extract(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.drop_duplicates()
    out = out.dropna(subset=["order_id", "order_date", "amount"])
    out["order_date"] = pd.to_datetime(out["order_date"], errors="coerce")
    out = out.dropna(subset=["order_date"])
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
    out = out.dropna(subset=["amount"])
    return out


def load(df: pd.DataFrame, table: str = "sales_orders") -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("Set DATABASE_URL in .env")
    # Example: postgresql://user:pass@localhost:5432/ecommerce
    conn = psycopg2.connect(url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    order_id TEXT PRIMARY KEY,
                    order_date DATE NOT NULL,
                    customer_id TEXT,
                    product_id TEXT,
                    amount NUMERIC NOT NULL,
                    region TEXT
                )
                """
            )
            for _, row in df.iterrows():
                cur.execute(
                    f"""
                    INSERT INTO {table} (order_id, order_date, customer_id, product_id, amount, region)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (order_id) DO UPDATE SET
                        order_date = EXCLUDED.order_date,
                        amount = EXCLUDED.amount
                    """,
                    (
                        str(row["order_id"]),
                        row["order_date"].date(),
                        str(row.get("customer_id", "")),
                        str(row.get("product_id", "")),
                        float(row["amount"]),
                        str(row.get("region", "")),
                    ),
                )
        conn.commit()
    finally:
        conn.close()


def run() -> None:
    raw = extract()
    clean = transform(raw)
    load(clean)
    print(f"Loaded {len(clean)} rows")


if __name__ == "__main__":
    run()
