from domain.interfaces.IUser import IUser
from core.database.Database import Session, Database
from infrastructure.Models.UserModel import UserModel
from domain.entities.UserEntity import UserEntity as User

db = Database()


class UserRepositories(IUser):
    
    def __init__(self, db_session=db.get_session()):       
        self.db_session = db_session
        
    def create_user(self, user:User) -> User:
        try:
            new_user = UserModel(
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                password=user.password
            )
            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)
            return User.model_validate(new_user)
        except Exception as e:
            print(e)
            self.db_session.rollback()
            raise e
        
    def get_user_by_email(self, email: str) -> User | None:
        try:
            user = self.db_session.query(UserModel).filter(UserModel.email == email).first()
            if user:
                return User.model_validate(user)
            return None
        except Exception as e:
            raise e
        
    def update_user(self, user_id: int, user: User) -> User | None:
        try:
            existing_user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
            if not existing_user:
                return None
            
            existing_user.username = user.username
            existing_user.email = user.email
            existing_user.is_active = user.is_active
            existing_user.password = user.password
            
            self.db_session.commit()
            self.db_session.refresh(existing_user)
            return User.model_validate(existing_user)
        except Exception as e:
            self.db_session.rollback()
            raise e
    
    def delete_user(self, user_id: int) -> bool:
        try:
            existing_user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
            if not existing_user:
                return False
            
            self.db_session.delete(existing_user)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            raise e
    