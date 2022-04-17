

from abc import ABC
from __seedwork.domain.repositories import (
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
    SearchableRepositoryInterface
)
from category.domain.entities import Category

# pylint: disable=too-few-public-methods
class _SearchParams(DefaultSearchParams[str]):
    pass


class _SearchResult(DefaultSearchResult[Category, str]):
    pass


class CategoryRepository(SearchableRepositoryInterface[Category, _SearchParams, _SearchResult], ABC):
    SearchParams = _SearchParams
    SearchResult = _SearchResult
