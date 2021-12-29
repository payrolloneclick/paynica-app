from ..types import TPrimaryKey
from .generic import AbstractReponse


class CompanyResponse(AbstractReponse):
    id: TPrimaryKey
    name: str
