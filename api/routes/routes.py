from api.security.auth import JWTIssuer, JWTDecoder
from api.resources.item import Item, ItemList
from api.resources.user import UserRegister

routes = [
    ("/decoder", JWTDecoder()),
    ("/auth", JWTIssuer()),
    ("/item/{name}", Item()),
    ("/items", ItemList()),
    ("/register", UserRegister())
]
