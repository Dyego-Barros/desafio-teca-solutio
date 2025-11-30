from pydantic import BaseModel

class UserEntity(BaseModel):
    id: int | None = None
    username: str
    email: str
    is_active: bool = True
    password: str
    
    model_config ={
        "from_attributes": True
    }