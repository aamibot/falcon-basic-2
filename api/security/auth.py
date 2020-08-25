import json
import jwt
import falcon
from datetime import datetime, timedelta
from api.security.security import authenticate_user
from api.config.main_config import SECRET
from api.schemas.auth_schema import AuthSchema


def _issue(
    claims: dict, expire: datetime = datetime.utcnow() + timedelta(days=5)
) -> str:
    """Create JWT Token"""
    claims["exp"] = expire
    claims["iat"] = datetime.utcnow()
    claims["nbf"] = claims["iat"] - timedelta(seconds=60)
    token = jwt.encode(claims, SECRET, algorithm="HS256")
    return token


class JWTIssuer:
    """Issues JWTs, to authenticated users"""

    schema = AuthSchema()

    def on_post(self, req, resp):
        try:
            username = req.context.get("json").get("username")
            password = req.context.get("json").get("password")

        except AttributeError as e:
            msg = "No Body found"
            raise falcon.HTTPBadRequest("Bad Request", msg)

        else:
            username = authenticate_user(username, password)

            if username:
                resp.body = _issue({"username": username})
            else:
                msg = "Invalid Credentials"
                raise falcon.HTTPBadRequest("Bad Request", msg)


class JWTDecoder:
    """Returns values stored in JWT.
    """

    def on_get(self, req, resp):
        user = req.context["user"]
        resp.body = f'User Found: {user["username"]}'
