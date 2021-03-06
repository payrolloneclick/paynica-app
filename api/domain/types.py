from enum import Enum

from pydantic.types import UUID4, constr

EMAIL_REGEXP = r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"


class TCurrency(str, Enum):
    USD = "USD"
    GBR = "GBP"
    EUR = "EUR"
    RUB = "RUB"


class TCountry(str, Enum):
    USA = "USA"
    GBR = "GBR"
    RUS = "RUS"


class TRole(str, Enum):
    EMPLOYER = "EMPLOYER"
    CONTRACTOR = "CONTRACTOR"


class TBankAccountType(str, Enum):
    BUSINESS = "BUSINESS"
    PERSONAL = "PERSONAL"


class TOperationStatus(str, Enum):
    CREATING = "CREATING"
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


TPrimaryKey = UUID4
TEmail = constr(strip_whitespace=True, to_lower=True, regex=EMAIL_REGEXP)
TPhone = constr(strip_whitespace=True, to_lower=True, min_length=1)
TPassword = constr(strip_whitespace=True, min_length=8)
TEmailCode = constr(strip_whitespace=True, min_length=16)
TPhoneCode = constr(strip_whitespace=True, min_length=6)
TPasswordCode = constr(strip_whitespace=True, min_length=16)
TInvitationCode = constr(strip_whitespace=True, min_length=16)
