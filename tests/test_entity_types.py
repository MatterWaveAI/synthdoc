"""
Entity types the renderer emits must each have a generic type in
entity_type_hierarchy.json, and named entities must keep their own generic type.

Fast: no browser.
"""
import pytest

from synthdoc.ner_data_generator import NERDataGenerator
from synthdoc.ontology_mapper import OntologyMapper


def _emitted_entity_types():
    mapper = OntologyMapper()
    return sorted(
        set(mapper._default_type_map.values())
        | set(mapper._default_property_map.values())
        | set(mapper._structural_properties.values())
        | {"TEXT"}
    )


def _hierarchy():
    NERDataGenerator._load_entity_hierarchy()
    return NERDataGenerator._entity_hierarchy


@pytest.mark.parametrize("entity_type", _emitted_entity_types())
def test_every_emitted_entity_type_has_a_generic_type(entity_type):
    assert entity_type in _hierarchy(), (
        f"{entity_type} is emitted by the renderer but missing from entity_type_hierarchy.json"
    )


@pytest.mark.parametrize("entity_type", ["PERSON", "ORG", "DATE", "ADDRESS", "EMAIL", "PHONE"])
def test_named_entities_are_their_own_generic_type(entity_type):
    assert NERDataGenerator.get_generic_type(entity_type) == entity_type


def test_unknown_entity_type_falls_back_to_text():
    assert NERDataGenerator.get_generic_type("NOT_A_REAL_TYPE") == "TEXT"


def test_name_is_resolved_from_its_subject_not_mapped_directly():
    # schema:name names whatever its subject is, so mapping it straight to PERSON
    # labels product lines and court names as people.
    mapper = OntologyMapper()
    assert "name" not in mapper._default_property_map
    assert "name" in mapper._subject_named_properties
