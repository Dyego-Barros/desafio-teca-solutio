from core.database.Database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class ProductsModel(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    marca = Column(String, nullable=True)
    valor = Column(Float, nullable=False)
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)
    in_stock = Column(Boolean, default=True)