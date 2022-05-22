from abc import ABC
from dataclasses import dataclass, field, fields
import json
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

    def __str__(self):
        return f"{self.id}"
