from fastapi.routing import APIRouter
from fastapi import HTTPException , Path , Body
from typing import List , Annotated

from ..schemas import ProductResponse , ProductCreate , ProductUpdate
from ..database import get_db
from ..models import Product

router = APIRouter(
    tags=['Products']
)


@router.get('/', response_model=List[ProductResponse])
def get_products():
    with get_db() as session:
        return session.query(Product).all()


@router.get('/{product_id}', response_model=ProductResponse)
def get_one_product(product_id: int = Path(ge=1)):
    with get_db() as session:
        product = session.query(Product).get(product_id)

    if not product:
            raise HTTPException(status_code=404 , detail='product not found')
        
    return product


@router.post('/', response_model=ProductResponse)
def create_product(data: ProductCreate):
    with get_db() as session:
        existing_product = session.query(Product).filter(Product.name == data.name).first()
        if existing_product:
            raise HTTPException(status_code=400, detail='Product exists.')

        new_product = Product(
            name=data.name,
            price=data.price,
            in_stock=data.in_stock,
            category_id=data.category_id
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product
@router.put('/{product_id}' , response_model=ProductResponse)
def update_product(
    product_id: Annotated[int, Path(ge=1)],
    data: Annotated [ProductUpdate , Body],
):
    with get_db() as session:
        existing_product = session.query(Product).get(product_id)

        if not existing_product:
            raise HTTPException(status_code=404 , detail='product not found. ')
        
        if data.name and session.query(Product).filter(Product.name==data.name, Product.product_id != product_id).first():
            raise HTTPException(status_code=400 , detail='product exists.')
        
        existing_product.name = data.name if data.name else  existing_product.name
        existing_product.price = data.price if data.price is not None else existing_product.price
        existing_product.in_stock = data.in_stock if data.in_stock is not None else existing_product.in_stock

        session.commit()
        session.refresh(existing_product)

        return existing_product 


@router.delete('/{product_id}')
def delete_product(
    product_id: Annotated[int, Path(ge=1)],
):
    with get_db() as session:
        existing_product = session.query(Product).get(product_id)

        if not existing_product:
            raise HTTPException(status_code=404 , detail='product not found. ')
        
        session.delete(existing_product)
        session.commit()

        return {'message': 'delete_product'}