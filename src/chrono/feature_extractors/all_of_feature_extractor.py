from copy import deepcopy
from pprint import pprint
from typing import Optional, List, Dict, Any
from unittest.mock import MagicMock

from chrono.feature_extractors.feature_extractor import FeatureExtractor
from chrono.model.window_info import BaseWindowInfo
from chrono.model.windows_state import WindowsState


class AllOfFeatureExtractor(FeatureExtractor):

    def __init__(self, sub_extractors: List[FeatureExtractor]):
        self._sub_extractors = sub_extractors

    def features_permutations(self, subfeatures: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:

        if len(subfeatures) == 0:
            return []

        sf = subfeatures[0]
        subfeatures = subfeatures[1:]

        if len(subfeatures) == 0:
            return sf

        sub_permutations = self.features_permutations(subfeatures)

        res = []
        for feature_dict in sf:
            for sub_feature_dict in sub_permutations:
                feature_dict = deepcopy(feature_dict)
                feature_dict.update(sub_feature_dict)
                res.append(feature_dict)

        return res

    def extract_features(self, windows_state: WindowsState) -> Optional[List[Dict[str, Any]]]:

        subfeatures = [fe.extract_features(windows_state) for fe in self._sub_extractors]

        if any(sf is None for sf in subfeatures):
            return None

        return self.features_permutations(subfeatures)


if __name__ == "__main__":

    mock_feature_extractor_1 = MagicMock(FeatureExtractor)
    mock_feature_extractor_1.extract_features.return_value = [{"t1": "v1", "t2": "v2"}, {"t1": "v1.1", "t2": "v2.1"}]

    mock_feature_extractor_2 = MagicMock(FeatureExtractor)
    mock_feature_extractor_2.extract_features.return_value = [{"t3": "v3", "t4": "v4"}]

    aofe = AllOfFeatureExtractor([mock_feature_extractor_1, mock_feature_extractor_2])

    pprint(aofe.extract_features(WindowsState(
        windows=[],
        active_window=BaseWindowInfo(
            name="ciao | [DPAIN-1234] | hohoh",
            process_name="pycharm",
            process_id=1,
            type_="BaseWindowInfo"
        ),
        hostname="hihih"
    )))
