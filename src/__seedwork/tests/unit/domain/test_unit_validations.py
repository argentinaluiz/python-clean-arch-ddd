from datetime import datetime
from typing import Any
import unittest
from unittest.mock import MagicMock

from __seedwork.domain.validations import PydanticValidator, ValidatorInterface, ValidatorRules
from __seedwork.exceptions import SimpleValidationException, ValidationException


class TestValidationRulesUnit(unittest.TestCase):

    def test_algumacoisa(self):
        validator = ValidatorRules.values('test', 'field')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual('test', validator.value)
        self.assertEqual('field', validator.prop)

    def test_required_rule(self):
        data = [
            {'value': "test", 'prop': "field"},
            {'value': 5, 'prop': "field"},
            {'value': 0, 'prop': "field"},
            {'value': False, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).required(),
                ValidatorRules
            )

        data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
        ]

        message_error = 'The field is required'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).required()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_string_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': "", 'prop': "field"},
            {'value': "test", 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).string(),
                ValidatorRules
            )

        data = [
            {'value': 5, 'prop': "field"},
            {'value': datetime, 'prop': "field"},
        ]

        message_error = 'The field must be a string'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).string()
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_max_length_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': "t" * 5, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).max_length(5),
                ValidatorRules
            )

        data = [
            {'value': "t" * 11, 'prop': "field"},
        ]

        message_error = 'The field must be less than 10 characters'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).max_length(10)
            self.assertEqual(message_error, assert_error.exception.args[0])

    def test_boolean_rule(self):
        data = [
            {'value': None, 'prop': "field"},
            {'value': True, 'prop': "field"},
            {'value': False, 'prop': "field"},
        ]

        for i in data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).boolean(),
                ValidatorRules
            )

        data = [
            {'value': "", 'prop': "field"},
            {'value': 5, 'prop': "field"},
        ]

        message_error = 'The field must be a boolean'

        for i in data:
            with self.assertRaises(SimpleValidationException) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).boolean()
            self.assertEqual(message_error, assert_error.exception.args[0])


class TestValidatorInterfaceUnit(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorInterface()
        self.assertEqual(
            "Can't instantiate abstract class ValidatorInterface " +
            "with abstract methods errors, validate",
            assert_error.exception.args[0]
        )


class StubPydanticValidation(PydanticValidator):
    mock_pydantic_class: Any

    def __init__(self, mock_pydantic_class=None) -> None:
        self.mock_pydantic_class = mock_pydantic_class
        super().__init__()

    def validate(self, data):
        self._validate(data, self.mock_pydantic_class)


class TestPydanticValidatorUnit(unittest.TestCase):

    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            PydanticValidator()
        self.assertEqual(
            "Can't instantiate abstract class PydanticValidator with abstract method validate",
            assert_error.exception.args[0]
        )

    def test_error_field(self):
        validator = StubPydanticValidation()
        self.assertIsNone(validator.errors)
        setattr(validator, '_errors', {'field': ['som error']})
        self.assertDictEqual({'field': ['som error']}, validator.errors)

    def test_validate_with_validate_error(self):
        mock_pydantic_class = MagicMock(
            side_effect=ValidationException({'field': ['some error']}))

        validator = StubPydanticValidation(mock_pydantic_class)
        with self.assertRaises(ValidationException) as assert_error:
            validator.validate({'field': None})
        self.assertDictEqual(
            {'field': ['some error']}, assert_error.exception.error)
        mock_pydantic_class.assert_called_once()

    def test_validate_with_success(self):
        mock_pydantic_class = MagicMock()

        validator = StubPydanticValidation(mock_pydantic_class)
        validator.validate({'field': 'test'})
        mock_pydantic_class.assert_called_once()


# class StubDRFValidation(DRFValidator):
#     mock_serializer: serializers.Serializer

#     def __init__(self, serializer=None) -> None:
#         self.mock_serializer = serializer
#         super().__init__()

#     def validate(self, data):
#         self._validate(self.mock_serializer)


# class TestDRFValidatorUnit(unittest.TestCase):

#     def test_throw_error_when_validate_method_not_implemented(self):
#         with self.assertRaises(TypeError) as assert_error:
#             # pylint: disable=abstract-class-instantiated
#             DRFValidator()
#         self.assertEqual(
#             "Can't instantiate abstract class DRFValidator with abstract method validate",
#             assert_error.exception.args[0]
#         )

#     def test_error_field(self):
#         validator = StubDRFValidation()
#         self.assertIsNone(validator.errors)
#         setattr(validator, '_errors', {'field': ['som error']})
#         self.assertDictEqual({'field': ['som error']}, validator.errors)

#     def test_validate_with_validate_error(self):
#         mock_serializer = serializers.Serializer()
#         mock_serializer.is_valid = MagicMock(return_value=False)
#         mock_serializer.error_messages = {'field': ['some error']}

#         validator = StubDRFValidation(mock_serializer)
#         with self.assertRaises(ValidationError) as assert_error:
#             validator.validate({'field': None})
#         self.assertDictEqual(
#             {'field': ['some error']}, assert_error.exception.error)
#         mock_serializer.is_valid.assert_called_once()

#     def test_validate_with_success(self):
#         mock_serializer = serializers.Serializer()
#         mock_serializer.is_valid = MagicMock(return_value=True)

#         validator = StubDRFValidation(mock_serializer)
#         validator.validate({'field': 'test'})
#         mock_serializer.is_valid.assert_called_once()
