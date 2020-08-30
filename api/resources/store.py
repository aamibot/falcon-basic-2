import json
import falcon
from api.schemas.item_schema import ItemSchema
from api.hooks.request_body_validator import validate_req_body
from api.models.store import StoreModel
from db import db


class Store:
    def on_get(self, req, resp, name):

        store = StoreModel.find_by_name(name)
        if store:
            resp.body = json.dumps(store.json(), ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"message": "Store not found"}, ensure_ascii=False)
            resp.status = falcon.HTTP_404

    def on_post(self, req, resp, name):

        if StoreModel.validate_name(name):
            msg = "Invalid Request"
            raise falcon.HTTPBadRequest("Bad Request", msg)

        elif StoreModel.find_by_name(name):
            message = f"A store with name {name} already exists."
            resp.body = json.dumps({"message": message}, ensure_ascii=False)
            resp.status = falcon.HTTP_400  # Bad Request
        else:
            data = req.context.get("json")
            store = StoreModel(name)

            try:
                store.save_to_db()
            except Exception as e:
                msg = "An error occured inserting the store"
                raise falcon.HTTPInternalServerError("Internal Server Error", msg)
            else:
                resp.body = json.dumps(
                    {"message": "Store added successfully"}, ensure_ascii=False
                )
                resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, name):

        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        resp.body = json.dumps({"message": f"Store {name} deleted"}, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class StoreList:
    def on_get(self, req, resp):

        with db.manager.session_scope() as session:
            resp.body = json.dumps(
                {"stores": [store.json() for store in session.query(StoreModel).all()]},
                ensure_ascii=False,
            )
            resp.status = falcon.HTTP_200
