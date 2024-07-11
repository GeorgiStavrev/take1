from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from backend.services.tracking import track


@api_view(["POST"])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def track_event(request: Request):
    track(request.user.username, request.data)
    return Response(status=200)
