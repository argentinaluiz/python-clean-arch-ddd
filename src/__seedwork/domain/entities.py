
from abc import ABC
from dataclasses import dataclass, fields, asdict, field
import json
from typing import Any
import uuid


@dataclass(frozen=True, slots=True)
class ValueObject(ABC):

    def __str__(self):
        fields_name = [field.name for field in fields(self)]
        return str(getattr(self, fields_name[0])) \
            if len(fields_name) == 1 \
            else json.dumps({field_name: getattr(self, field_name) for field_name in fields_name})


@dataclass(frozen=True, slots=True)
class UniqueEntityId(ValueObject):
    # pylint: disable=invalid-name,unnecessary-lambda
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())

    def __post_init__(self):
        self.__validate()

    def __validate(self):
        uuid.UUID(str(self.id))


@dataclass(frozen=True, kw_only=True, slots=True)
class Entity(ABC):
    # pylint: disable=invalid-name,unnecessary-lambda
    id: UniqueEntityId = field(default_factory=lambda: UniqueEntityId())

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
        return self

    def to_dict(self):
        dict_entity = asdict(self)
        print(dict_entity)
        dict_entity['id'] = str(dict_entity['id']['id'])
        return dict_entity


@dataclass(frozen=True, kw_only=True, slots=True)
class AggregateRoot(Entity):
    pass
