# Ontologies Directory

This directory contains formal ontologies used by the synthetic document dataset generator.

---

## DoCO-FD (Document Components Ontology - Form Documents Extension)

**Location:** [`doco-fd/`](doco-fd/)

**Purpose:** Extends the [Document Components Ontology (DoCO)](http://purl.org/spar/doco) with classes and properties specific to form-based business documents.

**Version:** 1.0.0

**Namespace:** `http://purl.org/doco-fd/`

**Files:**
- [`doco-fd.ttl`](doco-fd/doco-fd.ttl) - OWL 2 DL ontology in Turtle format
- [`README.md`](doco-fd/README.md) - Complete documentation
- [`LICENSE`](doco-fd/LICENSE) - CC BY 4.0
- [`examples/`](doco-fd/examples/) - Usage examples

### What DoCO-FD Adds

DoCO-FD fills critical gaps in DoCO for form-based documents:

| Concept | DoCO (Official) | DoCO-FD (Our Extension) |
|---------|-----------------|-------------------------|
| Form sections | `doco:Section` (generic) | `doco-fd:FormSection` (specific) |
| Form fields | `doco:TextBox` (generic) | `doco-fd:FormField` (specific) |
| Key-value pairs | ❌ Not supported | ✅ `doco-fd:KeyValuePair` |
| Table rows | ❌ Not supported | ✅ `doco-fd:TableRow` |
| Table cells | ❌ Not supported | ✅ `doco-fd:TableCell` |
| Column headers | ❌ Not supported | ✅ `doco-fd:columnHeader` |
| Field labels | ❌ Not supported | ✅ `doco-fd:fieldLabel` |
| Field values | ❌ Not supported | ✅ `doco-fd:fieldValue` |

### Quick Example

```html
<html xmlns:doco-fd="http://purl.org/doco-fd/"
      xmlns:schema="http://schema.org/">

  <!-- Form field with dual-layer markup -->
  <div typeof="schema:Person doco-fd:FormField" resource="#patient">
    <span property="doco-fd:fieldLabel">Patient Name:</span>
    <span property="schema:name doco-fd:fieldValue">John Doe</span>
  </div>

  <!-- Table with internal structure -->
  <table typeof="doco:Table" resource="#results">
    <tr typeof="doco-fd:TableRow">
      <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Test</th>
      <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Result</th>
    </tr>
    <tr typeof="doco-fd:TableRow">
      <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Blood Pressure</td>
      <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">120/80</td>
    </tr>
  </table>

</html>
```

---

## Integration with Project

### RDFa Parsing

All templates use DoCO-FD markup in their `template.html` files. The RDF extraction pipeline recognizes DoCO-FD namespaces:

```python
from rdflib import Namespace

DOCO_FD = Namespace("http://purl.org/doco-fd/")
g.bind("doco-fd", DOCO_FD)
```

### Bounding Box Extraction

The PagedJS renderer recognizes DoCO-FD properties for overlay generation:

```javascript
const valueSelectors = [
    '[property*="doco-fd:fieldValue"]',
    '[property*="doco-fd:cellValue"]',
    '[property*="doco-fd:columnHeader"]',
    // ...
];
```

### Entity Type Inference

Entity types are inferred from both DoCO-FD and Schema.org properties:

```python
def _infer_entity_type_from_property(property_attr: str) -> str:
    if 'doco-fd:fieldLabel' in property_attr:
        return 'FIELD_LABEL'
    elif 'doco-fd:cellValue' in property_attr:
        return 'TABLE_CELL'
    elif 'schema:name' in property_attr:
        return 'PERSON'
    # ...
```

---

## External References

### Official DOCO

- **Ontology:** http://purl.org/spar/doco
- **Documentation:** https://sparontologies.github.io/doco/current/doco.html
- **Local copy:** [`../doco.ttl`](../doco.ttl)

### Schema.org

- **Website:** https://schema.org/
- **RDF Schema:** https://schema.org/version/latest/schemaorg-current-https.ttl

### FOAF (Friend of a Friend)

- **Ontology:** http://xmlns.com/foaf/0.1/
- **Spec:** http://xmlns.com/foaf/spec/

### Dublin Core

- **Ontology:** http://purl.org/dc/terms/
- **Website:** https://www.dublincore.org/

---

## Publishing DoCO-FD

To make DoCO-FD publicly available:

### 1. GitHub Repository

Create a dedicated repository:
```
github.com/yourusername/doco-fd
├── doco-fd.ttl
├── README.md
├── LICENSE
├── examples/
└── docs/
```

### 2. Request PURL

Submit request to http://purl.org/ for permanent URI:
- Requested: `http://purl.org/doco-fd/`
- Redirects to: `https://yourusername.github.io/doco-fd/doco-fd.ttl`

### 3. W3C Community Group

Consider starting a W3C Community Group for form document ontologies:
- https://www.w3.org/community/

### 4. LOV (Linked Open Vocabularies)

Submit to LOV for discoverability:
- https://lov.linkeddata.es/dataset/lov/

---

## Citation

```bibtex
@misc{doco-fd,
  title = {DoCO-FD: Document Components Ontology - Form Documents Extension},
  author = {Blass, David},
  year = {2026},
  version = {1.0.0},
  url = {http://purl.org/doco-fd/},
  license = {CC-BY-4.0},
  note = {An OWL 2 DL extension to the Document Components Ontology}
}
```

---

## Contributing

We welcome contributions to DoCO-FD! See [`doco-fd/README.md`](doco-fd/README.md) for details.

Key areas for contribution:
- Additional document type examples
- Validation rules and constraints
- Integration with other ontologies
- Translation to other RDF formats (JSON-LD context, etc.)

---

## License

All ontologies in this directory are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
