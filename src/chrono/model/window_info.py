from typing import Union
from typing_extensions import Annotated, Literal

from pydantic import BaseModel, Field


class BaseWindowInfo(BaseModel):
    name: str
    process_name: str
    process_id: int
    type_: Literal["BaseWindowInfo"] = "BaseWindowInfo"


class BrowserWindowInfo(BaseWindowInfo):
    url: str
    type_: Literal["BrowserWindowInfo"] = "BrowserWindowInfo"


class IdeWindowInfo(BaseWindowInfo):
    project: str
    file: str
    type_: Literal["IdeWindowInfo"] = "IdeWindowInfo"


WindowInfo = Annotated[Union[BaseWindowInfo, BrowserWindowInfo, IdeWindowInfo], Field(discriminator='type_')]
