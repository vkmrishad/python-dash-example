from pydantic import BaseModel
from typing import Optional
from datetime import date


class OrderData(BaseModel):
    id: int
    order_id: Optional[str]
    order_date: Optional[date]
    dispatch_date: Optional[date]
    delivery_mode: Optional[str]
    customer_id: Optional[str]
    customer_name: Optional[str]
    segment: Optional[str]
    city: Optional[str]
    state_province: Optional[str]
    country_region: Optional[str]
    region: Optional[str]
    product_id: Optional[str]
    category: Optional[str]
    sub_category: Optional[str]
    product_name: Optional[str]
    sales: Optional[float]
    quantity: Optional[int]
    discount: Optional[float]
    profit: Optional[float]
