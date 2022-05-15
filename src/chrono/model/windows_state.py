from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from chrono.model.window_info import WindowInfo


class WindowsState(BaseModel):
    id: Optional[str] = None
    timestamp: Optional[datetime] = None
    hostname: str
    username: Optional[str]
    active_window: Optional[WindowInfo]
    windows: List[WindowInfo]
    time_delta: Optional[float]
