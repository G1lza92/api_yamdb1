import re

from django.core.exceptions import ValidationError

PATTERN = r"^[\w.@+-]+$"


class UsernameValidator(object):
    def __call__(self, value):
        if value == 'me':
            raise ValidationError(
                'Для имени пользователя нельзя использовать "me"'
            )
        if not re.findall(PATTERN, value):
            raise ValidationError(
                (f'Знаки '
                 f'{", ".join(i for i in value if not re.match(PATTERN, i))}'
                 f' запрещены для использоваения в имени')
            )
        return value
