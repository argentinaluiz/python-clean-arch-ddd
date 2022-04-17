

from abc import ABC
import abc
from dataclasses import Field, asdict, dataclass, field, fields
import enum
import math
from typing import Any, Generic, List, NewType, Optional, Type, TypeVar
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException, NotImplementedException
from __seedwork.domain.value_objects import UniqueEntityId

ET = TypeVar('ET', bound=Entity)
#teste = NewType('teste',Entity)


class RepositoryInterface(Generic[ET], ABC):

    @abc.abstractmethod
    def insert(self, entity: ET) -> None:
        raise NotImplementedException

    @abc.abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        raise NotImplementedException

    @abc.abstractmethod
    def find_all(self) -> List[ET]:
        raise NotImplementedException

    @abc.abstractmethod
    def update(self, entity: ET) -> None:
        raise NotImplementedException

    @abc.abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedException


Filter = TypeVar('Filter', str, Any)


class SortDirection(enum.Enum):
    ASC = 'asc'
    DESC = 'desc'

    def equals(self, value):
        return value == self.value


@dataclass(slots=True, init=True, kw_only=True)
class SearchParams(Generic[Filter]):
    page: Optional[int] = 1
    per_page: Optional[int] = 15
    sort: Optional[str] = None
    sort_dir: Optional[SortDirection] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        self._normalize_page()
        self._normalize_per_page()
        self._normalize_sort()
        self._normalize_sort_dir()
        self._normalize_filter()

    def _normalize_page(self):
        page = _int_or_none(self.page)
        if page <= 0:
            page = self._get_field('page').default
        self.page = page

    def _normalize_per_page(self):
        per_page = _int_or_none(self.per_page)
        if per_page <= 1:
            per_page = self._get_field('per_page').default
        self.per_page = per_page

    def _normalize_sort(self):
        self.sort = None if self.sort == "" or self.sort is None else str(
            self.sort)

    def _normalize_sort_dir(self):
        if not self.sort:
            self.sort_dir = None
            return

        sort_dir = str(self.sort_dir).lower()
        self.sort_dir = SortDirection.ASC.value  \
            if not SortDirection.ASC.equals(sort_dir) and not SortDirection.DESC.equals(sort_dir) \
            else sort_dir

    def _normalize_filter(self):
        self.filter = None if self.filter is None or self.filter == "" else str(
            self.filter)

    def _get_field(self, property: str) -> Field:
        class_fields = fields(self)
        for f in class_fields:
            if f.name == property:
                return f


def _int_or_none(value: Any, default=0) -> int:
    try:
        return int(value)
    except ValueError:
        return default
    except TypeError:
        return default


@dataclass
class SearchResult(Generic[ET, Filter]):
    items: List[ET]
    total: int
    current_page: int
    per_page: int
    last_page: int = field(init=False)
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        self.last_page = math.ceil(self.total/self.per_page)

    def to_dict(self):
        return {
            'items': self.items,
            'total': self.total,
            'current_page': self.current_page,
            'per_page': self.per_page,
            'last_page': self.last_page,
            'sort': self.sort,
            'sort_dir': self.sort_dir,
            'filter': self.filter,
        }


Input = TypeVar('Input')
Output = TypeVar('Output')


class SearchableRepositoryInterface(Generic[ET, Input, Output], RepositoryInterface[ET], ABC):
    sortable_fields: List[str] = []

    @abc.abstractmethod
    def search(self, input_params: Input) -> Output:
        raise NotImplementedException


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[ET], ABC):
    items: List[ET] = field(default_factory=lambda: [])

    def insert(self, entity: ET) -> None:
        self.items.append(entity)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        id_str = f"{entity_id}"
        return self._get(id_str)

    def find_all(self) -> List[ET]:
        return self.items

    def update(self, entity: ET) -> None:
        entity_found = self._get(entity.id)
        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        id_str = f"{entity_id}"
        entity = self._get(id_str)
        self.items.remove(entity)

    def _get(self, entity_id: str) -> ET:
        entity = next(filter(lambda i: i.id == entity_id, self.items), None)
        if entity is None:
            raise NotFoundException(f"Entity Not Found using ID '{entity_id}'")
        return entity


class InMemorySearchableRepository(InMemoryRepository[ET], SearchableRepositoryInterface[ET, SearchParams, SearchResult], ABC):
    def search(self, input_params: SearchParams[str]) -> SearchResult[ET, Filter]:
        items_filtered = self._apply_filter(self.items, input_params.filter)
        items_sorted = self._apply_sort(
            items_filtered, input_params.sort, input_params.sort_dir)
        items_paginated = self._apply_paginate(
            items_sorted, input_params.page, input_params.per_page)

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            current_page=input_params.page,
            per_page=input_params.per_page,
            sort=input_params.sort,
            sort_dir=input_params.sort_dir,
            filter=input_params.filter,
        )

    @abc.abstractmethod
    def _apply_filter(self, items: List[ET], filter_param: str = None) -> List[ET]:
        raise NotImplementedException

    def _apply_sort(self, items: List[ET], sort: str = None, sort_dir: SortDirection = None) -> List[ET]:
        if sort and sort in self.sortable_fields:
            is_reverse = not SortDirection.ASC.equals(sort_dir)
            return sorted(items, key=lambda item: getattr(item, sort), reverse=is_reverse)
        return items

    def _apply_paginate(self, items: List[ET], page: int, per_page: int):
        offset = (page - 1) * per_page
        limit = offset + per_page
        return items[slice(offset, limit)]
