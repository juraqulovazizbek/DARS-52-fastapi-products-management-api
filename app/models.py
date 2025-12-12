from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .database import Base


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column( 'id', Integer, primary_key=True)
    name = Column('name', String(100), unique=True, nullable=False)
    description = Column('description',Text)

    products = relationship('Product', back_populates='category')

    def __str__(self):
        return self.name   

    def __repr__(self):
        return self.name
    

class Product(Base):
    __tablename__ = 'products'

    product_id = Column('id', Integer, primary_key=True)
    name = Column('name', String(length=64), nullable=False)
    price = Column('price', Float, nullable=False)
    in_stock = Column('in_stock', Boolean, nullable=False, default=True)
    category_id = Column('category_id', Integer, ForeignKey('categories.id' , ondelete='CASCADE'))


    category = relationship('Category', back_populates='products')

    def __str__(self):
        return self.name   

    def __repr__(self):
        return self.name
    
