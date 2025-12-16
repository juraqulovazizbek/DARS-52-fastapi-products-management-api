from fastapi.routing import APIRouter
from fastapi import HTTPException, Path, Body, Depends, status , Query
from typing import List, Annotated 
from sqlalchemy.orm import Session

from ..schemas import ProductResponse, ProductCreate, ProductUpdate
from ..database import get_db
from ..models import Product , Category

router = APIRouter(
    tags=['Products']
)


@router.get('/', response_model=List[ProductResponse])
def get_products(
    session: Annotated[Session, Depends(get_db)],
):
    return session.query(Product).all()


@router.get('/search', response_model=List[ProductResponse])
def search_products(
    name: Annotated[str, Query(min_length=1)],
    session: Annotated[Session, Depends(get_db)]
):
    result = session.query(Product).filter(Product.name.ilike(f'%{name.lower()}%')).all()
    return result


@router.get('/filter/category', response_model=List[ProductResponse])
def search_products(
    category: Annotated[str, Query(min_length=2)],
    session: Annotated[Session, Depends(get_db)]
):
    category = session.query(Category).filter(Category.name==category).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    
    return category.products


@router.get('/filter/price', response_model=List[ProductResponse])
def search_products(
    session: Annotated[Session, Depends(get_db)],
    min_price: Annotated[float, Query(ge=0)] = None,
    max_price: Annotated[float, Query(ge=0)] = None,
):
    products = session.query(Product)
    if min_price:
        products = products.filter(Product.price >= min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)

    # products = products.order_by(Product.price.asc()) sort uchun

    return products.all()

@router.get('/{product_id}', response_model=ProductResponse)
def get_one_product(
    product_id: Annotated[int, Path(ge=1)],
    session: Annotated[Session, Depends(get_db)],
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='product not found')
    return product


@router.post('/',response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
def create_product(
    data:Annotated [ProductCreate , Body],
    session: Annotated[Session, Depends(get_db)],
):
    category = session.query(Category).get(data.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        ) 
    new_product = Product(
        name = data.name,
        price = data.price,
        category_id = data.category_id,
        in_stock = data.in_stock
    )


    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product


@router.put('/{product_id}',response_model=ProductResponse,status_code=status.HTTP_200_OK)
def update_product(
    product_id: Annotated[int, Path(ge=1)],
    data: Annotated[ProductUpdate, Body],
    session: Annotated[Session, Depends(get_db)],
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )

    if data.name:
        exists = session.query(Product).filter(
            Product.name == data.name,
            Product.product_id != product_id
        ).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Product with this name already exists.'
            )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    session.commit()
    session.refresh(product)

    return product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: Annotated[int, Path(ge=1)],
    session: Annotated[Session, Depends(get_db)],
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )

    session.delete(product)
    session.commit()