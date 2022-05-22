
from abc import ABC
from dataclasses import Field, dataclass, asdict, field
from typing import Any

from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True, slots=True)
class Entity(ABC):
    # pylint: disable=invalid-name,unnecessary-lambda
    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId())

    @property
    def id(self) -> str:
        return str(self.unique_entity_id.id)

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
        return self

    def to_dict(self):
        dict_entity = asdict(self)
        dict_entity.pop('unique_entity_id')
        dict_entity['id'] = str(self.id)
        return dict_entity

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        # pylint: disable=no-member
        return cls.__dataclass_fields__[entity_field]


@dataclass(frozen=True, kw_only=True, slots=True)
class AggregateRoot(Entity, ABC):
    pass
