from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime

Base = declarative_base()


class Order(Base):
	__tablename__= "Orders"
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("Users.id"))
	product_id = Column(Integer, ForeignKey("Products.id"))
	order_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
	quantity = Column(Integer, nullable=False)
	is_delivered = Column(Boolean, nullable=False)

	the_order = relationship("User", back_populates="order")
	ordered_product = relationship("Product", back_populates="order")

	__table_args__ = (
           UniqueConstraint("user_id", "product_id" , "order_date", name="unique_constraint"),
                     )

class User(Base):
	__tablename__ = "Users"

	id = Column(Integer, primary_key=True, index=True,autoincrement=True)
	username = Column(String, nullable=False)
	full_name = Column(String, nullable=False)
	email = Column(String, unique=True, index=True)
	order = relationship("Order", back_populates="the_order")

class Product(Base):
	__tablename__ = "Products"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	productname = Column(String, nullable=False)
	price = Column(Double, nullable=False)
	is_available = Column(Boolean, nullable=False)

	order = relationship("Order", back_populates="ordered_product")
	