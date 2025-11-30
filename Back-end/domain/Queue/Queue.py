import redis
import json
from domain.entities.ProductEntity import ProductEntity as Product
import os

class Queue:
    def __init__(self):
        self.redis_client = redis.Redis(host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT")), db=0)
    
    def Queue_publish(self,operation:str, data:dict):
        message = {
            "operation": operation,
            "data": data
        }
        self.redis_client.rpush('product_queue', json.dumps(message))

