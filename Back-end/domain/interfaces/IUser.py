from abc import ABC, abstractmethod
from domain.entities.UserEntity import UserEntity as User

class IUser(ABC):
    """Classe responsável por implementar os contratos da camada de repositório para Usuários"""
    
    @abstractmethod
    def create_user(self,user: User)->User:
        pass
    
    @abstractmethod
    def get_user_by_email(self,email:str)->User | None:
        pass
    
   
    @abstractmethod
    def update_user(self,user_id:int, user:User)->User | None:
        pass
    
    @abstractmethod
    def delete_user(self,user_id:int)->bool:
        pass