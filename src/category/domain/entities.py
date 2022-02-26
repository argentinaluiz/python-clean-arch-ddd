
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from __seedwork.domain.entities import AggregateRoot
from __seedwork.domain.validations import ValidatorRules


@dataclass(frozen=True, kw_only=True, slots=True)
class Category(AggregateRoot):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    # pylint: disable=invalid-name,unnecessary-lambda
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

    def update(self, name: str, description: str = None):
        self._set('name', name)
        self._set('description', description)

    def activate(self):
        self._set('is_active',True)

    def deactivate(self):
        self._set('is_active',False)

    def simple_validate(self):

        ValidatorRules.values(
            self.name, 'name'
        ).required().string().max_length(255)

        ValidatorRules.values(
            self.description, 'description'
        ).string()

        ValidatorRules.values(
            self.is_active, 'is_active'
        ).boolean()
