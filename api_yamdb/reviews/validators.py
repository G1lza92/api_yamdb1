import re

from django.core.exceptions import ValidationError

PATTERN = r"[^\w^.^@^+^-]+"


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Для имени пользователя нельзя использовать "me"'
        )
    forbidden = set(''.join(re.findall(PATTERN, value)))
    if forbidden:
        raise ValidationError(
            (f'Символы {tuple(forbidden)} нельзя использовать в имени')
        )
    return value
