from typing import Optional

from pydantic import BaseModel

from domain.types import TSortByDirection
from settings import DEFAULT_LIMIT


class AbstractCommand(BaseModel):
    pass


class AbstractListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = DEFAULT_LIMIT
    search: Optional[str] = None
    sort_by_field: Optional[str] = None
    sort_by_direction: Optional[TSortByDirection] = TSortByDirection.DESC
