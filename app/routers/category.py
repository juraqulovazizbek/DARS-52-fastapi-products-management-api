from fastapi.routing import APIRouter 
from fastapi import HTTPException , Path , Body , Depends , status
from typing import List , Annotated
from sqlalchemy.orm import Session

from ..schemas import CategoryResponse , CategoryCreate, CategoryUpdate 
from ..database import get_db
from ..models import Category

router = APIRouter(
        tags=['Categories']

)


@router.get('/', response_model=List[CategoryResponse])
def get_categories(
    session : Annotated[Session , Depends(get_db)],
):
    return session.query(Category).all()


@router.get('/{category_id}', response_model=CategoryResponse)
def get_one_category(
    category_id: Annotated[int, Path(ge=1)],
    session : Annotated[Session , Depends(get_db)],
):
    category = session.query(Category).get(category_id)

    if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND ,
                detail='category not found')
        
    return category


@router.post('/' , response_model=CategoryCreate , status_code=status.HTTP_201_CREATED)
def create_categories(
    data: CategoryCreate,
    session : Annotated[Session , Depends(get_db)]
    ):
    exisiting_category = session.query(Category).filter(Category.name==data.name).first()
    if exisiting_category:
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST ,
        detail=' Category with this name already exists. ')
        
    new_category = Category(name=data.name, description=data.description)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category 
    
@router.put('/{category_id}' , response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_categories(
    category_id: Annotated[int, Path(ge=1)],
    data: Annotated [CategoryUpdate , Body],
    session : Annotated[Session , Depends(get_db)]
):
    exisiting_category = session.query(Category).get(category_id)

    if not exisiting_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail='category not found. ')
        
    if  session.query(Category).filter(Category.name==data.name).first():
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='category exists. ')
        
    exisiting_category.name = data.name if data.name else  exisiting_category.name
    exisiting_category.description = data.description if data.description else  exisiting_category.description

    session.commit()
    session.refresh(exisiting_category)

    return exisiting_category 


@router.delete('/{category_id}' ,status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(
    category_id: Annotated[int, Path(ge=1)],
    session : Annotated[Session , Depends(get_db)],
):
    exisiting_category = session.query(Category).get(category_id)

    if not exisiting_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND ,
            detail='category not found. ')
    
    products = exisiting_category.products.count()
    if products > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail=f'Cannot delete category. {products} products are linked to this category')

    session.delete(exisiting_category)
    session.commit()

    return { "message": "Category deleted successfully"}