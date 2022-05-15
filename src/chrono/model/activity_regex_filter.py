from typing import Optional

from pydantic import BaseModel


class ActivityRegexFilter(BaseModel):
    hostname_re: Optional[str]
    username_re: Optional[str]
    process_name_re: Optional[str]
    name_re: Optional[str]
    project_re: Optional[str]
    file_re: Optional[str]
    branch_re: Optional[str]
    url_re: Optional[str]
