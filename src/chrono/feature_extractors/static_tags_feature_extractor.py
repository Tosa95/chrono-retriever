from typing import Optional, List, Dict, Any

from chrono.feature_extractors.feature_extractor import FeatureExtractor
from chrono.model.feature_extractors_descriptors import StaticTagsFeatureExtractorDescriptor
from chrono.model.windows_state import WindowsState


class StaticTagsFeatureExtractor(FeatureExtractor):

    def __init__(self, descriptor: StaticTagsFeatureExtractorDescriptor):
        self._descriptor = descriptor

    def extract_features(self, windows_state: WindowsState) -> Optional[List[Dict[str, Any]]]:

        return [self._descriptor.static_tags]

