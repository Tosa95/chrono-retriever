import os
import pprint
from typing import List, Union, Dict

from pydantic import BaseModel

from chrono.model.activity_regex_filter import ActivityRegexFilter


class AllOfFeatureExtractorDescriptor(BaseModel):
    all_of: List["FeatureExtractorDescriptor"]

    class Config:
        extra = "forbid"


class OneOfFeatureExtractorDescriptor(BaseModel):
    one_of: List["FeatureExtractorDescriptor"]

    class Config:
        extra = "forbid"


class RegexFeatureExtractorDescriptor(ActivityRegexFilter):
    pass

    class Config:
        extra = "forbid"


class StaticTagsFeatureExtractorDescriptor(BaseModel):
    static_tags: Dict[str, str]

    class Config:
        extra = "forbid"


FeatureExtractorDescriptor = Union[
    StaticTagsFeatureExtractorDescriptor,
    RegexFeatureExtractorDescriptor,
    AllOfFeatureExtractorDescriptor,
    OneOfFeatureExtractorDescriptor
]

AllOfFeatureExtractorDescriptor.update_forward_refs()
OneOfFeatureExtractorDescriptor.update_forward_refs()


class FeatureExtractorDescriptors(BaseModel):
    version: str
    feature_extractors: List[FeatureExtractorDescriptor]
    group_by_order: List[str]


if __name__ == "__main__":
    from yaml import load, dump, Loader, Dumper

    with open(os.path.join(os.path.dirname(__file__), "../../../tests/test.yml"), "rt") as f:
        data = load(f, Loader=Loader)

    parsed_data = FeatureExtractorDescriptors(**data)

    pprint.pprint(parsed_data)
