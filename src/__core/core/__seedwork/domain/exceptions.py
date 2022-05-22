from dataclasses import dataclass
from typing import TYPE_CHECKING


class NotImplementedException(Exception):
    pass


class SimpleValidationException(Exception):
    pass


if TYPE_CHECKING:
    from core.__seedwork.domain.validators import ErrorFields


class ValidationException(Exception):
    error: 'ErrorFields'

    def __init__(self, error: 'ErrorFields'):
        self.error = error
        super().__init__('Validation Error')


class NotFoundException(Exception):
    pass
