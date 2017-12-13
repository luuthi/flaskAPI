from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username,password):
    user = UserModel.get_by_username(username)
    # if user:
    #     user =UserModel.get_by_email(username)
    if user and safe_str_cmp(user.password, password) and (user.user_status == True):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.get_by_id(user_id)
