import pprint
from copy import deepcopy
from datetime import datetime, timedelta

from chrono.backend.queries import query
from chrono.backend.singletons.db_connector import get_db_connector
from chrono.model.activity_regex_filter import ActivityRegexFilter
from chrono.model.activity_stats import ActivityStats


@query.field("activity_stats")
def resolve_activity_stats(obj, info, from_timestamp: datetime, to_timestamp: datetime,
                          activity_filter: dict):

    activity_filter = ActivityRegexFilter(**activity_filter)
    db_connector = get_db_connector()

    items = list(db_connector.get_windows_states_w_activity_filter(from_timestamp, to_timestamp, activity_filter))

    pprint.pprint([i.active_window for i in items])

    total = sum(i.time_delta for i in items if i.time_delta is not None)
    total_human = str(timedelta(seconds=total))

    return ActivityStats(
        total_time=total,
        total_time_human=total_human,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp
    )

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
