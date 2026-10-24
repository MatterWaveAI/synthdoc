# Dataset format and history

> The original README of the generator, before it became the `synthdoc` library. Commands below
> use the old `generate_dataset.py` script; the installed equivalent is `synthdoc`. Some field
> examples predate the current label schema; the main README shows real output.

Generate large-scale synthetic document datasets for training NER and document understanding models. Creates realistic documents (invoices, forms, contracts, etc.) with pixel-perfect bounding box annotations and document graph annotations.

## Quick Start

```bash
cd synthetic-document-dataset

# Generate dataset (10 documents per template = ~810 images)
python generate_dataset.py --count 10

# Verify annotations with visual overlays
python generate_overlays.py --seed 10
```

Output:
- `data/images/*.jpg` - Document images
- `data/labels/*.json` - Traditional JSON annotations
- `data/labels/*.ttl` - RDF graphs with schema.org/DBpedia integration
- `data/labels/*.jsonld` - JSON-LD for web publishing
Usage:

```bash
# Sequential (default, backward compatible)

python generate_dataset.py --templates bank_statement invoice --count 5

# Parallel with 4 workers
python generate_dataset.py --templates bank_statement invoice medical_report tax_return --count 5 --workers 4
```

## How It Works

The generator uses an **HTML → PDF → Image** pipeline:

1. **Templates** create realistic documents using Jinja2 + Faker for random data
2. **HTML rendering** extracts bounding box coordinates via Playwright
3. **PDF conversion** ensures production-like document rendering
4. **Image extraction** creates one JPG per PDF page with scaled coordinates

Each template in `synthdoc/templates/` defines document structure and generates sample data. See [PIPELINE_README.md](PIPELINE_README.md) for technical details.

## Options

**Select specific templates:**
```bash
python generate_dataset.py --templates invoice bank_statement --count 50
```

**Visual verification:**
```bash
python generate_overlays.py --seed 10
```
Creates overlay images with bounding boxes in `data/overlays/`. The `--seed` should match your generation `--count` for smart sampling (100% for ≤10, 20% for ≤100, 5% for >100).

## Data Format

Each document has:
- `{template}_{number}.jpg` - Document image
- `{template}_{number}.json` - Annotations with hierarchical entity types

### Annotation Structure

```json
{
  "document_id": "w9_form_000001",
  "template_type": "w9_form",
  "width": 2000,
  "height": 2800,
  "annotations": [
    {
      "label": "field_name",
      "text_content": "text",
      "box_2d": [x1, y1, x2, y2],
      "entity_type": "PLAINTIFF_NAME",
      "generic_type": "PERSON"
    }
  ]
}
```

### Entity Type Hierarchy

Annotations include **two-level entity types** for flexible model training:

- **`entity_type`** (Specific): Precise semantic label (e.g., `PLAINTIFF_NAME`, `CASE_NUMBER`, `SIGNATURE_DATE`)
- **`generic_type`** (Generic Parent): Broader category for layout analysis (e.g., `PERSON`, `IDENTIFIER`, `DATE`)

This hierarchy allows you to:
- Train layout models on generic types (13 categories)
- Train extraction models on specific types (150+ entity types)
- Switch between granularities without re-annotation

**Generic Parent Categories:**
1. **Document Regions**: `HEADER`, `FOOTER`, `MARGIN`, `SEPARATOR`, `SECTION`, `STAMP`
2. **Text Blocks**: `TITLE`, `TEXT`, `LIST`
3. **Form Elements**: `FIELD_LABEL`, `INPUT_REGION`, `CHECKBOX`, `RADIO`, `SIGNATURE`
4. **Structured Data**: `TABLE`, `TABLE_ROW`, `TABLE_CELL`, `COLUMN_HEADER`
5. **Semantic Fields**: `IDENTIFIER`, `DATE`, `PERSON`, `ORG`, `ADDRESS`, `MONEY`, `CONTACT`
6. **Visual Elements**: `IMAGE`, `CODE_GRAPHIC`


## Optional: HuggingFace Upload

If you want to upload your dataset to HuggingFace for sharing or model training:

1. Edit `upload_to_hf.py` and set your dataset name:
   ```python
   HF_DATASET_NAME = "your-username/synthetic-documents"
   ```

2. Login to HuggingFace:
   ```bash
   pip install datasets huggingface_hub
   huggingface-cli login
   ```

3. Upload:
   ```bash
   python upload_to_hf.py
   ```

## Linked Data Integration

The pipeline generates **RDF/OWL graphs** with schema.org and DBpedia integration for semantic interoperability.

### Features

- **Schema.org types**: Person, Organization, PostalAddress, MonetaryAmount
- **DBpedia types**: Person, Organisation, Address
- **RDF formats**: Turtle (.ttl) and JSON-LD (.jsonld)
- **SPARQL queries**: Query across documents and external knowledge bases
- **Document ontology**: Sections → Fields → Labels/Values with no data duplication

### Example Usage

```python
from rdflib import Graph, Namespace

SCHEMA = Namespace("http://schema.org/")
DOC = Namespace("http://example.org/document-ontology#")

# Load RDF graph
g = Graph()
g.parse("data/labels/DOC_000000_page_1.ttl", format="turtle")

# Query all people entities
people = g.query("""
    PREFIX schema: <http://schema.org/>
    PREFIX doc: <http://example.org/document-ontology#>

    SELECT ?name
    WHERE {
        ?person a schema:Person ;
                doc:textContent ?name .
    }
""")

for row in people:
    print(f"Person: {row.name}")
```

### Export to Schema.org HTML

```bash
python export_schema_org_html.py
```

Generates HTML with embedded schema.org microdata for SEO and web publishing.
