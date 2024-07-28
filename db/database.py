import os

import pandas as pd
from pandas import DataFrame

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


def get_overview_metrics(df: DataFrame) -> dict:
    """
    Get overview metrics for the landing page
    :param df:
    :return:
    """
    total_orders = df.shape[0]
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    profit_ratio = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    start_date = df['Order Date'].min()
    end_date = df['Order Date'].max()

    data = {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_ratio": profit_ratio,
        "start_date": start_date,
        "end_date": end_date,
    }

    return data


if __name__ == '__main__':
    load_data()