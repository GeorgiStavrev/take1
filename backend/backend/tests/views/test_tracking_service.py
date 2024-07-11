import pytest
from unittest.mock import patch
from backend.services.tracking import track
from copy import deepcopy
import arrow

valid_data = {
    "user_id": "5",
    "events": [
        {
            "event": "test",
            "created_at": "2024-06-08T10:00:00Z",
            "properties": [
                {"name": "test_prop1", "value": "99"},
                {"name": "test_prop2", "value": "101"},
            ],
        }
    ],
    "properties": [{"name": "email", "value": "stavrev.georgi@gmail.com"}],
}


def test_track_raises_exception_when_invalid_data():
    with pytest.raises(Exception):
        track("test", {})


@patch("backend.services.tracking.stream_event")
def test_track_calls_stream_event_when_valid_data(stream_event_fn):
    track("test", valid_data)
    expected_data = deepcopy(valid_data)
    expected_data["client_id"] = "test"
    for event in expected_data.get("events", []):
        event["created_at"] = arrow.get(event["created_at"]).datetime
    stream_event_fn.assert_called_once_with(expected_data)
