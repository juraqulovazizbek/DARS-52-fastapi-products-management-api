from pydantic import BaseModel, Field

from typing import List , Annotated


class CategoryResponse(BaseModel):
    category_id: int
    name: Annotated [str , Field(max_length=100)]
    description: str | None = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: Annotated[ str, Field(None , min_length=2 , max_length=100)]
    description: Annotated[ str, Field(None, max_length=500)]


class CategoryUpdate(BaseModel):
    name: Annotated[ str, Field(None , min_length=2 , max_length=100)]
    description: Annotated[ str, Field(None, max_length=500)]


class ProductResponse(BaseModel):
    product_id: int
    name: Annotated[str, Field(max_length=100)]
    price: float
    in_stock: bool = False
    category_id: int
    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    category_id: int   # bu yerda product yaratilayotganda qaysi categoriyaga tegishli ekanligini bilgilab ketamiz va productni topishda uzimizga osonroq buladi
    name: Annotated [str, Field(max_length=100)]
    price: float
    in_stock: bool = True

class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=64)
    price: float | None = None
    in_stock: bool | None = None
    category_id: int | None = None  # optional  holatga qarab



