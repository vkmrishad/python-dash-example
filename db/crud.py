import os

import pandas as pd
from pandas import DataFrame

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, Date, func
from sqlalchemy.ext.declarative import declarative_base

path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(path, 'data', '(GB) Sample - EU Superstore.xls')


def load_data(file_path: str = data_file_path) -> DataFrame:
    """
    Load data from an Excel file
    :param file_path:
    :return:
    """
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Dispatch Date'] = pd.to_datetime(df['Dispatch Date'])
    df = df.sort_values(by='Row ID', ascending=False)

    return df


def save_data(df: DataFrame, file_path: str = data_file_path):
    """
    Save data to an Excel file
    :param df: DataFrame to be saved
    :param file_path: Path to the Excel file
    """
    xls = pd.ExcelFile(file_path)
    df.to_excel(file_path, sheet_name=xls.sheet_names[0], index=False, engine='openpyxl')

    print(f'Data saved to {file_path}')


Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_id = Column(String, nullable=True)
    order_date = Column(Date, nullable=True)
    dispatch_date = Column(Date, nullable=True)
    delivery_mode = Column(String, nullable=True)
    customer_id = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    segment = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state_province = Column(String, nullable=True)
    country_region = Column(String, nullable=True)
    region = Column(String, nullable=True)
    product_id = Column(String, nullable=True)
    category = Column(String, nullable=True)
    sub_category = Column(String, nullable=True)
    product_name = Column(String, nullable=True)
    sales = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    discount = Column(Float, nullable=True)
    profit = Column(Float, nullable=True)


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


def get_orders(session: Session, limit: int = 10, offset: int = 0) -> list:
    """
    Get a list of orders from the database
    :param session: SQLAlchemy session object
    :param limit: Number of records to return
    :param offset: Number of records to skip
    :return: List of orders
    """
    orders = session.query(Order).limit(limit).offset(offset).all().order_by(Order.id.desc())

    return orders
