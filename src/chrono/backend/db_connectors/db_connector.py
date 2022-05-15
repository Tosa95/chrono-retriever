from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterator, Iterable, Optional

from chrono.model.activity_regex_filter import ActivityRegexFilter
from chrono.model.windows_state import WindowsState


class DbConnector(ABC):

    @abstractmethod
    def upsert_windows_state(self, windows_state: WindowsState) -> WindowsState:
        ...

    @abstractmethod
    def get_windows_states(self, from_timestamp: datetime, to_timestamp: datetime, hostname: Optional[str] = None,
                           username: Optional[str] = None) -> Iterable[WindowsState]:
        ...

    @abstractmethod
    def get_windows_states_w_activity_filter(self, from_timestamp: datetime, to_timestamp: datetime,
                                             activity_filter: ActivityRegexFilter) -> Iterable[WindowsState]:
        ...

    def get_previous_windows_state(self, windows_state: WindowsState, delta: timedelta = timedelta(minutes=5)) -> \
            Optional[WindowsState]:

        to_timestamp = windows_state.timestamp - timedelta(milliseconds=1)
        from_timestamp = windows_state.timestamp - delta

        adjacent_states = list(self.get_windows_states(from_timestamp, to_timestamp,
                                                       windows_state.hostname, windows_state.username))

        if len(adjacent_states) > 0:
            return adjacent_states[-1]
        else:
            return None
