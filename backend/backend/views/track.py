from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from backend.schemas.track import TrackingRequest
# from backend.db_writer import write_event
from backend.kafka_writer import stream_event

@api_view(['POST'])
def track_event(request: Request):
    serializer = TrackingRequest(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    stream_event(data)
    return Response(status=200, data=data)
