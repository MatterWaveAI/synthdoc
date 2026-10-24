# synthdoc

Synthetic documents with pixel-accurate entity annotations, for training and benchmarking NER,
OCR and document-layout models.

Each document is filled with Faker data,
laid out in a headless browser with [Paged.js](https://pagedjs.org), and exported as page images
with a bounding box for every entity, taken from the rendered layout rather than estimated.

```python
import synthdoc

synthdoc.list_templates()                 # ['bank_statement', 'invoice', 'test_showcase']
synthdoc.generate(templates=["invoice"], count=10, out_dir="data")
```

synthdoc bundles three example templates. The full collection, 257 more across 23 categories
(tax forms, medical claims, leases, court filings, IDs, permits and more), is
[synthdoc-templates](https://github.com/matterwaveai/synthdoc-templates); see [Templates](#templates).

## Install

```bash
pip install synthdoc
playwright install chromium     # one-time: the browser synthdoc renders with
```

Optional extras:

| Extra | Adds |
|---|---|
| `synthdoc[validate]` | Validate output against the JSON schemas in `synthdoc/schemas/v1.0` |
| `synthdoc[viz]` | Overlay and chart helpers (matplotlib) |
| `synthdoc[pdf]` | WeasyPrint and pdf2image as alternative PDF backends |
| `synthdoc[bench]` | The OCR / NER / layout benchmark harness (torch, transformers, spaCy, Tesseract) |

## Command line

```bash
synthdoc --list                                   # category<TAB>template, one per line
synthdoc --templates invoice bank_statement --count 50 --out data
synthdoc --count 5 --workers 4 --out data         # every template, 4 in parallel
synthdoc --formats json --no-pdfs --out data      # JSON labels only, no PDFs kept
```

`synthdoc --help` lists the rest: `--template-dir`, `--entity-types`, `--min-bbox-size`,
`--validate`, `--config`.

## Templates

Add the synthdoc-templates collection, or any folder of your own templates, in one of three ways:

```bash
git clone https://github.com/matterwaveai/synthdoc-templates

synthdoc --template-dir synthdoc-templates --templates w9_form lease_agreement --count 10 --out data
export SYNTHDOC_TEMPLATE_PATH=$PWD/synthdoc-templates   # every run; os.pathsep-separated
```

```python
synthdoc.add_template_dir("synthdoc-templates")
```

In a source checkout, cloning into `src/synthdoc/templates/library/` loads the collection with no
flag at all. Folders later on the search path override earlier ones by template name.

## Output

Every page gets a sequential Bates number (`SDD000000`, `SDD000001`, ...), unique within an
output directory, so pages from different templates never collide.

```
data/
  images/SDD000000.jpg        one image per page
  labels/SDD000000.json       annotations
  labels/SDD000000.ttl        the same page as an RDF graph (DoCO + schema.org)
  labels/SDD000000.jsonld     and as JSON-LD
  pdfs/SDD000000-SDD000001.pdf
  overlays/SDD000000_overlay.jpg   boxes drawn on the page, for spot checks
  manifest.json               document -> page ranges
```

A label file lists the page's annotations:

```json
{
  "document_id": "SDD000000",
  "page_number": 1,
  "total_pages": 2,
  "width": 816,
  "height": 1056,
  "annotations": [
    {
      "label": "name",
      "text_content": "Luis Paul",
      "entity_type": "PERSON",
      "generic_type": "PERSON",
      "x": 427, "y": 276.56, "width": 296, "height": 22,
      "box_2d": [523, 261, 886, 282],
      "section_id": "parties_section",
      "field_id": "to_section",
      "rdfa_typeof": "schema:Person doco-fd:FormField",
      "rdfa_property": "schema:name foaf:name"
    }
  ]
}
```

`x`/`y`/`width`/`height` are in page pixels; `box_2d` is the same box normalised to 0–1000.
`entity_type` is the specific label and `generic_type` its coarse class (`PERSON`, `ORG`,
`DATE`, `MONEY`, `ADDRESS`, `IDENTIFIER`, `TITLE`, `LABEL`, `TABLE`, `TEXT`, ...), so one dataset
serves both fine-grained extraction and coarse layout models; `--entity-types` filters on the
generic class. Table cells also carry `table_id`, `row_id` and `column_header`, and
`rdfa_typeof` / `rdfa_property` link each entity to DoCO and schema.org.

A `schema:name` takes its entity type from the thing it names: inside a `schema:Person` it is
`PERSON`, inside an `Organization` `ORG`, and the name of anything else (a product line, a drug, a
procedure) stays `TEXT`. Template authors mark the subject with `typeof` on the field or its container.
[docs/dataset-format.md](docs/dataset-format.md) has more on the format.

## Writing a template

A template is a folder holding `template.json` (its name, category and class), `template.html`
(Jinja2), `styles.css`, and a `BaseTemplate` subclass that generates the data. It imports only from
`synthdoc.templates`, so it works from any template directory. Entities are marked in the HTML with RDFa
attributes, which is how the renderer knows what to box. [docs/templates.md](docs/templates.md)
walks through one; `synthdoc.get_template("invoice")` is a working example to read.

## Benchmarks

`synthdoc[bench]` adds three tracks that run on generated data: OCR (word and character error
rate), NER (precision / recall / F1 against the ground-truth entities) and layout segmentation
(mAP at IoU thresholds). Engines are configured in `synthdoc/bench/configs/engines.yaml`.

```bash
synthdoc-bench --help
```

## Development

```bash
pip install -e ".[dev]"
playwright install chromium
pytest                      # fast tests; add --run-pagedjs for the browser rendering tests
```

## License

MIT. The DoCO-FD ontology in `ontologies/doco-fd/` carries its own license (CC BY 4.0).
