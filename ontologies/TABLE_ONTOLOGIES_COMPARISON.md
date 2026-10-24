# Comparison of Table Ontologies

A comprehensive comparison of formal ontologies and vocabularies for representing table structures in RDF/OWL.

---

## Summary

**Yes, there ARE formal ontologies for tables!** The main one is the **W3C CSV on the Web (CSVW)** vocabulary, which defines classes for `Table`, `Row`, `Column`, and `Cell`. However, CSVW is designed for **data tables** (like CSV/Excel), while **DoCO-FD is designed for document tables** (like forms and reports).

---

## Existing Table Ontologies

### 1. W3C CSV on the Web (CSVW)

**Namespace:** `http://www.w3.org/ns/csvw#`
**Status:** W3C Recommendation (February 2016)
**Purpose:** Metadata vocabulary for tabular data (CSV files, spreadsheets)

#### Core Classes

```turtle
csvw:TableGroup  # A collection of related tables
csvw:Table       # An annotated table
csvw:Row         # A horizontal arrangement of cells
csvw:Column      # A vertical arrangement of cells
csvw:Cell        # Intersection of a row and column
csvw:Schema      # Defines table structure
csvw:Dialect     # Parsing hints (delimiters, encodings, etc.)
```

#### Key Properties

```turtle
csvw:table       # Links TableGroup to Tables
csvw:row         # Links Table to Rows
csvw:column      # Links Table to Columns
csvw:url         # Points to the CSV file
csvw:tableSchema # Defines column structure
csvw:datatype    # Cell data type
csvw:primaryKey  # Uniqueness constraints
csvw:foreignKeys # Referential integrity
```

#### Use Case
- Converting CSV files to RDF
- Describing spreadsheet structure
- Data warehouse schemas
- Statistical datasets

#### Example

```turtle
@prefix csvw: <http://www.w3.org/ns/csvw#> .

<#products-table> a csvw:Table ;
    csvw:url <products.csv> ;
    csvw:tableSchema <#schema> .

<#schema> a csvw:Schema ;
    csvw:column <#col-name>, <#col-price> ;
    csvw:primaryKey "id" .

<#col-name> a csvw:Column ;
    csvw:name "product_name" ;
    csvw:datatype "string" .

<#col-price> a csvw:Column ;
    csvw:name "price" ;
    csvw:datatype "number" .
```

---

### 2. RDF Data Cube Vocabulary

**Namespace:** `http://purl.org/linked-data/cube#`
**Status:** W3C Recommendation (January 2014)
**Purpose:** Publishing multi-dimensional statistical data (OLAP cubes)

#### Core Classes

```turtle
qb:DataSet           # The entire dataset
qb:DataStructureDefinition  # Schema definition
qb:Observation       # A single measurement
qb:Slice             # Subset of observations
qb:ComponentProperty # Dimension/measure/attribute
```

#### Use Case
- Statistical datasets (census, financial reports)
- OLAP cubes and business intelligence
- Time series data
- Multi-dimensional aggregations

#### Example

```turtle
@prefix qb: <http://purl.org/linked-data/cube#> .

<#sales-data> a qb:DataSet ;
    qb:structure <#sales-structure> .

<#obs1> a qb:Observation ;
    qb:dataSet <#sales-data> ;
    <#dimension-region> "North" ;
    <#dimension-product> "Widget A" ;
    <#measure-revenue> 15000 .
```

---

### 3. DoCO (Document Components Ontology)

**Namespace:** `http://purl.org/spar/doco/`
**Status:** Part of SPAR Ontologies (Scholarly Publishing)
**Purpose:** Document structure (sections, paragraphs, figures)

#### Table-Related Classes

```turtle
doco:Table       # A table within a document
doco:Caption     # Table caption
doco:Label       # Generic label
doco:Section     # Document section (may contain tables)
```

#### Limitations
- ❌ No classes for rows, cells, or columns
- ❌ No properties for table internals
- ❌ No support for headers vs data cells
- ✅ Only defines the table as a whole component

---

