from marshmallow import fields, Schema


class AuthSchema(Schema):

    username = fields.Str(required=True)
    password = fields.Str(required=True)
