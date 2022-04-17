
from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, List
from attr import field  # terá uma Self na versão 3.11
from rest_framework.fields import BooleanField, CharField, Field
from rest_framework.serializers import Serializer
from django.conf import settings
from __seedwork.domain.exceptions import (
    SimpleValidationException,
    NotImplementedException,
    ValidationException
)
from __seedwork.domain.entities import UniqueEntityId

if not settings.configured:
    settings.configure(
        USE_I18N=False
    )


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value, prop):
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == '':
            raise SimpleValidationException(f'The {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise SimpleValidationException(
                f'The {self.prop} must be a string')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_length:
            raise SimpleValidationException(
                f'The {self.prop} must be less than {max_length} characters'
            )
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and self.value is not True and self.value is not False:
            raise SimpleValidationException(
                f'The {self.prop} must be a boolean'
            )
        return self


ErrorFields = Dict[str, List[str]]

@dataclass(slots=True,)
class ValidatorFieldsInterface(ABC):
    errors: ErrorFields = None

    @abc.abstractmethod
    def validate(self, data: Any) -> None:
        raise NotImplementedException


class DRFValidator(ValidatorFieldsInterface, ABC):

    def _validate(self, serializer: Serializer) -> None:
        is_valid = serializer.is_valid()
        if not is_valid:
            # errors = {}
            # for key, _errors in serializer.errors.items():
            #     errors[key] = []
            #     for error in _errors:
            #         errors[key].append(str(error))
            self.errors = {
                key: [str(error) for error in _errors]
                for key, _errors in serializer.errors.items()
            }
            raise ValidationException(self.errors)

    @abc.abstractmethod
    def validate(self, data: Any):
        raise NotImplementedException


class UniqueEntityIdField(Field):
    default_error_messages = {
        'invalid': 'Must be a instance of UniqueEntityId.'
    }

    def to_internal_value(self, data):
        # We're lenient with allowing basic numerics to be coerced into strings,
        # but other types should fail. Eg. unclear if booleans should represent as `true` or `True`,
        # and composites such as lists are likely user error.
        if not isinstance(data, UniqueEntityId):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        return value


class StrictCharField(CharField):
    def to_internal_value(self, data):
        # We're lenient with allowing basic numerics to be coerced into strings,
        # but other types should fail. Eg. unclear if booleans should represent as `true` or `True`,
        # and composites such as lists are likely user error.
        if not isinstance(data, str):
            self.fail('invalid')
        return super().to_internal_value(data)


class StrictBooleanField(BooleanField):
    def to_internal_value(self, data):
        try:
            if data is True:
                return True
            elif data is False:
                return False
            elif data is None and self.allow_null:
                return None
        except TypeError:
            pass
        self.fail('invalid', input=data)

    def to_representation(self, value):
        if value in self.TRUE_VALUES:
            return True
        elif value in self.FALSE_VALUES:
            return False
        if value in self.NULL_VALUES and self.allow_null:
            return None
        return bool(value)


# class PydanticValidator(ValidatorInterface, ABC):
#     _errors: ValidationErrorFields = None

#     def _validate(self, data: dict | None, pydantic_class) -> None:
#         try:
#             data = data if isinstance(data, dict) else {}
#             print(data)
#             pydantic_class(**data)
#         except PydanticValidationError as error:
#             self._errors = {e['loc'][0]: e['msg'] for e in error.errors()}
#             raise ValidationException(self._errors) from error

#     @abc.abstractmethod
#     def validate(self, data: Any):
#         raise NotImplementedException

#     @property
#     def errors(self) -> ValidationErrorFields:
#         return self._errors
