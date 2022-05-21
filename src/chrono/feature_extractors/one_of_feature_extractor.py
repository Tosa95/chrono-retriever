from typing import List, Optional, Dict, Any

from chrono.feature_extractors.feature_extractor import FeatureExtractor
from chrono.model.windows_state import WindowsState


class OneOfFeatureExtractor(FeatureExtractor):

    def __init__(self, sub_extractors: List[FeatureExtractor], exhaustive: bool = False):
        self._sub_extractors = sub_extractors
        self._exhaustive = exhaustive

    def extract_features(self, windows_state: WindowsState) -> Optional[List[Dict[str, Any]]]:
        res = []

        sub_features = (se.extract_features(windows_state) for se in self._sub_extractors)

        for sf in sub_features:

            if sf is not None:
                for ssf in sf:
                    res.append(ssf)

                if not self._exhaustive:
                    return res

        if len(res) == 0:
            return None

        return res
