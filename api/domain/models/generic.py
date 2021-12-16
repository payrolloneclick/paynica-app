from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..types import TPrimaryKey


class AbstractModel(BaseModel):
    pk: TPrimaryKey

    created_date: Optional[datetime]
    updated_date: Optional[datetime]
