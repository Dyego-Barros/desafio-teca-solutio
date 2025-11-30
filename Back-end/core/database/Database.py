from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base 
import os

Engine = create_engine(os.environ.get('POSTGRES_URL_SQLALCHEMY'), echo=False)
Session = sessionmaker(bind=Engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = Engine
        self.SessionLocal = Session

    def get_session(self):
        try:
            db = self.SessionLocal()
            return db
        except Exception as e:
            db.rollback()
            (f"Database session error: {e}")
            raise e
            
        finally:
            db.close()

