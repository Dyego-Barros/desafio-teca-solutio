from domain.entities.ProductEntity import ProductEntity as Product
from infrastructure.repositories.ProductRepositories import ProductRepositories
from flask import jsonify

class ProductService:
    def __init__(self):
        self.product_repo = ProductRepositories()
        
    def create_product(self, product: Product) -> Product:
        return self.product_repo.create_product(product)
    
    def get_all_products(self) -> list | None:
        return self.product_repo.get_all_products()  
    
    
    def update_product(self, product_id: int, product: Product) -> Product | None:
        return self.product_repo.update_product(product_id, product)
    
    def delete_product(self, product_id: int) -> bool:
        return self.product_repo.delete_product(product_id)