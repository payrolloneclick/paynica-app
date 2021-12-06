import re
from typing import Optional

import phonenumbers


def validate_email(email: Optional[str]) -> str:
    if not email:
        return email
    if not re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        raise ValueError("Invalid email.")
    return email.lower()


def validate_phone(phone: Optional[str]) -> str:
    if not phone:
        return phone
    try:
        phone_number = phonenumbers.parse(phone)
    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number.")

    if not phonenumbers.is_valid_number(phone_number):
        raise ValueError("Invalid phone number.")

    return phone.lower()
