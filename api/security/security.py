from werkzeug.security import safe_str_cmp
from api.model.user import User

def authenticate_user(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user.username
