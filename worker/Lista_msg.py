import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

# Pega todos os itens da lista "products_queue"
items = redis_client.lrange("product_queue", 0, -1)

# Cada item vem como bytes, precisa decodificar
items = [item.decode("utf-8") for item in items]

print(items)
