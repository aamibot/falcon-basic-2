import json
import falcon
from api.schemas.item_schema import ItemSchema
from api.hooks.request_body_validator import validate_req_body
from api.models.item import ItemModel
from db import db


class Item:

    post_request_schema = ItemSchema()
    put_request_schema = ItemSchema()

    def on_get(self, req, resp, name):
        """Fetch item called name from items list"""

        item = ItemModel.find_by_name(name)

        if item:
            resp.body = json.dumps(item.json(), ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"message": "Item not found"}, ensure_ascii=False)
            resp.status = falcon.HTTP_404  # Not Found

        # req.media will deserialize json object

    @falcon.before(validate_req_body)
    def on_post(self, req, resp, name):
        """Insert item called name into items list"""

        if ItemModel.validate_name(name):
            msg = "Invalid Request"
            raise falcon.HTTPBadRequest("Bad Request", msg)

        elif ItemModel.find_by_name(name):
            message = f"An item with name {name} already exists."
            resp.body = json.dumps({"message": message}, ensure_ascii=False)
            resp.status = falcon.HTTP_400  # Bad Request
        else:
            # data = json.load(req.bounded_stream) #Return type - dict
            # data = req.bounded_stream.read() #Return type - bytes
            # data = json.loads(req.bounded_stream.read()) #Return type - dict
            # data = req.bounded_stream.read().decode("utf-8") #Return type - str
            # data = json.loads(req.bounded_stream.read().decode("utf-8")) #Return type - dict

            data = req.context.get("json")
            item = ItemModel(name, data.get("price"), data.get("store_id"))

            try:
                item.save_to_db()
            except Exception as e:
                msg = "An error occured inserting the item"
                raise falcon.HTTPInternalServerError("Internal Server Error", msg)
            else:
                resp.body = json.dumps(
                    {"message": "Item added successfully"}, ensure_ascii=False
                )
                resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, name):
        """Delete item called name from items list"""

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        resp.body = json.dumps({"message": f"Item {name} deleted"}, ensure_ascii=False)
        resp.status = falcon.HTTP_201

    @falcon.before(validate_req_body)
    def on_put(self, req, resp, name):
        """Insert/Update an item called name into items list"""

        if ItemModel.validate_name(name):
            msg = "Invalid Request"
            raise falcon.HTTPBadRequest("Bad Request", msg)
        else:
            data = req.context.get("json")
            item = ItemModel.find_by_name(name)

            if item is None:

                try:
                    item = ItemModel(name, data.get("price"), data.get("store_id"))
                except Exception as e:
                    msg = "An error occured inserting the item"
                    raise falcon.HTTPInternalServerError("Internal Server Error", msg)
                else:
                    resp.body = json.dumps({"item": item.json()}, ensure_ascii=False)
                    resp.status = falcon.HTTP_201
            else:

                try:
                    item.price = data.get("price")
                except Exception as e:
                    msg = "An error occured inserting the item"
                    raise falcon.HTTPInternalServerError("Internal Server Error", msg)
                else:
                    resp.body = json.dumps({"item": item.json()}, ensure_ascii=False)
                    resp.status = falcon.HTTP_200

            item.save_to_db()


class ItemList:
    def on_get(self, req, resp):

        with db.manager.session_scope() as session:
            resp.body = json.dumps(
                {"items": [item.json() for item in session.query(ItemModel).all()]},
                ensure_ascii=False,
            )
            resp.status = falcon.HTTP_200
