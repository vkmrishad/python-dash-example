import os

import pandas as pd
from loguru import logger

from src.db.connection import SessionLocal
from src.db.model import Order
from src.db.schema import OrderData


def load_data_to_db(file_path: str):
    # Read Excel file
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Dispatch Date'] = pd.to_datetime(df['Dispatch Date'])
    df = df.sort_values(by='Row ID', ascending=True)

    # Start logging
    logger.info("Starting data load to database...")

    # Validate data and prepare for insertion
    valid_data = []
    for _, row in df.iterrows():
        logger.info(f"Processing row: {row['Row ID']}")
        try:
            order = OrderData(
                id=int(row['Row ID']),
                order_id=str(row['Order ID']),
                order_date=pd.to_datetime(row['Order Date']).date(),
                dispatch_date=pd.to_datetime(row['Dispatch Date']).date(),
                delivery_mode=str(row['Delivery Mode']),
                customer_id=str(row['Customer ID']),
                customer_name=str(row['Customer Name']),
                segment=str(row['Segment']),
                city=str(row['City']),
                state_province=str(row['State/Province']),
                country_region=str(row['Country/Region']),
                region=str(row['Region']),
                product_id=str(row['Product ID']),
                category=str(row['Category']),
                sub_category=str(row['Sub-Category']),
                product_name=str(row['Product Name']),
                sales=float(row['Sales']),
                quantity=int(row['Quantity']),
                discount=float(row['Discount']),
                profit=float(row['Profit'])
            )
            valid_data.append(order.dict())
        except Exception as e:
            logger.error(f"Error validating row: {e}")

    logger.info(f"Data validation complete. {len(valid_data)} rows are valid.")

    # Insert data into database
    session = SessionLocal()
    try:
        logger.info("Inserting data into database...")
        for data in valid_data:
            logger.info(f"Inserting row: {data['id']}")
            order = Order(**data)
            session.add(order)
        session.commit()
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        session.rollback()
    finally:
        session.close()

    logger.info("Data load to database complete.")


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(path, 'data', '(GB) Sample - EU Superstore.xls')
    load_data_to_db(data_file_path)
