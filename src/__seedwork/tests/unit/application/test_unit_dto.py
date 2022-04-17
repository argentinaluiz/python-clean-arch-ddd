# pylint: disable=unexpected-keyword-arg
from typing import List
import unittest
from __seedwork.application.dto import Item, PaginationOutput, PaginationOutputMapper
from __seedwork.domain.repositories import SearchResult, SortDirection


class TestPaginationOutput(unittest.TestCase):

    def test_fields(self):
        self.assertEqual(PaginationOutput.__annotations__, {
            'items': List[Item],
            'total': int,
            'current_page': int,
            'last_page': int,
            'per_page': int,
        })


class TestPaginationOutputMapper(unittest.TestCase):

    def test_to_output(self):
        result = SearchResult(
            items=['fake'],
            total=1,
            current_page=1,
            per_page=1,
            sort='name',
            sort_dir=SortDirection.ASC.value,
            filter='filter fake'
        )
        
        output = PaginationOutputMapper.to_output(result.items, result=result)
        self.assertEqual(output, PaginationOutput(
            items=result.items,
            total=result.total,
            current_page=result.current_page,
            last_page=result.last_page,
            per_page=result.per_page,
        ))
