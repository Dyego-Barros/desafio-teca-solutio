import bcrypt

class Criptograph:
    """Classe para criptografia de senhas usando bcrypt."""
    @staticmethod
    def hash_password(password: str) -> str:
        """Cria Hash da senha fornecida."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        """Confere senha fornecida com o hash armazenado."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))