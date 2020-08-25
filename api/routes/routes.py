from api.security.auth import JWTIssuer, JWTDecoder
from api.resources.resources import Item, ItemList

routes = [
    ("/decoder", JWTDecoder()),
    ("/auth", JWTIssuer()),
    ("/item/{name}", Item()),
    ("/items", ItemList()),
]
