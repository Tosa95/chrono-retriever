import os
from datetime import datetime, timedelta
from importlib.abc import Loader
from typing import Optional, List, Dict, Any

import yaml
from pydantic import BaseModel

from chrono.backend.queries import query
from chrono.backend.singletons.db_connector import get_db_connector
from chrono.feature_extractors.factory import build_feature_extractor
from chrono.model.feature_extractors_descriptors import FeatureExtractorDescriptors
from chrono.model.windows_state import WindowsState

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "features_extractors"
)


class WindowsStatesWFeatures(WindowsState):
    features: Optional[List[Dict[str, Any]]]


class AggregationResult(BaseModel):
    name: Optional[str]
    time_delta: float
    time_delta_human: str
    grouped_by: Optional[str]
    sub_aggregations: Optional[List["AggregationResult"]]


def group_by_features(windows_states: List[WindowsStatesWFeatures], group_by: List[str], name: Optional[str] = None) -> \
        Optional[AggregationResult]:
    windows_states_grouped = {}

    while len(windows_states_grouped) == 0 and len(group_by) > 0:

        current_group_by = group_by[0]
        group_by = group_by[1:]

        total_time = 0

        for ws in windows_states:
            for f in ws.features:
                if ws.time_delta is None:
                    continue
                if current_group_by in f:
                    group = windows_states_grouped.get(f[current_group_by], [])
                    group.append(ws)
                    windows_states_grouped[f[current_group_by]] = group
                    total_time += ws.time_delta

        if len(windows_states_grouped) == 0:
            continue

        sub_aggs = []

        for key, windows in windows_states_grouped.items():
            sub_agg = group_by_features(windows, group_by, key)

            if sub_agg is not None:
                sub_aggs.append(sub_agg)

        return AggregationResult(
            name=name,
            grouped_by=current_group_by,
            time_delta=total_time,
            time_delta_human=str(timedelta(seconds=total_time)),
            sub_aggregations=sorted(sub_aggs, key=lambda a: a.time_delta, reverse=True)
        )

    total_time = sum(w.time_delta for w in windows_states if w.time_delta is not None)
    return AggregationResult(
        name=name,
        time_delta=total_time,
        time_delta_human=str(timedelta(seconds=total_time)),
        sub_aggregations=None
    )


@query.field("aggregation")
def resolve_aggregation(obj, info, from_timestamp: datetime, to_timestamp: datetime, feature_extractor: str):
    db_connector = get_db_connector()

    with open(os.path.join(DATA_FOLDER, feature_extractor), "rt") as f:
        fed = FeatureExtractorDescriptors(**yaml.load(f, Loader))
        fe = build_feature_extractor(fed)

    windows_states = db_connector.get_windows_states(from_timestamp, to_timestamp)

    with_features = [WindowsStatesWFeatures(**ws.dict(), features=fe.extract_features(ws)) for ws in windows_states]
    with_features = [x for x in with_features if x.features is not None]

    return group_by_features(with_features, fed.group_by_order).dict(exclude_unset=True,
                                                                    exclude_none=True)

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
