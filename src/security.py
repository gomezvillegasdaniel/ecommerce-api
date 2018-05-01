from passlib.context import CryptContext
from models.user_model import UserModel


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def hash_password(password):
    return pwd_context.hash(password)


def check_hashed_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and check_hashed_password(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
