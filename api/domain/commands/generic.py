from typing import Optional

from pydantic import BaseModel

from settings import DEFAULT_LIMIT


class AbstractCommand(BaseModel):
    pass


class AbstractListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = DEFAULT_LIMIT
    search: Optional[str] = None
    sort_by: Optional[str] = None
