
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from core.__seedwork.domain.repositories import SearchResult


Filter = TypeVar('Filter')


@dataclass(frozen=True, slots=True)
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None


Item = TypeVar('Item')


@dataclass(frozen=True, slots=True)
class PaginationOutput(Generic[Item]):
    items: List[Item]
    total: int
    current_page: int
    last_page: int
    per_page: int


class PaginationOutputMapper:
    @staticmethod
    def to_output(items: List[Item], result: SearchResult) -> PaginationOutput[Item]:
        return PaginationOutput(
            items=items,
            total=result.total,
            current_page=result.current_page,
            last_page=result.last_page,
            per_page=result.per_page,
        )
