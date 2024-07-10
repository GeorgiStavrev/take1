from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from backend.schemas.track import TrackingRequest

# from backend.db_writer import write_event
from backend.kafka_writer import stream_event


@api_view(["POST"])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def track_event(request: Request):
    serializer = TrackingRequest(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    data["client_id"] = request.user.username
    stream_event(data)
    return Response(status=200, data=data)
