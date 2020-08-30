from marshmallow import fields, Schema


class ItemSchema(Schema):

    price = fields.Float(required=True)
    store_id = fields.Integer(required=True)
