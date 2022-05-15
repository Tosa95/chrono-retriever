import pprint
from copy import deepcopy
from datetime import datetime

from chrono.backend.queries import query
from chrono.backend.singletons.db_connector import get_db_connector


@query.field("windows_states")
def resolve_window_states(obj, info, from_timestamp: datetime, to_timestamp: datetime):
    db_connector = get_db_connector()

    items = db_connector.get_windows_states(from_timestamp, to_timestamp)

    return [i.dict() for i in items]

# Example
# {
#   windows_states(from_timestamp:"2022-05-14T23:08:00+02:00", to_timestamp: "2022-05-15T00:00:00") {
#     active_window {
#       name
#       process_name
#       url
#       type_
#       project
#       file
#     }
#     timestamp
#     hostname
#   }
# }
