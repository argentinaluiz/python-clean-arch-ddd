# pylint: disable=unexpected-keyword-arg

from dataclasses import is_dataclass
from datetime import datetime
import unittest
from unittest import mock
from __seedwork.domain.exceptions import SimpleValidationException

from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):

    description = 'some description'

    def test_if_is_dataclass(self):
        is_dataclass(Category)

    def test_constructor(self):
        with mock.patch.object(Category, 'validate') as mock_validate_method:
            category = Category(name='Movie')
            mock_validate_method.assert_called_once()
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

    def test_activate(self):
        category = Category(name='Movie', is_active=False)
        category.activate()
        self.assertTrue(category.is_active)

    def test_deactivate(self):
        category = Category(name='Movie')
        category.deactivate()
        self.assertFalse(category.is_active)

    def test_update(self):
        with mock.patch.object(Category, 'validate') as mock_validate_method:
            category = Category(name='Movie')
            category.update('Documentary', self.description)
            self.assertEqual(mock_validate_method.call_count, 2)
            self.assertEqual(category.name, 'Documentary')
            self.assertEqual(category.description, self.description)
