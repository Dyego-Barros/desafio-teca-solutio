from pydantic import BaseModel

class ProductEntity(BaseModel):
    id: int | None = None
    nome: str
    marca: str 
    valor: float
    updated_at: str | None = None
    created_at: str | None = None
    in_stock: bool = True
    
    model_config ={
        "from_attributes": True
    }