### 4. Schema.org

**Namespace:** `http://schema.org/`
**Status:** Community vocabulary (Google, Microsoft, Yahoo, Yandex)
**Purpose:** General-purpose semantic markup for web pages

#### Table-Related Classes

```turtle
schema:Table     # A table on a web page
schema:Dataset   # Collection of data
```

#### Limitations
- ❌ No classes for rows, cells, or columns
- ❌ Very minimal table support
- ✅ Good for semantic entity types (Person, Organization, etc.)

---

## DoCO-FD: Filling the Gap for Document Tables

**Namespace:** `http://purl.org/doco-fd/`
**Status:** Our extension to DoCO
**Purpose:** Form-based business documents (invoices, medical records, contracts)

### Why DoCO-FD Was Needed

| Feature | CSVW | Data Cube | DoCO | Schema.org | **DoCO-FD** |
|---------|------|-----------|------|------------|-------------|
| **Target** | Data files | Statistics | Documents | Web pages | **Form documents** |
| **Table class** | ✅ csvw:Table | ✅ qb:DataSet | ✅ doco:Table | ✅ schema:Table | ✅ Uses doco:Table |
| **Row class** | ✅ csvw:Row | ✅ qb:Observation | ❌ None | ❌ None | ✅ **doco-fd:TableRow** |
| **Cell class** | ✅ csvw:Cell | ❌ None | ❌ None | ❌ None | ✅ **doco-fd:TableCell** |
| **Header class** | ❌ None | ❌ None | ❌ None | ❌ None | ✅ **doco-fd:TableHeader** |
| **Form fields** | ❌ None | ❌ None | ❌ None | ❌ None | ✅ **doco-fd:FormField** |
| **Field labels** | ❌ None | ❌ None | ❌ None | ❌ None | ✅ **doco-fd:fieldLabel** |
| **Embedded in HTML** | ❌ External CSV | ❌ Separate RDF | ✅ RDFa | ✅ RDFa | ✅ **RDFa** |

### DoCO-FD Classes

```turtle
# Extends DoCO
doco-fd:FormSection   # rdfs:subClassOf doco:Section
doco-fd:FormField     # rdfs:subClassOf doco:TextBox
doco-fd:KeyValuePair  # rdfs:subClassOf doco:TextBox
doco-fd:Header        # rdfs:subClassOf doco:FrontMatter
doco-fd:Footer        # rdfs:subClassOf doco:BackMatter

# NEW: Table internals (fills DOCO gap!)
doco-fd:TableRow      # rdfs:subClassOf owl:Thing
doco-fd:TableCell     # rdfs:subClassOf owl:Thing
doco-fd:TableHeader   # rdfs:subClassOf doco-fd:TableCell
```

### DoCO-FD Properties

```turtle
# Form field properties
doco-fd:fieldLabel    # The label text
doco-fd:fieldValue    # The value text

# Table properties
doco-fd:cellValue     # Cell content
doco-fd:columnHeader  # Column header text
doco-fd:rowHeader     # Row header text

# Structural relationships
doco-fd:hasField      # Section contains fields
doco-fd:hasRow        # Table contains rows
doco-fd:hasCell       # Row contains cells
```

---

## Use Case Comparison

### CSVW: Converting Product Catalog CSV

```csv
product_id,product_name,price
101,Widget A,25.00
102,Widget B,45.00
```

**CSVW Metadata:**
```json
{
  "@context": "http://www.w3.org/ns/csvw",
  "url": "products.csv",
  "tableSchema": {
    "columns": [
      {"name": "product_id", "datatype": "integer"},
      {"name": "product_name", "datatype": "string"},
      {"name": "price", "datatype": "number"}
    ],
    "primaryKey": "product_id"
  }
}
```

---

### DoCO-FD: Invoice Document Table

