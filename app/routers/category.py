from fastapi.routing import APIRouter 
from fastapi import HTTPException , Path , Body
from typing import List , Annotated

from ..schemas import CategoryResponse , CategoryCreate, CategoryUpdate
from ..database import get_db
from ..models import Category

router = APIRouter(
        tags=['Categories']

)


@router.get('/', response_model=List[CategoryResponse])
def get_categories():
    with get_db() as session:
        return session.query(Category).all()


@router.get('/{category_id}', response_model=CategoryResponse)
def get_one_category(category_id: int = Path(ge=1)):
    with get_db() as session:
        category = session.query(Category).get(category_id)

    if not category:
            raise HTTPException(status_code=404 , detail='category not found')
        
    return category


@router.post('/' , response_model=CategoryCreate)
def create_categories(data: CategoryCreate):
    with get_db() as session:
        exisiting_category = session.query(Category).filter(Category.name==data.name).first()
        if exisiting_category:
            raise HTTPException(status_code=400 , detail='category exists. ')
        
        new_category = Category(name=data.name, description=data.description)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)

        return new_category 
    
@router.put('/{category_id}' , response_model=CategoryResponse)
def update_categories(
    category_id: Annotated[int, Path(ge=1)],
    data: Annotated [CategoryUpdate , Body],
):
    with get_db() as session:
        exisiting_category = session.query(Category).get(category_id)

        if not exisiting_category:
            raise HTTPException(status_code=404 , detail='category not found. ')
        
        if  session.query(Category).filter(Category.name==data.name).first():
            raise HTTPException(status_code=400 , detail='category exists. ')
        
        exisiting_category.name = data.name if data.name else  exisiting_category.name
        exisiting_category.description = data.description if data.description else  exisiting_category.description

        session.commit()
        session.refresh(exisiting_category)

        return exisiting_category 


@router.delete('/{category_id}')
def update_categories(
    category_id: Annotated[int, Path(ge=1)],
):
    with get_db() as session:
        exisiting_category = session.query(Category).get(category_id)

        if not exisiting_category:
            raise HTTPException(status_code=404 , detail='category not found. ')
        
        session.delete(exisiting_category)
        session.commit()

        return {'message': 'deleted'}