import falcon
from falcon import API
from api.security.auth import JWTIssuer, JWTDecoder
from api.resources.item import Item, ItemList
from api.resources.user import UserRegister
from api.resources.store import Store, StoreList
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
from falcon_marshmallow import Marshmallow
from api.config.main_config import SECRET


def user_loader(user):
    return {"username": user}


def get_app() -> API:

    auth_backend = JWTAuthBackend(user_loader, SECRET, algorithm="HS256", leeway=30)
    auth_middleware = FalconAuthMiddleware(
        auth_backend,
        exempt_routes=["/auth", "/register"],
        exempt_methods=["HEAD", "OPTIONS"],
    )

    _app = falcon.API(
        middleware=[
            Marshmallow(),
            auth_middleware,
        ]  # middleware=[auth_middleware] - add to enable jwt authentication
    )
    _app.add_route("/decoder", JWTDecoder())
    _app.add_route("/auth", JWTIssuer())
    _app.add_route("/item/{name}", Item())
    _app.add_route("/items", ItemList())
    _app.add_route("/register", UserRegister())
    _app.add_route("/store/{name}", Store())
    _app.add_route("/stores", StoreList())

    return _app
