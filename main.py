import falcon
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
from falcon_marshmallow import Marshmallow
from api.routes.routes import routes
from api.config.main_config import SECRET


def user_loader(user):
    return {"username": user}


auth_backend = JWTAuthBackend(user_loader, SECRET, algorithm="HS256", leeway=30)
auth_middleware = FalconAuthMiddleware(
    auth_backend,
    exempt_routes=["/auth", "/register"],
    exempt_methods=["HEAD", "OPTIONS"],
)

api = falcon.API(
    middleware=[Marshmallow(), auth_middleware]
)  # middleware=[auth_middleware] - add to enable jwt authentication

for endpoint, _object in routes:
    api.add_route(endpoint, _object)
