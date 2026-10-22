import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2
)

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    # salt = bcrypt.gensalt()
    hashed_psswd = bcrypt.hashpw(password_bytes, salt)
    hashed_psswd_string = hashed_psswd.decode("utf-8")
    return hashed_psswd_string

def verify_password(password_hash: str, stored_psswd_hash: str) -> bool:
    password_byte = password_hash.encode('utf-8')
    hashed_psswd_byte = stored_psswd_hash.encode('utf-8')
    return bcrypt.checkpw(password_byte, hashed_psswd_byte)