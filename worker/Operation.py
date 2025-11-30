from datetime import datetime

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
    cursor.close()

def delete_product(cursor, data):
    cursor.execute("DELETE FROM products WHERE id=%s", (data["id"],))
    print("Produto deletado:", data)
    cursor.close()


# HASHMAP DE OPERAÇÕES
operation_handlers = {
    "create": create_product,
    "update": update_product,
    "delete": delete_product,
}