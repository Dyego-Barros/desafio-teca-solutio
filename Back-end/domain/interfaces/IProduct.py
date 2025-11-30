from abc import ABC, abstractmethod

class IProduct(ABC):
    """Classe responsável por implementar os contratos da camada de repositório para Produtos"""
    
    @abstractmethod
    def create_product(self, product_data: dict) -> dict:
        pass
    
    @abstractmethod
    def get_all_products(self) -> list | None:
        pass
    
    @abstractmethod    
    def update_product(self, product_id: int, product_data: dict) -> dict | None:
        pass
    
    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass