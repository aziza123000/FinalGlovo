from pydantic import BaseModel
from typing import Optional
from mysite.models import RoleChoices, OrderStatusChoices, CourierStatusChoices
from datetime import date, datetime


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: RoleChoices
    date_registered: date

class UserProfileOutSchema(UserProfileInputSchema):
    id: int
    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    username: str
    password: str


class CategoryInputSchema(BaseModel):
    category_name: str

class CategoryOutSchema(CategoryInputSchema):
    id: int
    class Config:
        from_attributes = True


class StoreInputSchema(BaseModel):
    store_name: str
    store_image: Optional[str] = None
    description: str
    created_date: date
    category_id: int

class StoreOutSchema(StoreInputSchema):
    id: int
    class Config:
        from_attributes = True


class ProductInputSchema(BaseModel):
    product_name: str
    product_image: Optional[str] = None
    product_description: str
    price: int
    quantity: int
    store_id: int

class ProductOutSchema(ProductInputSchema):
    id: int
    class Config:
        from_attributes = True


class OrderInputSchema(BaseModel):
    status: OrderStatusChoices
    delivery_address: str
    created_at: date
    product_id: int
    client_id: int

class OrderOutSchema(OrderInputSchema):
    id: int
    class Config:
        from_attributes = True


class ReviewInputSchema(BaseModel):
    rating: int
    text: str
    created_date: date
    client_id: int
    store_id: Optional[int] = None
    courier_id: Optional[int] = None

class ReviewOutSchema(ReviewInputSchema):
    id: int
    class Config:
        from_attributes = True



class ContactInputSchema(BaseModel):
    contact_name: str
    contact_number: str
    store_id: int

class ContactOutSchema(ContactInputSchema):
    id: int
    class Config:
        from_attributes = True

class AddressInputSchema(BaseModel):
    address_name: str
    store_id: int

class AddressOutSchema(AddressInputSchema):
    id: int
    class Config:
        from_attributes = True



class StoreMenuInputSchema(BaseModel):
    menu_name: str
    store_id: int

class StoreMenuOutSchema(StoreMenuInputSchema):
    id: int
    class Config:
        from_attributes = True



class CourierProfileInputSchema(BaseModel):
    courier_status: CourierStatusChoices
    user_id: int
    current_order_id: Optional[int] = None

class CourierProfileOutSchema(CourierProfileInputSchema):
    id: int
    class Config:
        from_attributes = True