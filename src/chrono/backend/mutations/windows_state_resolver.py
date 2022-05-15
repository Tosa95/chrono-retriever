import datetime
import json
from copy import deepcopy
from uuid import uuid4

from chrono.backend.mutations import mutation
from chrono.backend.singletons.mongo import get_mongo_client
from chrono.model.windows_state import WindowsState


@mutation.field("windows_state")
def resolve_window_state(obj, info, state):
    state = WindowsState(**state, timestamp=datetime.datetime.now())

    mongo_client = get_mongo_client()

    insert_id = mongo_client["chrono"]["windows_states"].insert_one(state.dict()).inserted_id

    print(insert_id)

    res = mongo_client["chrono"]["windows_states"].find_one({"_id": insert_id})
    res["id"] = str(res["_id"])

    return res

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
