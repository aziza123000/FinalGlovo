from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime

from mysite.database.db import Base


class RoleChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'
    courier = 'courier'


class OrderStatusChoices(str, PyEnum):
    pending = 'pending'
    canceled = 'canceled'
    delivered = 'delivered'


class CourierStatusChoices(str, PyEnum):
    busy = 'busy'
    available = 'available'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)

    courier_profile: Mapped[Optional['CourierProfile']] = relationship(back_populates='user')
    orders: Mapped[List['Order']] = relationship(back_populates='client')
    reviews_as_client: Mapped[List['Review']] = relationship(
        foreign_keys='Review.client_id', back_populates='client'
    )
    reviews_as_courier: Mapped[List['Review']] = relationship(
        foreign_keys='Review.courier_id', back_populates='courier'
    )

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100))

    stores: Mapped[List['Store']] = relationship(back_populates='category', cascade='all, delete-orphan')


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(200))
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship(back_populates='stores')

    contacts: Mapped[List['Contact']] = relationship(back_populates='store', cascade='all, delete-orphan')
    addresses: Mapped[List['Address']] = relationship(back_populates='store', cascade='all, delete-orphan')
    menus: Mapped[List['StoreMenu']] = relationship(back_populates='store', cascade='all, delete-orphan')
    products: Mapped[List['Product']] = relationship(back_populates='store', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(back_populates='store')


class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contact_name: Mapped[str] = mapped_column(String(100))
    contact_number: Mapped[str] = mapped_column(String(20))

    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship(back_populates='contacts')


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address_name: Mapped[str] = mapped_column(String(255))

    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship(back_populates='addresses')


class StoreMenu(Base):
    __tablename__ = 'store_menu'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    menu_name: Mapped[str] = mapped_column(String(100))

    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship(back_populates='menus')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(200))
    product_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    product_description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)

    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship(back_populates='products')

    orders: Mapped[List['Order']] = relationship(back_populates='product')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[OrderStatusChoices] = mapped_column(Enum(OrderStatusChoices), default=OrderStatusChoices.pending)
    delivery_address: Mapped[str] = mapped_column(Text)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship(back_populates='orders')

    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client: Mapped['UserProfile'] = relationship(back_populates='orders')

    courier_orders: Mapped[List['CourierProfile']] = relationship(back_populates='current_order')


class CourierProfile(Base):
    __tablename__ = 'courier_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courier_status: Mapped[CourierStatusChoices] = mapped_column(
        Enum(CourierStatusChoices), default=CourierStatusChoices.available
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship(back_populates='courier_profile')

    current_order_id: Mapped[Optional[int]] = mapped_column(ForeignKey('order.id'), nullable=True)
    current_order: Mapped[Optional['Order']] = relationship(back_populates='courier_orders')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client: Mapped['UserProfile'] = relationship(foreign_keys=[client_id], back_populates='reviews_as_client')

    store_id: Mapped[Optional[int]] = mapped_column(ForeignKey('store.id'), nullable=True)
    store: Mapped[Optional['Store']] = relationship(back_populates='reviews')

    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_profile.id'), nullable=True)
    courier: Mapped[Optional['UserProfile']] = relationship(foreign_keys=[courier_id], back_populates='reviews_as_courier')