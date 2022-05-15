import datetime
import json
from copy import deepcopy
from datetime import timezone
from uuid import uuid4

from chrono.backend.mutations import mutation
from chrono.backend.singletons.db_connector import get_db_connector
from chrono.backend.singletons.mongo import get_mongo_client
from chrono.model.windows_state import WindowsState


@mutation.field("windows_state")
def resolve_window_state(obj, info, state):
    state = WindowsState(**state)
    db_connector = get_db_connector()

    res = db_connector.upsert_windows_state(state)

    previous = db_connector.get_previous_windows_state(state)

    if previous is not None:
        previous.time_delta = (state.timestamp - previous.timestamp.astimezone(timezone.utc)).total_seconds()
        db_connector.upsert_windows_state(previous)


    return res.dict()

# Example
# mutation {
#   windows_state(state: {
#     hostname:"abc",
#     active_window:{
#       name: "w1",
#       process_name: "p",
#       process_id:234,
#       type_:"BaseWindowInfo"
#     },
#     windows:[
#       {
#         name: "w1",
#         process_name: "p",
#         process_id:234,
#         type_:"BaseWindowInfo"
#       }
#     ]
#   }) {
#     id,
#     active_window{
#       name,
#       process_name,
#       url,
#     },
#     timestamp
#   }
# }
