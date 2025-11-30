import psycopg2
import os
from pathlib import Path


class Database:
    def __init__(self, host: str=os.environ.get("POSTGRES_URL"), database: str=os.environ.get("POSTGRES_DB"), user: str=os.environ.get("POSTGRES_USER"), password: str=os.environ.get("POSTGRES_PASSWORD"), port: int=(os.environ.get("POSTGRES_PORT"))):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
        return self.connection

    def get_session(self):
        return self.connect()