from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

from chrono.model.windows_state import WindowsState


class FeatureExtractor(ABC):

    @abstractmethod
    def extract_features(self, windows_state: WindowsState) -> Optional[List[Dict[str, Any]]]:
        pass