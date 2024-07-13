from pydantic import BaseModel,EmailStr
import datetime

class OrderBase(BaseModel):
	order_date: datetime.datetime
	quantity: int
	is_delivered: bool
class UserBase(BaseModel):
	username: str
	full_name: str
	email: EmailStr
class ProductBase(BaseModel):
	product_name: str
	price: float
	is_available: bool

class Order(OrderBase):
	id: int
	user_id: int
	product_id: int
	class Config:
		orm_mode = True
class User(UserBase):
	id: int
	class Config:
		orm_mode = True
class Product(ProductBase):
	id: int
	class Config:
		orm_mode = True

class OrderCreate(OrderBase):
	pass
class UserCreate(UserBase):
	orders: list[Order] = []
	pass
class ProductCreate(ProductBase):
	orders: list[Order] = []
	pass