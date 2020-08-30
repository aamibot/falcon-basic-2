import falcon
import json
from api.schemas.auth_schema import AuthSchema
from api.hooks.request_body_validator import validate_req_body
from api.models.user import UserModel


class UserRegister(object):

    schema = AuthSchema()

    @falcon.before(validate_req_body)
    def on_post(self, req, resp):

        data = req.context.get("json")

        if UserModel.find_by_username(data.get("username")):
            payload = {
                "message": f"User with username:{data.get('username')} already exists"
            }
            resp.body = json.dumps(payload, ensure_ascii=False)
            resp.status = falcon.HTTP_400
        else:

            user = UserModel(**data)
            user.save_to_db()

            payload = {"message": "User created sucessfully"}
            resp.body = json.dumps(payload, ensure_ascii=False)
            resp.status = falcon.HTTP_201
