
# pylint: disable=unexpected-keyword-arg,protected-access

from dataclasses import dataclass, is_dataclass
import unittest
import uuid
from core.__seedwork.domain.entities import AggregateRoot, Entity
from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):

    def test_if_is_dataclass(self):
        is_dataclass(Entity)

    def test_set_id_and_props(self):
        entity = StubEntity(prop1='value1', prop2='value2')
        self.assertEqual('value1', entity.prop1)
        self.assertEqual('value2', entity.prop2)
        self.assertIsInstance(
            uuid.UUID(str(entity.unique_entity_id)), uuid.UUID)
        self.assertEqual(str(entity.unique_entity_id), entity.id)

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(unique_entity_id=UniqueEntityId("5490020a-e866-4229-9adc-aa44b83234c4"),
                            prop1='value1',
                            prop2='value2'
                            )
        self.assertEqual(
            "5490020a-e866-4229-9adc-aa44b83234c4",
            str(entity.unique_entity_id)
        )

    def test_to_dict_method(self):
        entity = StubEntity(unique_entity_id=UniqueEntityId(
            "5490020a-e866-4229-9adc-aa44b83234c4"), prop1='value1', prop2='value2'
        )
        self.assertDictEqual(
            {
                'id': "5490020a-e866-4229-9adc-aa44b83234c4",
                'prop1': 'value1',
                'prop2': 'value2'
            },
            entity.to_dict()
        )


@dataclass(frozen=True, kw_only=True)
class StubAggregateRoot(Entity):
    prop1: str
    prop2: str


class TestAggregateRootUnit(unittest.TestCase):

    def test_if_is_dataclass(self):
        is_dataclass(AggregateRoot)

    def test_if_be_a_child_class_of_entity(self):
        entity = StubAggregateRoot(prop1='value1', prop2='value2')
        self.assertTrue(isinstance(entity, Entity))
