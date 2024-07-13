from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.get("/users/", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	users = crud.get_users(db, skip=skip, limit=limit)
	return users

@app.get("/orders/users/{user_id}", response_model=list[schemas.Order])
async def get_user_orders(user_id: int, db: Session = Depends(get_db)):
	orders = crud.get_orders(db, user_id=user_id)
	return orders
	
@app.post("/users/new")
async def new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	return crud.create_user(db=db, user=user)

@app.post("/product/new")
async def new_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
	if int(product.price) not in range(100, 1000):
		raise HTTPException(
			status_code=400, detail="Price constraint violated"
		)
	return crud.create_product(db=db, product=product)

@app.post("/orders/new/{user_id}/{product_id}")
async def new_order(user_id: int, product_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
	if order.quantity not in range(1,100):
		raise HTTPException(
			status_code=400, detail="Quantity constraint violated"
		)
	return crud.create_order(db=db, order=order, user_id=user_id, product_id=product_id)

@app.delete("/orders/delete/{product_name}/{user_id}/{order_date}")
async def delete_order(user_id: int, product_name: str, order_date: datetime.datetime, db: Session = Depends(get_db)):
	db_order = db.query(models.Order).filter(models.Product.productname == product_name, models.User.id == user_id, models.Order.order_date == order_date).first()
	if db_order is None:
		raise HTTPException(status_code=404, detail="Order Not found")
	crud.delete_order(db=db, order=db_order)
	return {"Message": "Successfully Deleted"}

