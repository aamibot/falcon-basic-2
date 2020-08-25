from falcon.errors import HTTPBadRequest


def validate_req_body(req, resp, resource, params):
    if "json" not in req.context:
        msg = "Empty response body. A valid JSON document is required."
        raise HTTPBadRequest("Bad request", msg)
