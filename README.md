# Desafio Tech Solution

Este projeto é um desafio Full Stack que utiliza **Python**, **Angular**, **Redis**, **PostgreSQL** e **Docker Compose**.  
Ele consiste em:

- Um backend em Python (Flask/FastAPI) que fornece APIs REST.
- Um frontend em Angular que consome essas APIs.
- Um worker que processa tarefas em fila no Redis.
- Banco de dados PostgreSQL para persistência.
- pgAdmin para gerenciamento do banco.
- Redis para fila de mensagens entre backend e worker.

---

## Pré-requisitos

Antes de executar o projeto, você precisa ter instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Clonando o repositório

Clone o projeto e entre no diretório:

```bash
git clone https://github.com/Dyego-Barros/desafio-teca-solutio
cd desafio-teca-solutio
```
---

## Estrutura de diretorios
```
├── Back-end/           # Código do backend Python
├── Front-end/          # Código do frontend Angular
│   └── products-app/
├── Worker/             # Código do worker para processamento de filas Redis
├── docker-compose.yml  # Orquestração dos containers
├── .env                # Variáveis de ambiente
└── README.md
``` 
---
## Criando arquivo .env 

Crie um arquivo '.env' com as variaveis de ambientes que voce ira usar no seu projeto, algo parecido com isso 
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_URL_SQLALCHEMY=
```
---

## Ajuste do docker-compose.yaml

Ajustes Volumes, Rede e varaiveis de ambiente conforme sua necessidade, apos os ajustes e so executar 

```bash
docker-compose up -d
```
 Os conteineres irão subir, assim que finalizar os serviços estarão acessiveis no seu host
