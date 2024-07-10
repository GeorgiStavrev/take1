from rest_marshmallow import Schema, fields
from backend.schemas.track import Event


class EventsQueryResponse(Schema):
    events = fields.List(fields.Nested(Event))
