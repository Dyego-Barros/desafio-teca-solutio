from infrastructure.repositories.UserReposiories import UserRepositories
from domain.entities.UserEntity import UserEntity as User

class UserService:
    def __init__(self):
        self.user_repo = UserRepositories()
        
        
    def create_user(self, user:User) -> User:
        return self.user_repo.create_user(user)
    
    def get_user_by_email(self, email:str) -> User | None:
        return self.user_repo.get_user_by_email(email)   
    
    def update_user(self, user_id:int, user:User) -> User | None:
        return self.user_repo.update_user(user_id, user)
    
    def delete_user(self, user_id:int, user:User) -> bool:
        return self.user_repo.delete_user(user_id)
    
   