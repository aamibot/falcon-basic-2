from api.security.auth import JWTIssuer, JWTDecoder
from api.resources.item import Item, ItemList
from api.resources.user import UserRegister
from api.resources.store import Store, StoreList

routes = [
    ("/decoder", JWTDecoder()),
    ("/auth", JWTIssuer()),
    ("/item/{name}", Item()),
    ("/items", ItemList()),
    ("/register", UserRegister()),
    ("/store/{name}", Store()),
    ("/stores", StoreList()),
]
