from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correct year!'),
            params={'value': value},
        )
