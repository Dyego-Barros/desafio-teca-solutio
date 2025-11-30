import redis
import json
import time
from Database import Database
from Operation import operation_handlers
from datetime import datetime 
import os
db = Database()
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), db=0)
LOG_FILE = "/worker_messages_log.txt"

def execute_worker():
    print("Worker iniciado. Aguardando mensagens...\n")
    
    while True:
        try:
            # Espera por mensagens (bloqueante)
            _, message = redis_client.blpop("product_queue")
            msg = json.loads(message)
            
            operation = msg.get("operation")
            data = msg.get("data")
            
            # Escreve a operação e o data no arquivo
            with open(LOG_FILE, "a") as f:
                f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M')}Operation: {operation}, Data: {data}\n")

            # Cria conexão e cursor **para cada mensagem**
            conn = db.get_session()
            cursor = conn.cursor()
            
            try:
                handler = operation_handlers.get(operation)
                if handler:
                    handler(cursor, data)
                    conn.commit()
                else:
                    print(f"Operação desconhecida: {operation}")
            except Exception as e:
                print("Erro ao processar mensagem:", e)
                conn.rollback()
            finally:
                cursor.close()
                
        
        except redis.exceptions.ConnectionError as e:
            print("Erro de conexão com Redis:", e)
            time.sleep(5)  # espera 5 segundos antes de tentar de novo
        except Exception as e:
            print("Erro inesperado no worker:", e)
            time.sleep(5)  # espera 5 segundos antes de continuar

# Executa o worker
if __name__ == "__main__":
    execute_worker()
