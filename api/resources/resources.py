import json
import falcon
from api.schemas.item_schema import ItemSchema
from api.hooks.request_body_validator import validate_req_body


def validate_name(name):
    "Check type of name"
    try:
        float(name)
        return True
    except ValueError:
        return False


items = []


class Item(object):

    post_request_schema = ItemSchema()
    put_request_schema = ItemSchema()

    def on_get(self, req, resp, name):
        """Fetch item called name from items list"""

        item = next(filter(lambda x: x.get("name") == name, items), None)
        resp.body = json.dumps({"item": item}, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        if item:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404  # Not Found

        # req.media will deserialize json object

    @falcon.before(validate_req_body)
    def on_post(self, req, resp, name):
        """Insert item called name into items list"""

        if next(filter(lambda x: x.get("name") == name, items), None):
            message = f"An item with name {name} already exists."
            resp.body = json.dumps({"message": message}, ensure_ascii=False)
            resp.status = falcon.HTTP_400  # Bad Request
        else:
            # data = json.load(req.bounded_stream) #Return type - dict
            # data = req.bounded_stream.read() #Return type - bytes
            # data = json.loads(req.bounded_stream.read()) #Return type - dict
            # data = req.bounded_stream.read().decode("utf-8") #Return type - str
            # data = json.loads(req.bounded_stream.read().decode("utf-8")) #Return type - dict
            if len(name) == 0.0 or validate_name(name):
                msg = "Invalid Request"
                raise falcon.HTTPBadRequest("Bad Request", msg)
            else:
                item = {"name": name, "price": req.context.get("json").get("price")}
                items.append(item)
                resp.body = json.dumps(item, ensure_ascii=False)
                resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, name):
        """Delete item called name from items list"""

        global items
        items = list(filter(lambda x: x.get("name") != name, items))
        resp.body = json.dumps({"message": f"Item {name} deleted"}, ensure_ascii=False)
        resp.status = falcon.HTTP_201

    @falcon.before(validate_req_body)
    def on_put(self, req, resp, name):
        """Insert/Update an item called name into items list"""

        if len(name) == 0.0 or validate_name(name):
            msg = "Invalid Request"
            raise falcon.HTTPBadRequest("Bad Request", msg)
        else:
            data = req.context.get("json")
            item = next(filter(lambda x: x.get("name") == name, items), None)

            if item is None:
                item = {"name": name, "price": data.get("price")}
                items.append(item)
                resp.body = json.dumps({"item": item}, ensure_ascii=False)
                resp.status = falcon.HTTP_201
            else:
                item.update(data)
                resp.body = json.dumps({"item": item}, ensure_ascii=False)
                resp.status = falcon.HTTP_200


class ItemList(object):
    def on_get(self, req, resp):

        resp.body = json.dumps({"items": items}, ensure_ascii=False)
        resp.status = falcon.HTTP_200
