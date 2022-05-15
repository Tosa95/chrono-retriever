import os
from typing import Optional

import pygetwindow as gw
import socket

from datetime import datetime, tzinfo, timezone
from pygetwindow import BaseWindow

from src.chrono.model.window_info import WindowInfo, BaseWindowInfo
from src.chrono.model.windows_state import WindowsState
from src.chrono.retrievers.window_specializer import BaseWindowSpecializer


class WindowsStateRetriever:

    def __init__(self, specializer: BaseWindowSpecializer):
        self._specializer = specializer

    def _prepare_window(self, w: BaseWindow) -> Optional[WindowInfo]:
        if w is None:
            return None

        window_info = BaseWindowInfo(
            name=w.title,
            process_name=w.process.name(),
            process_id=w.process.pid
        )

        if self._specializer.applies_to(window_info):
            window_info = self._specializer.specialize(window_info)

        return window_info

    def retrieve_windows_state(self) -> WindowsState:
        return WindowsState(
            hostname=socket.gethostname(),
            username=os.getlogin(),
            active_window=self._prepare_window(gw.getActiveWindow()),
            windows=[self._prepare_window(w) for w in gw.getAllWindows()],
            timestamp=datetime.now(tz=timezone.utc)
        )
