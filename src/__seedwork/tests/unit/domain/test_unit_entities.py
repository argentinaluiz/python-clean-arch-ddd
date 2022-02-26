
# pylint: disable=unexpected-keyword-arg,protected-access

from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
import uuid

from __seedwork.domain.entities import AggregateRoot, Entity, UniqueEntityId, ValueObject


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):

    def test_if_is_dataclass(self):
        is_dataclass(ValueObject)

    def test_init_prop(self):
        vo1 = StubOneProp('value')
        self.assertEqual('value', vo1.prop)

        vo2 = StubTwoProp('value1', 'value2')
        self.assertEqual('value1', vo2.prop1)
        self.assertEqual('value2', vo2.prop2)

    def test_convert_to_str(self):
        vo1 = StubOneProp('value')
        self.assertEqual('value', str(vo1))

        vo1 = StubTwoProp('value1', 'value2')
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo1))

    def test_if_props_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            vo1 = StubOneProp('value')
            vo1.prop = 'change'


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_dataclass(self):
        is_dataclass(UniqueEntityId)

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            with self.assertRaises(ValueError) as assert_error:
                UniqueEntityId("111111")
            self.assertEqual('badly formed hexadecimal UUID string', assert_error.exception.args[0])
            mock_validate.assert_called_once()

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId("5490020a-e866-4229-9adc-aa44b83234c4")
            self.assertEqual(value_object.id, "5490020a-e866-4229-9adc-aa44b83234c4")
            mock_validate.assert_called_once()

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(str(value_object.id))
            mock_validate.assert_called_once()

    def test_if_id_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'change'


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
        self.assertTrue(uuid.UUID(str(entity.id)))

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(id=UniqueEntityId("5490020a-e866-4229-9adc-aa44b83234c4"),
                            prop1='value1',
                            prop2='value2'
                            )
        self.assertEqual(
            "5490020a-e866-4229-9adc-aa44b83234c4",
            str(entity.id)
        )

    def test_to_dict_method(self):
        entity = StubEntity(id=UniqueEntityId(
            "5490020a-e866-4229-9adc-aa44b83234c4"), prop1='value1', prop2='value2'
        )
        self.assertDictEqual(
            {'id': "5490020a-e866-4229-9adc-aa44b83234c4",
                'prop1': 'value1', 'prop2': 'value2'},
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
