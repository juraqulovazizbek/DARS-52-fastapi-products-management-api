from fastapi import FastAPI

from .database import engine, Base
from .models import *
from .routers import category, product 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(category.router, prefix='/api/categories')

app.include_router(product.router, prefix='/api/products') 