from rest_marshmallow import Schema, fields


class Property(Schema):
    name = fields.String()
    value = fields.String()


class Event(Schema):
    event = fields.String()
    properties = fields.List(fields.Nested(Property), required=False)
    created_at = fields.DateTime()


class TrackingRequest(Schema):
    client_id = fields.String()
    user_id = fields.String()
    events = fields.List(fields.Nested(Event), required=False)
    properties = fields.List(fields.Nested(Property))
