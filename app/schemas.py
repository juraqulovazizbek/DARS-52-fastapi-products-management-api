from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    category_id: int
    name: str = Field(max_length=100)
    description: str | None = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None


# Product

class ProductResponse(BaseModel):
    product_id: int
    name: str = Field(max_length=64)
    price: float
    in_stock: bool = False
    category_id: int    # qaysi categoryga tegishli ekanligini kurish uchun

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str = Field(max_length=64)
    price: float
    in_stock: bool = False
    category_id: int   # bu yerda product yaratilayotganda qaysi categoriyaga tegishli ekanligini bilgilab ketamiz va productni topishda uzimizga osonroq buladi

class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=64)
    price: float | None = None
    in_stock: bool | None = None
    category_id: int | None = None  # optional  holatga qarab
