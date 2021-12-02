from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class AbstractModel(BaseModel):
    pk: UUID4
    created_date: Optional[datetime]
    updated_date: Optional[datetime]
