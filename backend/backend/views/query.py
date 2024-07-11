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
import arrow
from backend.services.querying import query


@api_view(["GET"])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def query_events(request: Request):
    before = arrow.get(request.query_params.get("before"))
    after = arrow.get(request.query_params.get("after"))
    event_name = request.query_params.get("event")

    events = query(request.user.username, event_name, before.datetime, after.datetime)

    data = {"events": events}
    serializer = EventsQueryResponse(data=data)
    if serializer.is_valid():
        return Response(status=200, data=data)
    else:
        return Response(status=500)
