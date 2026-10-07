"""Airflow DAG: daily e-commerce sales ETL with basic error handling/logging."""
from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

logger = logging.getLogger(__name__)


def _run_etl(**_context):
    try:
        from etl import run

        run()
        logger.info("ecommerce_sales_etl completed")
    except Exception:
        logger.exception("ecommerce_sales_etl failed")
        raise


default_args = {
    "owner": "aaryan",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_sales_etl",
    default_args=default_args,
    description="Daily e-commerce sales CSV -> PostgreSQL ETL",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "ecommerce"],
) as dag:
    PythonOperator(task_id="run_etl", python_callable=_run_etl)
