from typing import List

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db.db import engine
from backend.db.models import Event, EventProperty


def query(
    username: str, event_name: str, before: datetime, after: datetime
) -> List[dict]:
    stmt = (
        select(Event)
        .where(
            Event.client_id == username,
            Event.name == event_name,
            Event.created_at >= after,
            Event.created_at <= before,
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
    return events
