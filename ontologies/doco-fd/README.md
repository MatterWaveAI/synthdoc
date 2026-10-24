# DoCO-FD: Document Components Ontology - Form Documents Extension

**Version:** 1.0.0
**Date:** 2026-01-13
**License:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
**Namespace:** `http://purl.org/doco-fd/`
**Prefix:** `doco-fd:`

---

## Overview

DoCO-FD is a formal OWL 2 DL extension to the [Document Components Ontology (DoCO)](http://purl.org/spar/doco) that provides structured vocabulary for form-based documents. While DoCO excels at modeling academic papers and books, it lacks the specific classes and properties needed for business forms, government documents, invoices, medical records, and other structured data entry documents.

**DoCO-FD fills these gaps by adding:**
- Form-specific structural elements (FormSection, FormField)
- Table internals (TableRow, TableCell, TableHeader)
- Key-value pair semantics for label-value associations
- Document layout components (Header, Footer)

---

## Design Philosophy

### 1. **Extends, Doesn't Replace**

DoCO-FD is designed as a proper extension to DoCO:
- All new classes are subclasses of existing DoCO classes
- `FormSection` extends `doco:Section`
- `FormField` extends `doco:TextBox`
- `Header` extends `doco:FrontMatter`
- `Footer` extends `doco:BackMatter`

This ensures compatibility with existing DoCO-based systems while adding domain-specific semantics.

### 2. **Dual-Layer Markup**

DoCO-FD is designed to work alongside Schema.org for complete semantic annotation:

```html
<!-- Structural (DoCO-FD) + Semantic (Schema.org) -->
<div typeof="schema:Person doco-fd:FormField" resource="#patient">
  <span property="doco-fd:fieldLabel">Patient Name</span>
  <span property="schema:name doco-fd:fieldValue">John Doe</span>
</div>
```

- **DoCO-FD** describes document structure (it's a form field)
- **Schema.org** describes semantic meaning (it's a person)

### 3. **Addresses Real Gaps**

The biggest gap DoCO-FD fills is **table internals**. DoCO has `doco:Table` but nothing for rows, cells, or headers. This makes it impossible to properly annotate structured tabular data - a critical need for business documents.

---

## Classes

### Form Structure

#### `doco-fd:FormSection`
**Extends:** `doco:Section`

A logical grouping of related form fields within a document.

**Example:**
```html
<section typeof="doco-fd:FormSection" resource="#billingInfo">
  <h2 property="doco:sectionTitle">Billing Information</h2>
  <!-- form fields -->
</section>
```

**Use Cases:**
- Patient Information section in medical forms
- Billing Address section in invoices
- Employment History section in applications

---

#### `doco-fd:FormField`
**Extends:** `doco:TextBox`

A structured element for data entry or display, consisting of a label and value.

**Example:**
```html
<div typeof="doco-fd:FormField" resource="#invoiceNumber">
  <span property="doco-fd:fieldLabel">Invoice Number:</span>
  <span property="doco-fd:fieldValue">INV-2024-001</span>
</div>
```

**Use Cases:**
- Any labeled data field in forms
- Invoice line items
- Patient vital signs
- Tax form entries

---

#### `doco-fd:KeyValuePair`
**Extends:** `doco:TextBox`

A semantic pairing of a label (key) and its associated data value.

**Example:**
```html
<div typeof="doco-fd:KeyValuePair" resource="#totalAmount">
  <span property="doco-fd:fieldLabel">Total Amount:</span>
  <span property="doco-fd:fieldValue">$1,234.56</span>
</div>
```

**Use Cases:**
- Configuration settings
- Metadata key-values
- Summary totals
- Reference numbers

**Note:** KeyValuePair is semantically similar to FormField but emphasizes the key-value relationship pattern.

---

### Document Layout

#### `doco-fd:Header`
**Extends:** `doco:FrontMatter`

The top section of a document containing identifying information, logos, titles, and metadata.

**Example:**
```html
<header typeof="doco-fd:Header" resource="#docHeader">
  <h1 property="doco:title">Invoice</h1>
  <div property="schema:identifier">INV-2024-001</div>
</header>
```

**Use Cases:**
- Invoice headers with company logo
- Medical record headers with patient ID
- Legal document headers with case numbers

---

#### `doco-fd:Footer`
**Extends:** `doco:BackMatter`

The bottom section of a document containing supplementary information, disclaimers, and legal notices.

**Example:**
```html
<footer typeof="doco-fd:Footer" resource="#docFooter">
  <p property="doco:footnote">All amounts in USD. Payment due within 30 days.</p>
</footer>
```

**Use Cases:**
- Page numbers and document metadata
- Legal disclaimers
- Contact information
- Terms and conditions

---

### Table Components

#### `doco-fd:TableRow`

A horizontal sequence of table cells representing a single record.

**Example:**
```html
<tr typeof="doco-fd:TableRow" resource="#row1">
  <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Product A</td>
  <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">$25.00</td>
</tr>
```

---

#### `doco-fd:TableCell`

An individual data container at the intersection of a row and column.

**Example:**
```html
<td typeof="doco-fd:TableCell" property="doco-fd:cellValue">$1,234.56</td>
```

**With dual markup:**
```html
<td typeof="doco-fd:TableCell schema:MonetaryAmount"
    property="doco-fd:cellValue schema:value">
  $1,234.56
</td>
```

---

#### `doco-fd:TableHeader`
**Extends:** `doco-fd:TableCell`

A cell that provides a descriptive label for a column or row.

**Example:**
```html
<thead>
  <tr>
    <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Product</th>
    <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Price</th>
  </tr>
</thead>
```

---

## Properties

### Object Properties (Structural Relationships)

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `doco-fd:hasField` | FormSection | FormField | Section contains field |
| `doco-fd:hasRow` | doco:Table | TableRow | Table contains row |
| `doco-fd:hasCell` | TableRow | TableCell | Row contains cell |

---

### Data Properties (Content)

#### Field Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `doco-fd:fieldLabel` | FormField | xsd:string | Descriptive label for field |
| `doco-fd:fieldValue` | FormField | rdfs:Literal | Data content of field |

#### Table Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `doco-fd:cellValue` | TableCell | rdfs:Literal | Content of table cell |
| `doco-fd:columnHeader` | TableHeader | xsd:string | Column header text |
| `doco-fd:rowHeader` | TableHeader | xsd:string | Row header text |

#### Layout Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `doco-fd:rowIndex` | TableRow | xsd:nonNegativeInteger | Zero-based row position |
| `doco-fd:columnIndex` | TableCell | xsd:nonNegativeInteger | Zero-based column position |

---

## Complete Example: Invoice

```html
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:schema="http://schema.org/"
      xmlns:doco="http://purl.org/spar/doco/"
      xmlns:doco-fd="http://purl.org/doco-fd/"
      xmlns:foaf="http://xmlns.com/foaf/0.1/">

<body typeof="schema:Invoice doco:BodyMatter" resource="#invoice">

  <!-- Header -->
  <header typeof="doco-fd:Header" resource="#header">
    <h1 property="doco:title">Invoice</h1>
    <div typeof="doco-fd:FormField" resource="#invoiceNumber">
      <span property="doco-fd:fieldLabel">Invoice Number:</span>
      <span property="schema:identifier doco-fd:fieldValue">INV-2024-001</span>
    </div>
  </header>

  <!-- Customer Information Section -->
  <section typeof="doco-fd:FormSection" resource="#customerInfo">
    <h2 property="doco:sectionTitle">Customer Information</h2>

    <div typeof="schema:Person doco-fd:FormField" resource="#customer">
      <span property="doco-fd:fieldLabel">Customer Name:</span>
      <span property="schema:name doco-fd:fieldValue">John Smith</span>
    </div>

    <div typeof="schema:PostalAddress doco-fd:FormField" resource="#billingAddress">
      <span property="doco-fd:fieldLabel">Billing Address:</span>
      <span property="schema:streetAddress doco-fd:fieldValue">123 Main St, Anytown, USA</span>
    </div>
  </section>

  <!-- Line Items Table -->
  <table typeof="doco:Table" resource="#lineItems">
    <caption property="doco:caption">Line Items</caption>

    <thead>
      <tr typeof="doco-fd:TableRow">
        <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Description</th>
        <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Quantity</th>
        <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Price</th>
      </tr>
    </thead>

    <tbody>
      <tr typeof="doco-fd:TableRow" resource="#item1">
        <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget A</td>
        <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">5</td>
        <td typeof="doco-fd:TableCell schema:MonetaryAmount"
            property="doco-fd:cellValue schema:value">$25.00</td>
      </tr>
      <tr typeof="doco-fd:TableRow" resource="#item2">
        <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget B</td>
        <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">3</td>
        <td typeof="doco-fd:TableCell schema:MonetaryAmount"
            property="doco-fd:cellValue schema:value">$45.00</td>
      </tr>
    </tbody>
  </table>

  <!-- Total -->
  <div typeof="doco-fd:KeyValuePair schema:MonetaryAmount" resource="#total">
    <span property="doco-fd:fieldLabel">Total Amount:</span>
    <span property="schema:value doco-fd:fieldValue">$1,234.56</span>
  </div>

  <!-- Footer -->
  <footer typeof="doco-fd:Footer" resource="#footer">
    <p property="doco:footnote">Payment due within 30 days. All amounts in USD.</p>
  </footer>

</body>
</html>
```

---

## Usage with RDFLib

```python
from rdflib import Graph, Namespace

# Load DoCO-FD ontology
g = Graph()
g.parse("doco-fd.ttl", format="turtle")

# Define namespaces
DOCO_FD = Namespace("http://purl.org/doco-fd/")
g.bind("doco-fd", DOCO_FD)

# Parse RDFa from HTML
g.parse(data=html_content, format="rdfa", publicID="http://example.org/invoice")

# Query for all form fields
query = """
    PREFIX doco-fd: <http://purl.org/doco-fd/>

    SELECT ?field ?label ?value
    WHERE {
        ?field a doco-fd:FormField ;
               doco-fd:fieldLabel ?label ;
               doco-fd:fieldValue ?value .
    }
"""

results = g.query(query)
for row in results:
    print(f"{row.label}: {row.value}")
```

---

## Integration with Existing Tools

### Update extract_field_relationships.py

```python
from rdflib import Namespace

# Add DoCO-FD namespace
DOCO_FD = Namespace("http://purl.org/doco-fd/")

def _expand_curie(curie: str) -> str:
    namespace_map = {
        'schema': 'http://schema.org/',
        'doco': 'http://purl.org/spar/doco/',
        'doco-fd': 'http://purl.org/doco-fd/',  # Add this
        'foaf': 'http://xmlns.com/foaf/0.1/',
        'dc': 'http://purl.org/dc/terms/',
    }
    # ... rest of function
```

### Update pagedjs_renderer.py

Add DoCO-FD selectors:

```javascript
const valueSelectors = [
    '[property*="doco-fd:fieldValue"]',
    '[property*="doco-fd:cellValue"]',
    '[property*="doco-fd:columnHeader"]',
    // ... existing selectors
];
```

---

## Validation and Quality Assurance

### OWL Validation

The ontology can be validated using:
- **Protégé:** Import `doco-fd.ttl` and run reasoner
- **Robot:** `robot validate --input doco-fd.ttl`
- **Online:** [OWL Validator](https://www.w3.org/RDF/Validator/)

### Consistency Checks

- All classes are properly subclassed from DoCO
- All properties have defined domains and ranges
- No circular dependencies
- Disjointness where appropriate

---

## Comparison with Alternatives

### vs. Pure DoCO

| Concept | DoCO | DoCO-FD |
|---------|------|---------|
| Form field | `doco:TextBox` | `doco-fd:FormField` (more specific) |
| Header | `doco:FrontMatter` | `doco-fd:Header` (more specific) |
| Table row | ❌ Not supported | ✅ `doco-fd:TableRow` |
| Table cell | ❌ Not supported | ✅ `doco-fd:TableCell` |
| Key-value pair | ❌ Not supported | ✅ `doco-fd:KeyValuePair` |

### vs. Schema.org

Schema.org provides semantic types (Person, Organization, Invoice) but lacks document structure vocabulary. DoCO-FD and Schema.org complement each other perfectly through dual-layer markup.

### vs. Custom data-* Attributes

| Approach | Interoperability | Reasoning | Standards |
|----------|------------------|-----------|-----------|
| data-* attributes | ❌ Poor | ❌ No reasoning | ❌ Non-standard |
| DoCO-FD | ✅ Excellent | ✅ OWL 2 DL | ✅ W3C aligned |

---

## Roadmap

### Version 1.0.0 (Current)
- ✅ Core form structure classes
- ✅ Table internal components
- ✅ Basic properties for fields and cells

### Version 1.1.0 (Planned)
- [ ] Validation constraints (required fields, data types)
- [ ] Field grouping patterns
- [ ] Conditional field visibility
- [ ] Multi-language label support

### Version 2.0.0 (Future)
- [ ] Form submission semantics
- [ ] Field interdependencies
- [ ] Calculated fields
- [ ] Integration with W3C Web Forms standards

---

## Contributing

We welcome contributions! To propose changes:

1. Open an issue describing the use case
2. Provide examples from real documents
3. Ensure backward compatibility with DoCO
4. Submit pull request with updated ontology and documentation

---

## Citation

If you use DoCO-FD in your work, please cite:

```bibtex
@misc{doco-fd,
  title = {DoCO-FD: Document Components Ontology - Form Documents Extension},
  author = {Blass, David},
  year = {2026},
  version = {1.0.0},
  url = {http://purl.org/doco-fd/},
  note = {An OWL 2 DL extension to the Document Components Ontology for form-based documents}
}
```

---

## References

- **DoCO:** Constantin, A., et al. (2016). "The Document Components Ontology (DoCO)." *Semantic Web*, 7(2), 167-181. DOI: 10.3233/SW-150177
- **Schema.org:** https://schema.org/
- **RDFa:** https://www.w3.org/TR/rdfa-primer/
- **OWL 2:** https://www.w3.org/TR/owl2-overview/

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit and indicate if changes were made
