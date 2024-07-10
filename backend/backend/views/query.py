from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from backend.schemas.query import EventsQueryResponse
from backend.db.db import engine
from backend.db.models import Event, EventProperty
import arrow
from sqlalchemy import select
from sqlalchemy.orm import Session
import json
from backend.serialization import json_serial


@api_view(["GET"])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def query_events(request: Request):
    before = arrow.get(request.query_params.get("before"))
    after = arrow.get(request.query_params.get("after"))
    event_name = request.query_params.get("event")
    stmt = (
        select(Event)
        .where(
            Event.client_id == request.user.username,
            Event.name == event_name,
            Event.created_at >= after.datetime,
            Event.created_at <= before.datetime,
        )
        .join(EventProperty)
        .distinct()
    )
    events = []
    with Session(engine) as session:
        result = session.execute(statement=stmt)
        events = []
        results = result.all()
        for result in results:
            result_dict = result._asdict()
            event = result_dict["Event"]
            event_dict = event._asdict()

            final_dict = {}
            final_dict["properties"] = []
            for prop in event.properties:
                prop_dict = prop._asdict()
                prop_dict.pop("id")
                prop_dict.pop("event_id")

            final_dict["event"] = event_dict["name"]
            final_dict["properties"].append(prop_dict)
            final_dict["created_at"] = event_dict["created_at"].strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            events.append(final_dict)

    data = {"events": events}
    serializer = EventsQueryResponse(data=data)
    if serializer.is_valid():
        return Response(status=200, data=data)
    else:
        return Response(status=500)
