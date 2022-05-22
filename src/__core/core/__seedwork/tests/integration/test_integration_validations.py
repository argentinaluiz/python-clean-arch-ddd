import unittest
#from pydantic.dataclasses import dataclass
# pylint: disable=no-name-in-module
#from pydantic.fields import Field
from rest_framework import serializers
from core.__seedwork.domain.exceptions import ValidationException
from core.__seedwork.domain.validators import DRFValidator


# @dataclass
# class StubPydantic:
#     prop1: str = Field(...)
#     prop2: int = Field(...)


# class StubPydanticValidation(PydanticValidator):

#     def validate(self, data):
#         self._validate(data, StubPydantic)

# pylint: disable=abstract-method
class StubSerializer(serializers.Serializer):
    name = serializers.CharField()
    money = serializers.IntegerField()


class StubDRFValidator(DRFValidator):

    def validate(self, data):
        self._validate(StubSerializer(data=data))


class TestDRFValidatorInt(unittest.TestCase):

    def test_validation_error(self):
        with self.assertRaises(ValidationException) as assert_error:
            StubDRFValidator().validate({})
        self.assertDictEqual(
            {
                'name': ['This field is required.'],
                'money': ['This field is required.']
            },
            assert_error.exception.error
        )

    def test_valid(self):
        validator = StubDRFValidator()
        # ser true depois
        validator.validate({'name': 'name test', 'money': 5})
        self.assertIsNone(validator.errors)
