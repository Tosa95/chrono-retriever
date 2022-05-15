import datetime
from datetime import timezone

from ariadne import ScalarType

timestamp = ScalarType("Timestamp")


@timestamp.serializer
def serialize_datetime(value: datetime):
    return value.astimezone(timezone.utc).isoformat()


@timestamp.value_parser
def parse_datetime_value(value):
    # dateutil is provided by python-dateutil library
    return datetime.datetime.fromisoformat(value).astimezone(timezone.utc)
