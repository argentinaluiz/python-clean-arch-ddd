# pylint: disable=unexpected-keyword-arg

from dataclasses import dataclass
from typing import List, TypedDict
import unittest

from __seedwork.domain.repositories import InMemoryRepository, InMemorySearchableRepository, RepositoryInterface, SearchParams, SearchResult, SearchableRepositoryInterface, SortDirection
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException
from __seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            RepositoryInterface()
        self.assertEqual(
            "Can't instantiate abstract class RepositoryInterface with abstract " +
            "methods delete, find_all, find_by_id, insert, update",
            assert_error.exception.args[0]
        )


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):

    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_attr_is_empty_on_init(self):
        self.assertListEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name='test', price=0)
        self.repo.insert(entity)
        self.assertDictEqual(entity.to_dict(), self.repo.items[0].to_dict())

    def test_throw_exception_when_entity_not_found(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity Not Found using ID 'fake id'")

        unique_entity = UniqueEntityId('0adc23be-b196-4439-a42c-9b0c7c4d1058')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity)
        self.assertEqual(
            assert_error.exception.args[0], "Entity Not Found using ID '0adc23be-b196-4439-a42c-9b0c7c4d1058'")

    def test_find_by_id(self):
        entity = StubEntity(name='test', price=0)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertDictEqual(entity.to_dict(), entity_found.to_dict())

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertDictEqual(entity.to_dict(), entity_found.to_dict())

    def test_find_all(self):
        entity = StubEntity(name='test', price=0)
        self.repo.insert(entity)

        items = self.repo.find_all()
        self.assertListEqual([entity], items)

    def test_throw_exception_on_update_when_entity_not_found(self):
        entity = StubEntity(name='test', price=0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity Not Found using ID '{entity.id}'")

    def test_update(self):
        entity = StubEntity(name='test', price=0)
        self.repo.insert(entity)

        entity_updated = StubEntity(
            unique_entity_id=entity.unique_entity_id, name='updated', price=1)
        self.repo.update(entity_updated)
        self.assertDictEqual(entity_updated.to_dict(),
                             self.repo.items[0].to_dict())

    def test_throw_exception_on_delete_when_entity_not_found(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity Not Found using ID 'fake id'")

    def test_delete(self):
        entity = StubEntity(name='test', price=0)
        self.repo.insert(entity)

        self.repo.delete(entity.id)
        self.assertListEqual(self.repo.items, [])


class TestSearchParams(unittest.TestCase):

    def test_page_field(self):
        input_params = SearchParams()
        self.assertEqual(input_params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': "", 'expected': 1},
            {'page': "fake", 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
        ]

        for i in arrange:
            input_params = SearchParams(page=i['page'])
            self.assertEqual(input_params.page, i['expected'])

    def test_per_page_field(self):
        input_params = SearchParams()
        self.assertEqual(input_params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': "", 'expected': 15},
            {'per_page': "fake", 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': True, 'expected': 15},
            {'per_page': False, 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 10, 'expected': 10},
            {'per_page': 20, 'expected': 20},
        ]

        for i in arrange:
            input_params = SearchParams(per_page=i['per_page'])
            self.assertEqual(input_params.per_page, i['expected'])

    def test_sort_field(self):
        input_params = SearchParams()
        self.assertIsNone(input_params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': "", 'expected': None},
            {'sort': "fake", 'expected': "fake"},
            {'sort': 0, 'expected': '0'},
            {'sort': -1, 'expected': "-1"},
            {'sort': True, 'expected': "True"},
            {'sort': False, 'expected': "False"},
            {'sort': {}, 'expected': "{}"},
        ]

        for i in arrange:
            input_params = SearchParams(sort=i['sort'])
            self.assertEqual(input_params.sort, i['expected'])

    def test_sort_dir_field(self):
        input_params = SearchParams()
        self.assertIsNone(input_params.sort_dir)

        input_params = SearchParams(sort=None)
        self.assertIsNone(input_params.sort_dir)

        input_params = SearchParams(sort="")
        self.assertIsNone(input_params.sort_dir)

        arrange = [
            {'sort_dir': None, 'expected': SortDirection.ASC.value},
            {'sort_dir': "", 'expected': SortDirection.ASC.value},
            {'sort_dir': "fake", 'expected': SortDirection.ASC.value},
            {'sort_dir': "asc", 'expected': SortDirection.ASC.value},
            {'sort_dir': "ASC", 'expected': SortDirection.ASC.value},
            {'sort_dir': "desc", 'expected': SortDirection.DESC.value},
            {'sort_dir': "DESC", 'expected': SortDirection.DESC.value},
        ]

        for i in arrange:
            input_params = SearchParams(sort='name', sort_dir=i['sort_dir'])
            self.assertEqual(input_params.sort_dir, i['expected'])

    def test_filter_field(self):
        input_params = SearchParams()
        self.assertIsNone(input_params.filter)

        arrange = [
            {'filter': None, 'expected': None},
            {'filter': "", 'expected': None},
            {'filter': "fake", 'expected': "fake"},
            {'filter': 0, 'expected': "0"},
            {'filter': -1, 'expected': "-1"},
            {'filter': True, 'expected': "True"},
            {'filter': False, 'expected': "False"},
            {'filter': {}, 'expected': "{}"},
        ]

        for i in arrange:
            input_params = SearchParams(filter=i['filter'])
            self.assertEqual(input_params.filter, i['expected'])


class TestSearchResult(unittest.TestCase):

    def test_constructor(self):
        entity = StubEntity(name='name fake', price=5)
        output = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2
        )

        self.assertDictEqual(output.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': None,
            'sort_dir': None,
            'filter': None
        })

        output = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2,
            sort="name",
            sort_dir=SortDirection.ASC.value,
            filter="test"
        )

        self.assertDictEqual(output.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': "name",
            'sort_dir': SortDirection.ASC.value,
            'filter': "test"
        })

    def test_last_page_is_1_when_per_page_is_greater_than_total(self):
        output = SearchResult(
            items=[],
            total=4,
            current_page=1,
            per_page=15
        )
        self.assertEqual(output.last_page, 1)


class TestSearchableRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            SearchableRepositoryInterface()
        self.assertEqual(
            "Can't instantiate abstract class SearchableRepositoryInterface with abstract " +
            "methods delete, find_all, find_by_id, insert, search, update",
            assert_error.exception.args[0]
        )

    def test_sortable_fields_prop(self):
        self.assertEqual(SearchableRepositoryInterface.sortable_fields, [])


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity]):
    sortable_fields: List[str] = ['name']

    def _apply_filter(self, items: List[StubEntity], filter_param: str = None) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(
                lambda i: filter_param.lower() in i.name.lower() or str(i.price) == filter_param,
                items
            )
            return list(filter_obj)

        return items


class TestInMemorySearchableRepository(unittest.TestCase):

    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        items = [StubEntity(name='test', price=5)]
        # pylint: disable=protected-access
        result = self.repo._apply_filter(items)
        self.assertEqual(result, items)

        items = [
            StubEntity(name='test', price=5),
            StubEntity(name='TEST', price=5),
            StubEntity(name='fake', price=0),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, 'TEST')
        self.assertEqual(result, [items[0], items[1]])

        result = self.repo._apply_filter(items, '5')
        self.assertEqual(result, [items[0], items[1]])

    def test__apply_sort(self):
        items = [
            StubEntity(name='b', price=5),
            StubEntity(name='a', price=5),
        ]
        # pylint: disable=protected-access
        result = self.repo._apply_sort(items)
        self.assertEqual(result, items)

        result = self.repo._apply_sort(items, "price")
        self.assertEqual(result, items)

        items = [
            StubEntity(name='b', price=4),
            StubEntity(name='a', price=5),
            StubEntity(name='c', price=3),
        ]
        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, "name")
        self.assertEqual(result, [items[2], items[0], items[1]])

        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, "name", 'desc')
        self.assertEqual(result, [items[2], items[0], items[1]])

        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, "name", 'asc')
        self.assertEqual(result, [items[1], items[0], items[2]])

        self.repo.sortable_fields.append('price')
        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, "price")
        self.assertEqual(result, [items[1], items[0], items[2]])

        self.repo.sortable_fields.append('price')
        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, "price", "desc")
        self.assertEqual(result, [items[1], items[0], items[2]])

        self.repo.sortable_fields.append('price')
        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, "price", "asc")
        self.assertEqual(result, [items[2], items[0], items[1]])

    def test__apply_paginate(self):
        items = [
            StubEntity(name='a', price=1),
            StubEntity(name='b', price=1),
            StubEntity(name='c', price=1),
            StubEntity(name='d', price=1),
            StubEntity(name='e', price=1),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_paginate(items, 1, 2)
        self.assertEqual(result, [items[0], items[1]])

        result = self.repo._apply_paginate(items, 2, 2)
        self.assertEqual(result, [items[2], items[3]])

        result = self.repo._apply_paginate(items, 3, 2)
        self.assertEqual(result, [items[4]])

        result = self.repo._apply_paginate(items, 4, 2)
        self.assertEqual(result, [])

    def test_search_when_params_is_empty(self):
        entity = StubEntity(name='b', price=1)
        items = [entity] * 16
        self.repo.items = items

        result = self.repo.search(SearchParams())
        self.assertEqual(result, SearchResult(
            items=[entity] * 15,
            total=16,
            current_page=1,
            per_page=15,
            sort=None,
            sort_dir=None,
            filter=None
        ))

    def test_search_applying_paginate_and_filter(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='TeSt', price=1),
        ]

        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1, per_page=2, filter="TEST"))
        self.assertEqual(result, SearchResult(
            items=[items[0], items[2]],
            total=3,
            current_page=1,
            per_page=2,
            filter="TEST"
        ))

        result = self.repo.search(SearchParams(
            page=2, per_page=2, filter="TEST"))
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=3,
            current_page=2,
            per_page=2,
            filter="TEST"
        ))

    def test_search_applying_paginate_and_sort(self):
        items = [
            StubEntity(name='b', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='d', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='c', price=1),
        ]
        self.repo.items = items

        arrange = [
            {
                'input': SearchParams(per_page=2, sort='name'),
                'output': SearchResult(
                    items=[items[1], items[0]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort="name",
                    sort_dir="asc"
                )
            },
            {
                'input': SearchParams(page=2, per_page=2, sort='name'),
                'output': SearchResult(
                    items=[items[4], items[2]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort="name",
                    sort_dir="asc"
                )
            },
            {
                'input': SearchParams(per_page=2, sort='name', sort_dir='desc'),
                'output': SearchResult(
                    items=[items[3], items[2]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort="name",
                    sort_dir="desc"
                )
            },
            {
                'input': SearchParams(page=2, per_page=2, sort='name', sort_dir='desc'),
                'output': SearchResult(
                    items=[items[4], items[0]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort="name",
                    sort_dir="desc"
                )
            }
        ]

        for item in arrange:
            result = self.repo.search(item['input'])
            print(result, item['output'])
            self.assertEqual(result, item['output'])

    def test_search_applying_filter_sort_and_paginate(self):
        items = [
            StubEntity(name='test', price=1),
            StubEntity(name='a', price=1),
            StubEntity(name='TEST', price=1),
            StubEntity(name='e', price=1),
            StubEntity(name='TeSt', price=1),
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        self.assertEqual(result, SearchResult(
            items=[items[2], items[4]],
            total=3,
            current_page=1,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        result = self.repo.search(SearchParams(
            page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))

        self.assertEqual(result, SearchResult(
            items=[items[0]],
            total=3,
            current_page=2,
            per_page=2,
            sort="name",
            sort_dir="asc",
            filter="TEST"
        ))
