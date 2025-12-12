from fastapi import FastAPI

from .database import engine, Base
from .models import Category, Product
from .routers import category, product 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(
    category.router,
    prefix='/categories'
    )
app.include_router(
    product.router,
    prefix='/products'
)