```html
<table typeof="doco:Table" resource="#products">
  <caption property="doco:caption">Products</caption>

  <thead>
    <tr typeof="doco-fd:TableRow">
      <th typeof="doco-fd:TableHeader"
          property="doco-fd:columnHeader">Product</th>
      <th typeof="doco-fd:TableHeader"
          property="doco-fd:columnHeader">Price</th>
    </tr>
  </thead>

  <tbody>
    <tr typeof="doco-fd:TableRow" resource="#row1">
      <td typeof="doco-fd:TableCell"
          property="doco-fd:cellValue">Widget A</td>
      <td typeof="doco-fd:TableCell schema:MonetaryAmount"
          property="doco-fd:cellValue schema:value">$25.00</td>
    </tr>
    <tr typeof="doco-fd:TableRow" resource="#row2">
      <td typeof="doco-fd:TableCell"
          property="doco-fd:cellValue">Widget B</td>
      <td typeof="doco-fd:TableCell schema:MonetaryAmount"
          property="doco-fd:cellValue schema:value">$45.00</td>
    </tr>
  </tbody>
</table>
```

**RDF Output:**
```turtle
@prefix doco: <http://purl.org/spar/doco/> .
@prefix doco-fd: <http://purl.org/doco-fd/> .
@prefix schema: <http://schema.org/> .

<#products> a doco:Table ;
    doco:caption "Products" ;
    doco-fd:hasRow <#row1>, <#row2> .

<#row1> a doco-fd:TableRow ;
    doco-fd:hasCell _:cell1_1, _:cell1_2 .

_:cell1_1 a doco-fd:TableCell ;
    doco-fd:cellValue "Widget A" .

_:cell1_2 a doco-fd:TableCell, schema:MonetaryAmount ;
    doco-fd:cellValue "$25.00" ;
    schema:value "$25.00" .
```

---

## Key Differences

### CSVW (Data Tables)

```
Purpose: Converting CSV files to RDF
Focus:   Data structure, constraints, validation
Target:  Databases, spreadsheets, data warehouses

Strengths:
✅ Rich schema definitions
✅ Data type validation
✅ Foreign key relationships
✅ W3C Recommendation

Limitations:
❌ External to documents (points to CSV files)
❌ Not embedded in HTML
❌ No support for document semantics
❌ No support for form fields
```

### DoCO-FD (Document Tables)

```
Purpose: Semantic markup for form documents
Focus:   Document structure, visual layout, entity extraction
Target:  Invoices, medical records, contracts, reports

Strengths:
✅ Embedded in HTML with RDFa
✅ Supports form fields (label-value pairs)
✅ Dual-layer markup (structure + semantics)
✅ Bounding box extraction for NER training
✅ Extends official DoCO standard

Limitations:
❌ Not a W3C standard (yet!)
❌ Less focus on data validation
❌ Simpler schema definitions
```

---

## When to Use Which

### Use CSVW when:
- Converting CSV files to RDF
- Describing database schemas
- Publishing statistical datasets
- Need data validation and constraints
- Working with spreadsheets

### Use RDF Data Cube when:
- Publishing OLAP cubes
- Statistical aggregations
- Multi-dimensional datasets
- Time series data
- Business intelligence reports

### Use DoCO-FD when:
- Marking up HTML documents
- Extracting entities from forms
- Training NER models on documents
- Generating synthetic training data
- Working with invoices, medical records, contracts
- Need bounding box extraction

---

## Could We Use CSVW Instead?

**Short answer:** No, because CSVW is designed for different use cases.

### Why CSVW Doesn't Fit Our Needs

1. **External Files vs. Embedded Markup**
   - CSVW: Points to external CSV files (`csvw:url "products.csv"`)
   - DoCO-FD: Embedded directly in HTML with RDFa

2. **Data vs. Documents**
   - CSVW: Describes data structure (like a database schema)
   - DoCO-FD: Describes document structure (like a form layout)

3. **No Form Field Support**
   - CSVW: Has no concept of "label" and "value" pairs
   - DoCO-FD: Built around FormField with fieldLabel and fieldValue

4. **No Document Context**
   - CSVW: Standalone tables
   - DoCO-FD: Tables within sections, with headers and footers

