from ..types import TPrimaryKey
from .generic import AbstractReponse


class CompanyResponse(AbstractReponse):
    pk: TPrimaryKey
    name: str
