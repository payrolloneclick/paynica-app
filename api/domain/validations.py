from typing import Optional

import phonenumbers

EMAIL_REGEXP = r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"


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
