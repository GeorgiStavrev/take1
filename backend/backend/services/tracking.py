from backend.kafka_writer import stream_event
from backend.schemas.track import TrackingRequest


def track(username: str, data: dict):
    serializer = TrackingRequest(data=data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    data["client_id"] = username
    stream_event(data)
