from datetime import datetime

from pydantic import BaseModel


class ActivityStats(BaseModel):
    total_time: float
    total_time_human: str
    from_timestamp: datetime
    to_timestamp: datetime
