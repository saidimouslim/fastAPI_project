from sqlalchemy.orm import Session
import models, schemas
import datetime


def get_users(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.User).offset(skip).limit(limit).all()

def get_orders(db: Session, user_id: int):
	return db.query(models.Order).filter(models.User.id == user_id).all()

def create_user(db: Session, user: schemas.UserCreate):
	db_user = models.User(email=user.email, full_name=user.fullname, username=user.username)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def create_product(db: Session, product: schemas.ProductCreate):
	db_product = models.Product(productname=product.product_name, price=product.price, is_available=product.is_available)
	db.add(db_product)
	db.commit()
	db.refresh(db_product)
	return db_product

def create_order(db: Session, order: schemas.OrderCreate, user_id: int, product_id: int):
	db_order = models.Order(order_date=order.order_date, quantity=order.quantity, is_delivered=order.is_delivered, user_id=user_id, product_id=product_id)
	db.add(db_order)
	db.commit()
	db.refresh(db_order)
	return db_order



def delete_order(db: Session, order: schemas.Order):
	db.delete(order)
	db.commit()