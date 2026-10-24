"""
Tests that the ontology adapter produces valid 7-layer JSON for every template.

These tests are fast — no browser, no file I/O, no Paged.js.
They validate the ontology_adapter output against schemas/v1.0/document.schema.json.

Run:
    pytest tests/test_ontology_schema.py -v
    pytest tests/test_ontology_schema.py -v --template=bank_statement
"""
from pathlib import Path

import synthdoc.schemas

SCHEMA_DIR = Path(synthdoc.schemas.__file__).parent / "v1.0"


class TestOntologySchemaValidation:
    """Validate that every template produces ontology JSON conforming to the schema."""

    def test_ontology_output_validates(self, template_name, template_instance):
        """Ontology JSON from adapter must pass document.schema.json validation."""
        from synthdoc.ontology_adapter import build_ontology_document
        from synthdoc.schemas.tools.validate import DocumentValidator

        # Build a representative label_data dict (same shape as NER generator output)
        mock_label = {
            "document_id": f"TEST_{template_name}",
            "page_number": 1,
            "total_pages": 1,
            "width": 816,
            "height": 1056,
            "template_type": template_name,
            "sections": [],
            "fields": [],
            "annotations": [
                {
                    "label": "sample_field_0",
                    "text_content": "John Doe",
                    "entity_type": "PERSON",
                    "generic_type": "PERSON_NAME",
                    "box_2d": [100, 200, 300, 230],
                },
                {
                    "label": "sample_label_0",
                    "text_content": "Name:",
                    "entity_type": "FIELD_LABEL",
                    "generic_type": "FIELD_LABEL",
                    "box_2d": [50, 200, 95, 230],
                },
            ],
        }

        ontology_doc = build_ontology_document(mock_label, template_instance)

        validator = DocumentValidator(SCHEMA_DIR)
        is_valid, errors = validator.validate_document(ontology_doc)
        assert is_valid, f"{template_name}: schema validation failed: {errors}"

    def test_ontology_metadata_uses_template_methods(self, template_name, template_instance):
        """Metadata should reflect the template's archetype/category/document_type."""
        from synthdoc.ontology_adapter import build_ontology_document

        mock_label = {
            "document_id": f"TEST_{template_name}",
            "page_number": 1,
            "total_pages": 1,
            "width": 816,
            "height": 1056,
            "sections": [],
            "fields": [],
            "annotations": [],
        }

        doc = build_ontology_document(mock_label, template_instance)

        meta = doc["metadata"]
        assert meta["document_id"] == f"TEST_{template_name}"
        assert meta["archetype"] in (
            "form", "ledger", "letter", "invoice", "report",
            "certificate", "card", "legal", "ticket", "label",
        ), f"{template_name}: invalid archetype '{meta['archetype']}'"
        assert meta["category"] in (
            "financial", "legal", "medical", "government", "business",
            "education", "insurance", "real_estate", "transportation",
            "logistics", "manufacturing", "retail", "technology",
        ), f"{template_name}: invalid category '{meta['category']}'"

    def test_ontology_content_blocks_match_annotations(self, template_name, template_instance):
        """Content blocks should map 1:1 from annotations."""
        from synthdoc.ontology_adapter import build_ontology_document

        annotations = [
            {"label": f"ann_{i}", "text_content": f"text_{i}",
             "entity_type": "TEXT", "generic_type": "TEXT",
             "box_2d": [i * 100, 100, i * 100 + 90, 130]}
            for i in range(5)
        ]

        mock_label = {
            "document_id": "TEST_blocks",
            "page_number": 1,
            "total_pages": 1,
            "width": 816,
            "height": 1056,
            "sections": [],
            "fields": [],
            "annotations": annotations,
        }

        doc = build_ontology_document(mock_label, template_instance)
        blocks = doc["content"]["blocks"]

        # Should have at least as many blocks as annotations
        assert len(blocks) >= len(annotations), (
            f"Expected at least {len(annotations)} blocks, got {len(blocks)}"
        )

        # Each annotation block should have a bbox
        for block in blocks[:len(annotations)]:
            assert "bbox" in block, f"Block {block['block_id']} missing bbox"
            assert block["bbox"]["coordinate_system"] == "normalized"

    def test_ontology_without_template_instance(self, template_name):
        """Adapter should work with template_instance=None (safe defaults)."""
        from synthdoc.ontology_adapter import build_ontology_document

        mock_label = {
            "document_id": "TEST_no_instance",
            "page_number": 1,
            "total_pages": 1,
            "width": 816,
            "height": 1056,
            "sections": [],
            "fields": [],
            "annotations": [],
        }

        doc = build_ontology_document(mock_label, template_instance=None)
        assert doc["metadata"]["archetype"] == "form"
        assert doc["metadata"]["category"] == "business"
        assert doc["content"]["blocks"] == []
