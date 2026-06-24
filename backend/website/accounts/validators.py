import re

from django.core.exceptions import ValidationError


def validate_iran_phone(value):
    pattern = r'^(09\d{9}|9\d{9})$'

    if not re.fullmatch(pattern, value):
        raise ValidationError(
            "Phone number must start with 9 or 09."
        )