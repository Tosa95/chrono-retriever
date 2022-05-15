from datetime import datetime
from typing import Any


def to_jsonable_dict(x: Any):

    if isinstance(x, dict):
        return {k: to_jsonable_dict(v) for k, v in x.items()}

    if isinstance(x, list):
        return [to_jsonable_dict(v) for v in x]

    if isinstance(x, datetime):
        return x.isoformat()

    return x