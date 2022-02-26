# pylint: disable=unexpected-keyword-arg

from dataclasses import is_dataclass
from datetime import datetime
import unittest
from __seedwork.exceptions import SimpleValidationException

from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):

    description = 'some description'

    def test_if_is_dataclass(self):
        is_dataclass(Category)

    def test_constructor(self):
        category = Category(name='Movie')
        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)

        created_at = datetime.now()
        category = Category(name='Movie', description=self.description,
                            is_active=False, created_at=created_at)
        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, self.description)
        self.assertEqual(category.is_active, False)
        self.assertEqual(category.created_at, created_at)

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
        category.update('Documentary', self.description)
        self.assertEqual(category.name, 'Documentary')
        self.assertEqual(category.description, self.description)
