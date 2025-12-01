from domain.entities.ProductEntity import ProductEntity as Product
from domain.interfaces.IProduct import IProduct
from core.database.Database import Session, Database
from infrastructure.Models.ProductsModel import ProductsModel
from domain.Queue.Queue import Queue

db = Database()

class ProductRepositories(IProduct):
    def __init__(self, db_session = db.get_session()):
        self.db_session = db_session
        self.__queue = Queue()

    def create_product(self, product: Product) -> Product:
        try:
            new_product = ProductsModel(
                nome=product.nome,
                marca=product.marca,
                valor=product.valor,                               
                in_stock=product.in_stock
            )
            
            self.__queue.Queue_publish("create", product.model_dump())
            return Product.model_validate(new_product)
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all_products(self) -> list| None:
        try:
            product = self.db_session.query(ProductsModel).all()
            if product:
                return product
            return None
        except Exception as e:
            raise e
    
    
    def update_product(self, product_id: int, product: Product) -> Product | None:
        try:
            product.id = product_id
            
            self.__queue.Queue_publish("update",product.model_dump())
            return Product.model_validate(product)
        except Exception as e:
            self.db_session.rollback()
            raise e
        
    def delete_product(self, product_id: int) -> bool:
        try:
            self.__queue.Queue_publish("delete", {"id": product_id})
            return True
        except Exception as e:
            self.db_session.rollback()
            raise e