from werkzeug.security import safe_str_cmp
from api.models.user import UserModel

def authenticate_user(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user.username
