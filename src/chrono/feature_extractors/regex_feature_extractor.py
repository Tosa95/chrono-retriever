import re
from typing import Optional, Dict, Any, List

from chrono.feature_extractors.feature_extractor import FeatureExtractor
from chrono.model.feature_extractors_descriptors import RegexFeatureExtractorDescriptor
from chrono.model.window_info import BaseWindowInfo
from chrono.model.windows_state import WindowsState


class RegexFeatureExtractor(FeatureExtractor):
    def __init__(self, descriptor: RegexFeatureExtractorDescriptor):
        self._descriptor = descriptor

    def apply_regex(self, regex: str, value: str, res: Dict[str, str]) -> bool:
        match = re.search(regex, value, re.RegexFlag.IGNORECASE)

        if match is not None:
            res.update(match.groupdict())
            return True

        return False

    def extract_features(self, windows_state: WindowsState) -> Optional[List[Dict[str, Any]]]:

        res = {}
        accepted = []

        if windows_state.active_window is None:
            return None

        if self._descriptor.file_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.file_re, windows_state.active_window.file, res))
            except AttributeError:
                pass

        if self._descriptor.process_name_re is not None:
            try:
                accepted.append(
                    self.apply_regex(self._descriptor.process_name_re, windows_state.active_window.process_name, res))
            except AttributeError:
                pass

        if self._descriptor.username_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.username_re, windows_state.username, res))
            except AttributeError:
                pass

        if self._descriptor.hostname_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.hostname_re, windows_state.hostname, res))
            except AttributeError:
                pass

        if self._descriptor.branch_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.branch_re, windows_state.active_window.branch, res))
            except AttributeError:
                pass

        if self._descriptor.project_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.project_re, windows_state.active_window.project, res))
            except AttributeError:
                pass

        if self._descriptor.url_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.url_re, windows_state.active_window.url, res))
            except AttributeError:
                pass

        if self._descriptor.name_re is not None:
            try:
                accepted.append(self.apply_regex(self._descriptor.name_re, windows_state.active_window.name, res))
            except AttributeError:
                pass

        if all(accepted):
            return [res]
        else:
            return None


if __name__ == "__main__":
    windows_state = WindowsState(
        windows=[],
        active_window=BaseWindowInfo(
            name="ciao | [DPAIN-1234] | hohoh",
            process_name="pycharm",
            process_id=1,
            type_="BaseWindowInfo"
        ),
        hostname="hihih"
    )

    fe = RegexFeatureExtractor(
        descriptor=RegexFeatureExtractorDescriptor(
            name_re=r"(?P<us_id>(DPAIN|DPADEVOPS|DPAP)-\d+)"
        )
    )

    print(fe.extract_features(windows_state))
