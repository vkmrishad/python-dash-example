import os
from typing import List

import pandas as pd
from pandas import DataFrame
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db.model import Order

path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(path, "data", "(GB) Sample - EU Superstore.xls")


def load_data(file_path: str = data_file_path) -> DataFrame:
    """
    Load data from an Excel file
    :param file_path:
    :return:
    """
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Dispatch Date"] = pd.to_datetime(df["Dispatch Date"])
    df = df.sort_values(by="Row ID", ascending=False)

    return df


def save_data(df: DataFrame, file_path: str = data_file_path):
    """
    Save data to an Excel file
    :param df: DataFrame to be saved
    :param file_path: Path to the Excel file
    """
    xls = pd.ExcelFile(file_path)
    df.to_excel(
        file_path, sheet_name=xls.sheet_names[0], index=False, engine="openpyxl"
    )

    print(f"Data saved to {file_path}")


def get_overview_metrics(session: Session) -> dict:
    """
    Get overview metrics from the database
    :param session: SQLAlchemy session object
    :return: Dictionary with metrics
    """
    # Total orders
    total_orders = session.query(func.count(Order.id)).scalar()

    # Total sales
    total_sales = session.query(func.sum(Order.sales)).scalar() or 0.0

    # Total profit
    total_profit = session.query(func.sum(Order.profit)).scalar() or 0.0

    # Profit ratio
    profit_ratio = (total_profit / total_sales * 100) if total_sales != 0 else 0.0

    # Date range
    start_date = session.query(func.min(Order.order_date)).scalar()
    end_date = session.query(func.max(Order.order_date)).scalar()

    data = {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_ratio": profit_ratio,
        "start_date": start_date,
        "end_date": end_date,
    }

    return data


def order_to_dict(orders: List[Order]) -> List[dict]:
    return [
        {
            "id": order.id,
            "order_id": order.order_id,
            "order_date": order.order_date,
            "dispatch_date": order.dispatch_date,
            "delivery_mode": order.delivery_mode,
            "customer_id": order.customer_id,
            "customer_name": order.customer_name,
            "segment": order.segment,
            "city": order.city,
            "state_province": order.state_province,
            "country_region": order.country_region,
            "region": order.region,
            "product_id": order.product_id,
            "category": order.category,
            "sub_category": order.sub_category,
            "product_name": order.product_name,
            "sales": order.sales,
            "quantity": order.quantity,
            "discount": order.discount,
            "profit": order.profit,
        }
        for order in orders
    ]