5. **Different Markup Style**
   - CSVW: JSON-LD metadata files separate from data
   - DoCO-FD: RDFa attributes directly in HTML elements

### Example Showing the Mismatch

**CSVW approach (doesn't work for our use case):**
```html
<!-- HTML document -->
<table id="products">
  <tr><th>Product</th><th>Price</th></tr>
  <tr><td>Widget A</td><td>$25.00</td></tr>
</table>

<!-- Separate JSON-LD metadata file -->
<script type="application/ld+json">
{
  "@context": "http://www.w3.org/ns/csvw",
  "url": "products.csv",  ← Points to CSV, not the HTML table!
  "tableSchema": { ... }
}
</script>
```

**DoCO-FD approach (works perfectly):**
```html
<table typeof="doco:Table" resource="#products">
  <tr typeof="doco-fd:TableRow">
    <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Product</th>
    <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Price</th>
  </tr>
  <tr typeof="doco-fd:TableRow">
    <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget A</td>
    <td typeof="doco-fd:TableCell schema:MonetaryAmount"
        property="doco-fd:cellValue schema:value">$25.00</td>
  </tr>
</table>
<!-- All metadata embedded directly in HTML! -->
```

---

## Complementary Usage

CSVW and DoCO-FD can be **complementary** in different parts of a workflow:

```
┌─────────────────────────────────────────────────┐
│  1. Create synthetic documents                  │
│     → Use DoCO-FD for HTML markup              │
│     → Extract entities with bounding boxes      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  2. Train NER model on documents                │
│     → Use DoCO-FD annotations                   │
│     → Model learns to extract from PDFs         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  3. Extract structured data from documents      │
│     → NER model identifies fields and values    │
│     → Convert to tabular format                 │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  4. Publish as CSV with CSVW metadata           │
│     → Use CSVW for data validation              │
│     → Publish to data warehouse                 │
└─────────────────────────────────────────────────┘
```

---

## Conclusion

### Summary Table

| Ontology | Purpose | Target Format | Status | Our Usage |
|----------|---------|---------------|--------|-----------|
| **CSVW** | Tabular data conversion | CSV files | W3C Rec | ❌ Not suitable |
| **Data Cube** | Statistical datasets | OLAP cubes | W3C Rec | ❌ Not suitable |
| **DoCO** | Document structure | HTML/PDF docs | Published | ✅ Base ontology |
| **Schema.org** | Semantic entities | Web pages | Community | ✅ Entity types |
| **DoCO-FD** | Form documents | HTML forms | Our extension | ✅ **Primary** |

### Key Takeaway

**Yes, formal table ontologies exist (CSVW, Data Cube), BUT:**
- They're designed for **data tables** (CSV, spreadsheets, databases)
- NOT for **document tables** (invoices, forms, reports)
- DoCO-FD fills the gap for **document-centric table markup**

**DoCO-FD is necessary because:**
1. No other ontology supports embedded HTML table markup with RDFa
2. No other ontology has form field label-value semantics
3. No other ontology integrates table internals with document structure
4. No other ontology supports bounding box extraction for NER training

---

## References

### W3C Specifications
- [CSV on the Web (CSVW)](https://www.w3.org/ns/csvw) - W3C Recommendation
- [RDF Data Cube Vocabulary](https://www.w3.org/TR/vocab-data-cube/) - W3C Recommendation
- [Model for Tabular Data and Metadata](https://www.w3.org/TR/tabular-data-model/)
- [Generating RDF from Tabular Data](https://www.w3.org/TR/csv2rdf/)

### Other Ontologies
- [DoCO (Document Components Ontology)](http://purl.org/spar/doco)
- [Schema.org](https://schema.org/)
- [FOAF (Friend of a Friend)](http://xmlns.com/foaf/0.1/)

### DoCO-FD
- [DoCO-FD Ontology](doco-fd/doco-fd.ttl)
- [DoCO-FD Documentation](doco-fd/README.md)
- [DoCO-FD Visual Guide](doco-fd/VISUAL_GUIDE.md)

---

**Last Updated:** January 13, 2026
