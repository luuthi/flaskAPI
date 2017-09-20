from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username,password):
    user = UserModel.get_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return {"users": UserModel.get_by_id(user_id)}