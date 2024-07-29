from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base


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
