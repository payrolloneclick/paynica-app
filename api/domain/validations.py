from typing import Optional

import phonenumbers


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
