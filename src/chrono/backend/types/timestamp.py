import datetime

from ariadne import ScalarType

timestamp = ScalarType("Timestamp")


@timestamp.serializer
def serialize_datetime(value):
    return value.isoformat()


@timestamp.value_parser
def parse_datetime_value(value):
    # dateutil is provided by python-dateutil library
    return datetime.datetime.fromisoformat(value)
