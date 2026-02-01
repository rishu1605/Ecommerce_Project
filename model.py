from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    user_id: int
    name: str
    username: str
    email: str
    role: str  # 'Buyer', 'Seller', or 'Admin'

@dataclass
class Product:
    product_id: int
    name: str
    price: float
    category: str
    seller_id: int
    manufacturer: str
    description: str
    model_no: str
    year: int
    tech_specs: str
    images: List[str]  # List of Base64 strings
    stock: int = 10

@dataclass
class Order:
    order_id: int
    buyer_id: int
    total_amount: float
    status: str  # 'Pending', 'Shipped', 'Delivered', 'Refunded'
    order_date: datetime
    payment_status: str  # 'Held in Escrow' or 'Released'

@dataclass
class Complaint:
    complaint_id: int
    order_id: int
    user_id: int
    message: str
    status: str = "Open"
    admin_reply: Optional[str] = None