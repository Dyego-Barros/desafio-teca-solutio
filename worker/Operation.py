from datetime import datetime
import os

LOG_FILE = f"{os.path.abspath(os.path.dirname(os.path.join(os.path.abspath(__file__))))}/worker_messages_log.txt"

def create_product(cursor, data):
    created_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO public.products 
        (nome, marca, valor, created_at, in_stock) 
        VALUES (%s, %s, %s, %s, %s)
        """,
        (data["nome"], data["marca"], data["valor"], created_at, data["in_stock"])
    )
    print("Produto criado:", data)
     # Escreve a operação e o data no arquivo
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M')} Operation: create, Data: {data}\n")

    cursor.close()


def update_product(cursor, data):
    updated_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cursor.execute(
        """
        UPDATE products 
        SET nome=%s, marca=%s, valor=%s, updated_at=%s, in_stock=%s
        WHERE id=%s
        """,
        (data["nome"], data["marca"], data["valor"], updated_at, data["in_stock"], data["id"])
    )
    print("Produto atualizado:", data)
     # Escreve a operação e o data no arquivo
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M')} Operation: update, Data: {data}\n")

    cursor.close()

def delete_product(cursor, data):
    cursor.execute("SELECT id,nome,marca,valor,created_at,updated_at,in_stock FROM products WHERE id=%s", (data["id"],))
    result = cursor.fetchone()
    print("Produto deletado:",dict(result))
    # Escreve a operação e o data no arquivo
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M')} Operation: delete, Data: {dict(result)}\n")
        
    cursor.execute("DELETE FROM products WHERE id=%s", (data["id"],))
    cursor.close()


# HASHMAP DE OPERAÇÕES
operation_handlers = {
    "create": create_product,
    "update": update_product,
    "delete": delete_product,
}