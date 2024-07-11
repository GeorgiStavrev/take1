import pytest
from unittest.mock import patch, ANY
from backend.services.querying import query
from datetime import datetime


@patch("backend.services.querying.Session.execute")
@patch("backend.services.querying.engine")
def test_query_calls_execute(engine, execute):
    username = "test"
    event_name = "My_event"
    before = datetime.now()
    after = datetime.now()
    query(username, event_name, before, after)

    expected_stmt = """SELECT DISTINCT user_events.id, user_events.client_id, user_events.user_id, user_events.name, user_events.created_at, user_events.processed_at 
FROM user_events JOIN user_event_properties ON user_events.id = user_event_properties.event_id 
WHERE user_events.client_id = :client_id_1 AND user_events.name = :name_1 AND user_events.created_at >= :created_at_1 AND user_events.created_at <= :created_at_2"""

    execute.assert_called_once_with(statement=ANY)
    kwargs = execute.call_args.kwargs
    assert "statement" in kwargs
    assert str(kwargs["statement"]) == expected_stmt


@patch("backend.services.querying.Session.execute")
@patch("backend.services.querying.engine")
def test_query_raises_exception(engine, execute):
    username = "test"
    event_name = "My_event"
    with pytest.raises(Exception):
        query(username, event_name, None, None)
