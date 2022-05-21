import json
import os
from datetime import timedelta
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel
from yaml import Loader

from chrono.feature_extractors.factory import build_feature_extractor
from chrono.model.feature_extractors_descriptors import FeatureExtractorDescriptors
from chrono.model.windows_state import WindowsState


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


if __name__ == "__main__":

    DATA_FILE_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "activities_2022_05_20.json"
    )

    with open(DATA_FILE_PATH, "rt") as f:
        data = json.load(f)

    windows_states = data["data"]["windows_states"]

    for ws in windows_states:
        if ws["active_window"] is not None:
            ws["active_window"]["process_id"] = 0

        ws["windows"] = []

    windows_states = [WindowsState(**ws) for ws in windows_states]

    with open("test.yml", "rt") as f:
        fed = FeatureExtractorDescriptors(**yaml.load(f, Loader))
        fe = build_feature_extractor(fed)

    with_features = [WindowsStatesWFeatures(**ws.dict(), features=fe.extract_features(ws)) for ws in windows_states]
    with_features = [x for x in with_features if x.features is not None]

    print(group_by_features(with_features, fed.group_by_order).json(indent=4, exclude_unset=True,
                                                                    exclude_none=True))
