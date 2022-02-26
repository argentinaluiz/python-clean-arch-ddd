# pylint: disable=unexpected-keyword-arg

import unittest
from __seedwork.exceptions import SimpleValidationException, ValidationException

from category.domain.validators import CategoryRules, CategoryValidator
from category.domain.entities import Category

class TestCategoryValidatorUnit(unittest.TestCase):

    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidator()
        return super().setUp()

    def test_invalidation_cases_for_name_field(self):
        with self.assertRaises(ValidationException) as assert_error:
            self.validator.validate({'name': ''})
        print(assert_error.exception.error)

    def test_invalidation_of_entity(self):
        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name='').simple_validate()
        self.assertEqual('The name is required',
                         assert_error.exception.args[0])

        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name=5).simple_validate()
        self.assertEqual('The name must be a string',
                         assert_error.exception.args[0])

        with self.assertRaises(
            SimpleValidationException,
        ) as assert_error:
            Category(name='t' * 256).simple_validate()
        self.assertEqual('The name must be less than 255 characters',
                         assert_error.exception.args[0])

        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name='t', description=5).simple_validate()
        self.assertEqual('The description must be a string',
                         assert_error.exception.args[0])

        with self.assertRaises(SimpleValidationException) as assert_error:
            Category(name='t', is_active=5).simple_validate()
        self.assertEqual('The is_active must be a boolean',
                         assert_error.exception.args[0])

    def test_activate(self):
        category = Category(name='Movie', is_active=False)
        category.activate()
        self.assertTrue(category.is_active)

    def test_deactivate(self):
        category = Category(name='Movie')
        category.deactivate()
        self.assertFalse(category.is_active)

    def test_update(self):
        category = Category(name='Movie')
        category.update('Documentary', 'some description')
        self.assertEqual(category.name, 'Documentary')
        self.assertEqual(category.description, 'some description')
