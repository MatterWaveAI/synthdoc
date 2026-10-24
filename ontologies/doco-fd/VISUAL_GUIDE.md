# DoCO-FD Visual Guide

A comprehensive visual reference for understanding and using the Document Components Ontology - Form Documents Extension.

---

## Table of Contents

1. [Ontology Architecture](#ontology-architecture)
2. [Class Hierarchy](#class-hierarchy)
3. [Document Structure](#document-structure)
4. [Form Field Anatomy](#form-field-anatomy)
5. [Table Structure](#table-structure)
6. [Dual-Layer Markup](#dual-layer-markup)
7. [RDF Graph Visualization](#rdf-graph-visualization)
8. [Migration Patterns](#migration-patterns)

---

## Ontology Architecture

### The Three-Layer Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR DOCUMENTS                            │
│  (Invoices, Medical Records, Tax Forms, Contracts, etc.)   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ annotated with
                            │
┌─────────────────────────────────────────────────────────────┐
│               DoCO-FD (Form Documents)                       │
│                                                              │
│  • FormField, FormSection, KeyValuePair                     │
│  • TableRow, TableCell, TableHeader                         │
│  • Header, Footer                                            │
│  • fieldLabel, fieldValue, cellValue                        │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ extends
                            │
┌─────────────────────────────────────────────────────────────┐
│                  DoCO (Document Components)                  │
│                                                              │
│  • Section, Paragraph, Table                                │
│  • FrontMatter, BodyMatter, BackMatter                      │
│  • Title, Label, TextBox                                    │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ uses
                            │
┌─────────────────────────────────────────────────────────────┐
│              RDF/OWL (Semantic Web Foundation)              │
│                                                              │
│  • Classes, Properties, Resources                           │
│  • Triples (Subject-Predicate-Object)                       │
│  • Reasoning and Inference                                  │
└─────────────────────────────────────────────────────────────┘
```

### Integration with Semantic Vocabularies

```
┌──────────────┐
│   DoCO-FD    │ ◄──── Document Structure (HOW it's organized)
│  (Structural)│
└──────────────┘
       │
       │ Used together via
       │ Dual-Layer Markup
       │
       ▼
┌──────────────┐
│  Schema.org  │ ◄──── Semantic Meaning (WHAT it represents)
│  (Semantic)  │
└──────────────┘

Example:
  <div typeof="schema:Person doco-fd:FormField">
           └─ Semantic      └─ Structural
```

---

## Class Hierarchy

### Complete DoCO-FD Class Tree

```
owl:Thing
│
├─ doco:Section ◄──────────────┐
│  └─ doco-fd:FormSection      │ Form-specific
│                               │ structures
├─ doco:TextBox ◄──────────────┤
│  ├─ doco-fd:FormField        │
│  └─ doco-fd:KeyValuePair     │
│                               │
├─ doco:FrontMatter ◄──────────┤
│  └─ doco-fd:Header           │ Document layout
│                               │
├─ doco:BackMatter ◄───────────┤
│  └─ doco-fd:Footer           │
│                               │
├─ doco:Table ◄────────────────┘
│  (no DoCO subclasses)
│
├─ doco-fd:TableRow ◄──────────┐
│                               │ Table internals
├─ doco-fd:TableCell ◄─────────┤ (NEW in DoCO-FD)
│  └─ doco-fd:TableHeader      │
└────────────────────────────────┘
```

### Property Hierarchy

```
Properties
│
├─ Object Properties (Relationships)
│  │
│  ├─ doco-fd:hasField
│  │    Domain: FormSection
│  │    Range:  FormField
│  │
│  ├─ doco-fd:hasRow
│  │    Domain: doco:Table
│  │    Range:  TableRow
│  │
│  └─ doco-fd:hasCell
│       Domain: TableRow
│       Range:  TableCell
│
└─ Data Properties (Content)
   │
   ├─ Field Properties
   │  ├─ doco-fd:fieldLabel    → xsd:string
   │  └─ doco-fd:fieldValue    → rdfs:Literal
   │
   ├─ Table Properties
   │  ├─ doco-fd:cellValue     → rdfs:Literal
   │  ├─ doco-fd:columnHeader  → xsd:string
   │  └─ doco-fd:rowHeader     → xsd:string
   │
   └─ Layout Properties
      ├─ doco-fd:rowIndex      → xsd:nonNegativeInteger
      └─ doco-fd:columnIndex   → xsd:nonNegativeInteger
```

---

## Document Structure

### Typical Invoice Layout

```
┌─────────────────────────────────────────────────────────────┐
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃  Header (doco-fd:Header)                               ┃ │
│ ┃  ┌──────────────────────────────────────────────────┐  ┃ │
│ ┃  │ Invoice                  [doco:title]            │  ┃ │
│ ┃  │ Invoice #: INV-001       [FormField]             │  ┃ │
│ ┃  │ Date: 2026-01-13         [FormField]             │  ┃ │
│ ┃  └──────────────────────────────────────────────────┘  ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ FormSection: Customer Information                      │ │
│ │ ┌────────────────────────────────────────────────────┐ │ │
│ │ │ FormField: Customer Name   │ John Smith            │ │ │
│ │ │            [fieldLabel]    │ [fieldValue]          │ │ │
│ │ ├────────────────────────────────────────────────────┤ │ │
│ │ │ FormField: Address         │ 123 Main St           │ │ │
│ │ └────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ FormSection: Line Items                                │ │
│ │ ┌────────────────────────────────────────────────────┐ │ │
│ │ │ Table (doco:Table)                                 │ │ │
│ │ │ ┌─────────────┬──────────┬─────────┬─────────────┐ │ │ │
│ │ │ │ TableHeader │TableHeader│TableHdr │ TableHeader │ │ │ │
│ │ │ │ Description │ Quantity  │  Price  │   Amount    │ │ │ │
│ │ │ ├─────────────┼──────────┼─────────┼─────────────┤ │ │ │
│ │ │ │ TableCell   │TableCell │TableCell│  TableCell  │ │ │ │
│ │ │ │ Widget A    │    5     │ $25.00  │  $125.00    │ │ │ │
│ │ │ ├─────────────┼──────────┼─────────┼─────────────┤ │ │ │
│ │ │ │ TableCell   │TableCell │TableCell│  TableCell  │ │ │ │
│ │ │ │ Widget B    │    3     │ $45.00  │  $135.00    │ │ │ │
│ │ │ └─────────────┴──────────┴─────────┴─────────────┘ │ │ │
│ │ └────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ KeyValuePair: Total        │ $260.00                   │ │
│ │               [fieldLabel] │ [fieldValue]              │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃  Footer (doco-fd:Footer)                               ┃ │
│ ┃  Payment due within 30 days. All amounts in USD.       ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
└─────────────────────────────────────────────────────────────┘
```

---

## Form Field Anatomy

### The Key-Value Pattern

```
┌────────────────────────────────────────────────────────────┐
│  FormField (doco-fd:FormField)                             │
│  resource="#customerName"                                  │
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │   Field Label    │   :    │     Field Value         │  │
│  │                  │        │                         │  │
│  │ "Customer Name"  │        │    "John Smith"         │  │
│  │                  │        │                         │  │
│  │ doco-fd:         │        │ schema:name             │  │
│  │   fieldLabel     │        │ doco-fd:fieldValue      │  │
│  └──────────────────┘        └─────────────────────────┘  │
│        ▲                              ▲                    │
│        │                              │                    │
│    Describes WHAT                 The DATA                │
│    (metadata)                     (content)               │
└────────────────────────────────────────────────────────────┘
```

### HTML Representation

```html
<!-- Visual Breakdown -->
<div typeof="schema:Person doco-fd:FormField" resource="#customerName">
│    └──┬─┘           └────┬────┘        └──────┬──────┘
│       │                  │                     │
│   Semantic type    Structural type      Unique identifier
│   (WHAT it is)     (HOW it's shown)     (for RDF graph)
│
  <span property="doco-fd:fieldLabel">Customer Name:</span>
  │               └───────┬────────┘      └──────┬──────┘
  │                       │                      │
  │                  Property name          Label text
  │                  (RDF predicate)        (displayed)
  │
  <span property="schema:name doco-fd:fieldValue">John Smith</span>
        │         └─────┬────┘ └──────┬────────┘  └────┬─────┘
        │               │             │                 │
        │          Semantic      Structural         Value text
        │          property      property           (data)
        │          (person's     (field's
        │           name)         value)
</div>
```

### Field Types Comparison

```
┌─────────────────────┬─────────────────┬──────────────────────┐
│   FormField         │  KeyValuePair   │   Plain Text         │
├─────────────────────┼─────────────────┼──────────────────────┤
│                     │                 │                      │
│ ┌─────────────────┐ │ ┌─────────────┐ │ ┌──────────────────┐ │
│ │ Label: Value    │ │ │ Key: Value  │ │ │ Just text here   │ │
│ │                 │ │ │             │ │ │                  │ │
│ │ [Interactive    │ │ │ [Config     │ │ │ [No structure]   │ │
│ │  data entry]    │ │ │  setting]   │ │ │                  │ │
│ └─────────────────┘ │ └─────────────┘ │ └──────────────────┘ │
│                     │                 │                      │
│ Use: Forms,         │ Use: Metadata,  │ Use: Paragraphs,     │
│      Applications   │      Summaries  │      Descriptions    │
└─────────────────────┴─────────────────┴──────────────────────┘
```

---

## Table Structure

### Table Component Hierarchy

```
┌──────────────────────────────────────────────────────────────┐
│  Table (doco:Table)                                          │
│  resource="#productTable"                                    │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TableRow (doco-fd:TableRow) - Header Row              │ │
│  │  resource="#headerRow"                                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │ TableHeader  │  │ TableHeader  │  │ TableHeader │  │ │
│  │  │ "Product"    │  │ "Quantity"   │  │ "Price"     │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TableRow (doco-fd:TableRow) - Data Row #1             │ │
│  │  resource="#row1"                                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │ TableCell    │  │ TableCell    │  │ TableCell   │  │ │
│  │  │ "Widget A"   │  │ "5"          │  │ "$25.00"    │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TableRow (doco-fd:TableRow) - Data Row #2             │ │
│  │  resource="#row2"                                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │ TableCell    │  │ TableCell    │  │ TableCell   │  │ │
│  │  │ "Widget B"   │  │ "3"          │  │ "$45.00"    │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Table Cell Markup Detail

```
Single Table Cell Breakdown:

<td typeof="doco-fd:TableCell schema:MonetaryAmount"
    property="doco-fd:cellValue schema:value">
  $125.00
</td>

Visualized:

┌─────────────────────────────────────────────────────────┐
│  <td> Element                                           │
│  ┌───────────────────────────────────────────────────┐ │
│  │  typeof (Classes)                                 │ │
│  │  ┌──────────────────┐  ┌────────────────────────┐ │ │
│  │  │ doco-fd:         │  │ schema:                │ │ │
│  │  │   TableCell      │  │   MonetaryAmount       │ │ │
│  │  │                  │  │                        │ │ │
│  │  │ (Structure:      │  │ (Semantics:            │ │ │
│  │  │  It's a cell)    │  │  It's money)           │ │ │
│  │  └──────────────────┘  └────────────────────────┘ │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │  property (RDF Predicates)                        │ │
│  │  ┌──────────────────┐  ┌────────────────────────┐ │ │
│  │  │ doco-fd:         │  │ schema:                │ │ │
│  │  │   cellValue      │  │   value                │ │ │
│  │  │                  │  │                        │ │ │
│  │  │ (Cell's text     │  │ (Monetary              │ │ │
│  │  │  content)        │  │  value)                │ │ │
│  │  └──────────────────┘  └────────────────────────┘ │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Content: "$125.00"                               │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Table vs. Form Fields

```
Table Layout                    Form Layout
══════════════                  ════════════

┌─────────────────────┐         ┌────────────────────────┐
│ ╔═══╦═══╦═══╗       │         │ Label:  [Value]        │
│ ║ H ║ H ║ H ║       │         │ Label:  [Value]        │
│ ╠═══╬═══╬═══╣       │         │ Label:  [Value]        │
│ ║ C ║ C ║ C ║       │         │ Label:  [Value]        │
│ ╠═══╬═══╬═══╣       │         └────────────────────────┘
│ ║ C ║ C ║ C ║       │
│ ╚═══╩═══╩═══╝       │         Each is a FormField
└─────────────────────┘

Cells in grid structure         Label-value pairs
Best for: Repeated data         Best for: Unique fields
          Multiple records               Single record
```

---

## Dual-Layer Markup

### Why Two Vocabularies?

```
┌───────────────────────────────────────────────────────────┐
│                    Complete Information                    │
└───────────────────────────────────────────────────────────┘
                            ▲
                            │
         ┌──────────────────┴─────────────────┐
         │                                    │
         │                                    │
┌────────▼────────────┐           ┌───────────▼──────────┐
│   DoCO-FD Layer     │           │  Schema.org Layer    │
│   (Structure)       │           │  (Semantics)         │
├─────────────────────┤           ├──────────────────────┤
│ "HOW it's shown"    │           │ "WHAT it means"      │
│                     │           │                      │
│ • FormField         │           │ • Person             │
│ • TableCell         │           │ • MonetaryAmount     │
│ • FormSection       │           │ • Organization       │
│ • Header/Footer     │           │ • PostalAddress      │
└─────────────────────┘           └──────────────────────┘
```

### Layering Example

```html
<!-- Layer 1: Just HTML (No Semantics) -->
<div>
  <span>Patient Name:</span>
  <span>John Doe</span>
</div>
<!-- Problem: Computer can't understand this -->


<!-- Layer 2: Add DoCO-FD (Structure) -->
<div typeof="doco-fd:FormField">
  <span property="doco-fd:fieldLabel">Patient Name:</span>
  <span property="doco-fd:fieldValue">John Doe</span>
</div>
<!-- Better: Now we know it's a form field with label/value -->


<!-- Layer 3: Add Schema.org (Semantics) -->
<div typeof="schema:Person doco-fd:FormField" resource="#patient">
  <span property="doco-fd:fieldLabel">Patient Name:</span>
  <span property="schema:name doco-fd:fieldValue">John Doe</span>
</div>
<!-- Best: Now we know BOTH structure AND meaning! -->
```

### Information Extraction Benefit

```
Without Dual-Layer:
┌──────────────────────┐
│ "John Doe"           │  → What is this? Text? Name? Address?
└──────────────────────┘     ❓ Ambiguous


With Dual-Layer:
┌──────────────────────────────────────────────────────┐
│ typeof="schema:Person doco-fd:FormField"             │
│ property="schema:name doco-fd:fieldValue"            │
│                                                       │
│ "John Doe"                                           │
└──────────────────────────────────────────────────────┘
         │                          │
         ▼                          ▼
    ✓ It's a Person's name    ✓ It's in a form field
    ✓ Use NER model          ✓ Extract as key-value
    ✓ Link to other          ✓ Pair with label
      Person properties         "Patient Name:"
```

---

## RDF Graph Visualization

### Simple Field as RDF Graph

HTML:
```html
<div typeof="schema:Person doco-fd:FormField" resource="#patient">
  <span property="doco-fd:fieldLabel">Patient Name</span>
  <span property="schema:name doco-fd:fieldValue">John Doe</span>
</div>
```

RDF Graph:
```
                    ┌──────────────────┐
                    │   #patient       │  (Resource/Subject)
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           │                 │                 │
      rdf:type          doco-fd:         schema:name
           │            fieldValue            │
           │                 │                 │
           ▼                 ▼                 ▼
    ┌──────────┐      ┌───────────┐    ┌───────────┐
    │ schema:  │      │ "John Doe"│    │ "John Doe"│
    │  Person  │      │ (literal) │    │ (literal) │
    └──────────┘      └───────────┘    └───────────┘

    ┌─────────────────────────────────────────────────┐
    │  Triple 1: #patient  rdf:type      schema:Person│
    │  Triple 2: #patient  doco-fd:      "John Doe"   │
    │                      fieldValue                  │
    │  Triple 3: #patient  schema:name   "John Doe"   │
    └─────────────────────────────────────────────────┘
```

### Table as RDF Graph

HTML:
```html
<table typeof="doco:Table" resource="#products">
  <tr typeof="doco-fd:TableRow" resource="#row1">
    <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget A</td>
    <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">$25.00</td>
  </tr>
</table>
```

RDF Graph:
```
         ┌────────────┐
         │ #products  │ (Table)
         └─────┬──────┘
               │
         doco-fd:hasRow
               │
               ▼
         ┌────────────┐
         │   #row1    │ (Row)
         └─────┬──────┘
               │
        ┌──────┴──────┐
        │             │
  doco-fd:hasCell  doco-fd:hasCell
        │             │
        ▼             ▼
   ┌─────────┐   ┌─────────┐
   │ _:cell1 │   │ _:cell2 │ (Cells)
   └────┬────┘   └────┬────┘
        │             │
 doco-fd:cellValue  doco-fd:cellValue
        │             │
        ▼             ▼
   "Widget A"     "$25.00"
```

### Complete Invoice Graph

```
                        ┌──────────────┐
                        │  #invoice    │ (Root)
                        └──────┬───────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
         doco-fd:         doco-fd:         doco-fd:
          hasHeader        hasSection       hasFooter
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │ #header  │     │#customer │     │ #footer  │
        └────┬─────┘     │   Info   │     └────┬─────┘
             │           └────┬─────┘          │
      doco-fd:hasField        │           doco:footnote
             │           doco-fd:hasField      │
             ▼                │                ▼
      ┌───────────┐           ▼         "Payment due..."
      │#invoiceNum│    ┌──────────────┐
      └─────┬─────┘    │#customerName │
            │          └──────┬───────┘
    doco-fd:fieldValue        │
            │          schema:name,
            ▼          doco-fd:fieldValue
      "INV-2026-001"          │
                              ▼
                        "John Smith"
```

---

## Migration Patterns

### Before & After: Form Field

#### Before (data-* attributes)
```html
<div data-label="Patient Name" data-entity-type="PERSON">
  John Doe
</div>
```

```
Visual representation:
┌────────────────────────────────┐
│ data-label="Patient Name"      │ ← Custom, non-standard
│ data-entity-type="PERSON"      │ ← Not in RDF graph
│                                 │
│ John Doe                        │ ← Just text
└────────────────────────────────┘

Problems:
❌ Not machine-readable (RDF)
❌ No semantic interoperability
❌ Can't reason or infer
❌ No standard vocabulary
```

#### After (DoCO-FD + RDFa)
```html
<div typeof="schema:Person doco-fd:FormField" resource="#patient">
  <span property="doco-fd:fieldLabel">Patient Name</span>
  <span property="schema:name doco-fd:fieldValue">John Doe</span>
</div>
```

```
Visual representation:
┌─────────────────────────────────────────────────────┐
│ typeof="schema:Person doco-fd:FormField"            │ ← Standard RDF
│ resource="#patient"                                 │ ← Graph node
│  ┌────────────────────────────────────────────────┐ │
│  │ property="doco-fd:fieldLabel"                  │ │ ← RDF predicate
│  │ Patient Name                                   │ │
│  └────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │ property="schema:name doco-fd:fieldValue"      │ │ ← Dual properties
│  │ John Doe                                       │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘

Benefits:
✅ Standard RDF/OWL
✅ Semantic web compatible
✅ Can reason and infer
✅ Interoperable globally
```

### Before & After: Table

#### Before (data-* attributes)
```html
<table data-section="products">
  <tr>
    <th data-role="column-header">Product</th>
    <th data-role="column-header">Price</th>
  </tr>
  <tr>
    <td data-label="Product">Widget A</td>
    <td data-label="Price" data-entity-type="AMOUNT">$25.00</td>
  </tr>
</table>
```

```
Table structure:
┏━━━━━━━━━┳━━━━━━━━┓
┃ Product ┃ Price  ┃
┣━━━━━━━━━╋━━━━━━━━┫
┃ Widget A┃ $25.00 ┃
┗━━━━━━━━━┻━━━━━━━━┛

RDF Graph: ❌ Cannot be extracted!
(data-* attributes don't create triples)
```

#### After (DoCO-FD + RDFa)
```html
<table typeof="doco:Table" resource="#products">
  <thead>
    <tr typeof="doco-fd:TableRow">
      <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Product</th>
      <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Price</th>
    </tr>
  </thead>
  <tbody>
    <tr typeof="doco-fd:TableRow" resource="#row1">
      <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget A</td>
      <td typeof="doco-fd:TableCell schema:MonetaryAmount"
          property="doco-fd:cellValue schema:value">$25.00</td>
    </tr>
  </tbody>
</table>
```

```
Table structure:
┏━━━━━━━━━┳━━━━━━━━┓
┃ Product ┃ Price  ┃  ← TableHeader × 2
┣━━━━━━━━━╋━━━━━━━━┫
┃ Widget A┃ $25.00 ┃  ← TableCell × 2
┗━━━━━━━━━┻━━━━━━━━┛
      ▲         ▲
      │         └─ Typed as schema:MonetaryAmount
      └─ All in TableRow (#row1)

RDF Graph: ✅ Complete structure!
#products → hasRow → #row1 → hasCell → [cells with values]
```

---

## Namespace Quick Reference

### Namespace Prefixes

```
┌─────────────┬─────────────────────────────────────────────────┐
│   Prefix    │              Namespace URI                      │
├─────────────┼─────────────────────────────────────────────────┤
│ schema      │ http://schema.org/                              │
│ doco        │ http://purl.org/spar/doco/                      │
│ doco-fd     │ http://purl.org/doco-fd/                        │
│ foaf        │ http://xmlns.com/foaf/0.1/                      │
│ dc          │ http://purl.org/dc/terms/                       │
│ rdf         │ http://www.w3.org/1999/02/22-rdf-syntax-ns#     │
│ rdfs        │ http://www.w3.org/2000/01/rdf-schema#           │
│ xsd         │ http://www.w3.org/2001/XMLSchema#               │
│ owl         │ http://www.w3.org/2002/07/owl#                  │
└─────────────┴─────────────────────────────────────────────────┘
```

### When to Use Which Vocabulary

```
┌──────────────────────┬─────────────┬──────────────────────┐
│      Use Case        │  Vocabulary │      Example         │
├──────────────────────┼─────────────┼──────────────────────┤
│ Document structure   │ doco        │ Section, Paragraph   │
│ Form components      │ doco-fd     │ FormField, TableCell │
│ Semantic entities    │ schema      │ Person, Organization │
│ People/groups        │ foaf        │ name, Organization   │
│ Metadata             │ dc          │ title, date, creator │
│ Data types           │ xsd         │ string, integer      │
└──────────────────────┴─────────────┴──────────────────────┘
```

---

## Complete Example Diagram

### Invoice with All Annotations

```
┌──────────────────────────────────────────────────────────────────┐
│ <html xmlns:schema="..." xmlns:doco="..." xmlns:doco-fd="...">  │
└──────────────────────────────────────────────────────────────────┘
        │
        └──> <body typeof="schema:Invoice doco:BodyMatter">
                   │
                   ├──> <header typeof="doco-fd:Header">
                   │         │
                   │         ├──> <h1 property="doco:title">
                   │         │      Invoice
                   │         │
                   │         └──> <div typeof="doco-fd:FormField">
                   │                   <span property="doco-fd:fieldLabel">
                   │                     Invoice #
                   │                   <span property="doco-fd:fieldValue">
                   │                     INV-001
                   │
                   ├──> <section typeof="doco-fd:FormSection">
                   │         │
                   │         └──> <div typeof="schema:Person doco-fd:FormField">
                   │                   <span property="doco-fd:fieldLabel">
                   │                     Customer
                   │                   <span property="schema:name doco-fd:fieldValue">
                   │                     John Smith
                   │
                   ├──> <table typeof="doco:Table">
                   │         │
                   │         ├──> <tr typeof="doco-fd:TableRow">
                   │         │       └──> <th typeof="doco-fd:TableHeader"
                   │         │               property="doco-fd:columnHeader">
                   │         │              Product
                   │         │
                   │         └──> <tr typeof="doco-fd:TableRow">
                   │                 └──> <td typeof="doco-fd:TableCell"
                   │                         property="doco-fd:cellValue">
                   │                        Widget A
                   │
                   └──> <footer typeof="doco-fd:Footer">
                             <p property="doco:footnote">
                               Payment due in 30 days
```

---

## Summary: Key Takeaways

### The Three-Second Guide

```
┌────────────────────────────────────────────────────────┐
│  1. Use DoCO-FD for STRUCTURE (how it's organized)    │
│     → FormField, TableCell, Header, Footer            │
│                                                         │
│  2. Use Schema.org for SEMANTICS (what it means)       │
│     → Person, Organization, MonetaryAmount            │
│                                                         │
│  3. Combine them with "typeof" and "property"          │
│     → typeof="schema:Person doco-fd:FormField"        │
│     → property="schema:name doco-fd:fieldValue"       │
└────────────────────────────────────────────────────────┘
```

### What DoCO-FD Gives You

```
Before DoCO-FD:                After DoCO-FD:
═══════════════                ══════════════

❌ No table cells              ✅ TableRow, TableCell
❌ No form fields              ✅ FormField, FormSection
❌ No key-value pairs          ✅ KeyValuePair
❌ Generic "textbox"           ✅ Specific field types
❌ No field properties         ✅ fieldLabel, fieldValue
❌ Custom data-* attrs         ✅ Standard RDF properties

Result: Cannot extract        Result: Full RDF graph
        structured data               extraction!
```

### Decision Tree: Which Class to Use?

```
                    Is it a form-based document?
                              │
                 ┌────────────┴────────────┐
                Yes                        No
                 │                          │
                 ▼                          ▼
         Use DoCO-FD!                  Use plain DoCO
                 │
      ┌──────────┴──────────┐
      │                     │
   Is it a              Is it a
   field?              table?
      │                     │
      ▼                     ▼
   FormField          TableRow
   fieldLabel         TableCell
   fieldValue         cellValue
                      columnHeader
```

---

## Complete Template Pipeline Example

### From Template to Training Data

This section shows the complete flow of how DoCO and DoCO-FD work together in the synthetic document generation pipeline.

```
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 1: Template Definition                    │
└─────────────────────────────────────────────────────────────────┘

Template File Structure:
invoice_template/
├── template.html    ← DoCO-FD markup + Jinja2 variables
├── styles.css       ← Visual styling
├── script.js        ← Dynamic behavior
├── template.py      ← Data generator
└── config.yaml      ← Metadata

┌─────────────────────────────────────────────────────────────────┐
│                  STEP 2: HTML with RDFa Markup                  │
└─────────────────────────────────────────────────────────────────┘

<html xmlns:schema="http://schema.org/"
      xmlns:doco="http://purl.org/spar/doco/"
      xmlns:doco-fd="http://purl.org/doco-fd/">

<body typeof="schema:Invoice doco:BodyMatter" resource="#invoice">

  <!-- Header Section -->
  <header typeof="doco-fd:Header" resource="#header">
    <h1 property="doco:title">Invoice</h1>

    <div typeof="doco-fd:FormField" resource="#invoiceNum">
      <span property="doco-fd:fieldLabel">Invoice #:</span>
      <span property="schema:identifier doco-fd:fieldValue">
        {{ invoice_number }}
      </span>
    </div>
  </header>

  <!-- Customer Section -->
  <section typeof="doco-fd:FormSection" resource="#customerInfo">
    <h2 property="doco:sectionTitle">Customer Information</h2>

    <div typeof="schema:Person doco-fd:FormField" resource="#customer">
      <span property="doco-fd:fieldLabel">Customer Name:</span>
      <span property="schema:name doco-fd:fieldValue">
        {{ customer_name }}
      </span>
    </div>
  </section>

  <!-- Table Section -->
  <table typeof="doco:Table" resource="#items">
    <tr typeof="doco-fd:TableRow">
      <th typeof="doco-fd:TableHeader"
          property="doco-fd:columnHeader">Product</th>
      <th typeof="doco-fd:TableHeader"
          property="doco-fd:columnHeader">Price</th>
    </tr>
    {% for item in items %}
    <tr typeof="doco-fd:TableRow" resource="#item{{ loop.index }}">
      <td typeof="doco-fd:TableCell"
          property="doco-fd:cellValue">{{ item.name }}</td>
      <td typeof="doco-fd:TableCell schema:MonetaryAmount"
          property="doco-fd:cellValue schema:value">
        {{ item.price }}
      </td>
    </tr>
    {% endfor %}
  </table>

</body>
</html>

┌─────────────────────────────────────────────────────────────────┐
│              STEP 3: Data Generation (template.py)              │
└─────────────────────────────────────────────────────────────────┘

def generate_sample():
    return {
        'invoice_number': 'INV-2026-001',
        'customer_name': 'John Smith',
        'items': [
            {'name': 'Widget A', 'price': '$25.00'},
            {'name': 'Widget B', 'price': '$45.00'}
        ]
    }

┌─────────────────────────────────────────────────────────────────┐
│           STEP 4: Rendered HTML (Jinja2 + Data)                │
└─────────────────────────────────────────────────────────────────┘

<html xmlns:schema="http://schema.org/"
      xmlns:doco="http://purl.org/spar/doco/"
      xmlns:doco-fd="http://purl.org/doco-fd/">

<body typeof="schema:Invoice doco:BodyMatter" resource="#invoice">

  <header typeof="doco-fd:Header" resource="#header">
    <h1 property="doco:title">Invoice</h1>

    <div typeof="doco-fd:FormField" resource="#invoiceNum">
      <span property="doco-fd:fieldLabel">Invoice #:</span>
      <span property="schema:identifier doco-fd:fieldValue">INV-2026-001</span>
    </div>
  </header>

  <section typeof="doco-fd:FormSection" resource="#customerInfo">
    <h2 property="doco:sectionTitle">Customer Information</h2>

    <div typeof="schema:Person doco-fd:FormField" resource="#customer">
      <span property="doco-fd:fieldLabel">Customer Name:</span>
      <span property="schema:name doco-fd:fieldValue">John Smith</span>
    </div>
  </section>

  <table typeof="doco:Table" resource="#items">
    <tr typeof="doco-fd:TableRow">
      <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Product</th>
      <th typeof="doco-fd:TableHeader" property="doco-fd:columnHeader">Price</th>
    </tr>
    <tr typeof="doco-fd:TableRow" resource="#item1">
      <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget A</td>
      <td typeof="doco-fd:TableCell schema:MonetaryAmount"
          property="doco-fd:cellValue schema:value">$25.00</td>
    </tr>
    <tr typeof="doco-fd:TableRow" resource="#item2">
      <td typeof="doco-fd:TableCell" property="doco-fd:cellValue">Widget B</td>
      <td typeof="doco-fd:TableCell schema:MonetaryAmount"
          property="doco-fd:cellValue schema:value">$45.00</td>
    </tr>
  </table>

</body>
</html>

┌─────────────────────────────────────────────────────────────────┐
│         STEP 5: PagedJS Rendering (PDF + Bounding Boxes)       │
└─────────────────────────────────────────────────────────────────┘

Visual Output (PDF):
┌───────────────────────────────────────┐
│  Invoice                              │ ← <h1>
│                                        │
│  Invoice #: INV-2026-001              │ ← FormField
│                                        │
│  Customer Information                 │ ← Section Title
│  Customer Name: John Smith            │ ← FormField
│                                        │
│  ┌──────────┬──────────┐              │
│  │ Product  │  Price   │              │ ← TableHeader × 2
│  ├──────────┼──────────┤              │
│  │ Widget A │ $25.00   │              │ ← TableCell × 2
│  ├──────────┼──────────┤              │
│  │ Widget B │ $45.00   │              │ ← TableCell × 2
│  └──────────┴──────────┘              │
└───────────────────────────────────────┘

Bounding Boxes Extracted:
[
  {
    "text": "Invoice #:",
    "bbox": [50, 100, 120, 115],
    "entity_type": "FIELD_LABEL",
    "property": "doco-fd:fieldLabel"
  },
  {
    "text": "INV-2026-001",
    "bbox": [125, 100, 220, 115],
    "entity_type": "IDENTIFIER",
    "property": "schema:identifier, doco-fd:fieldValue"
  },
  {
    "text": "John Smith",
    "bbox": [200, 150, 300, 165],
    "entity_type": "PERSON",
    "property": "schema:name, doco-fd:fieldValue"
  },
  {
    "text": "Widget A",
    "bbox": [50, 230, 150, 250],  ← FULL CELL BBOX
    "entity_type": "TABLE_CELL",
    "property": "doco-fd:cellValue"
  },
  {
    "text": "$25.00",
    "bbox": [160, 230, 260, 250],  ← FULL CELL BBOX
    "entity_type": "MONEY",
    "property": "doco-fd:cellValue, schema:value"
  }
]

┌─────────────────────────────────────────────────────────────────┐
│          STEP 6: RDF Graph Extraction (extract_field_          │
│                    relationships.py)                            │
└─────────────────────────────────────────────────────────────────┘

RDF Triples (Turtle Format):

@prefix schema: <http://schema.org/> .
@prefix doco: <http://purl.org/spar/doco/> .
@prefix doco-fd: <http://purl.org/doco-fd/> .

<#invoice> a schema:Invoice, doco:BodyMatter ;
    doco-fd:hasHeader <#header> ;
    doco-fd:hasSection <#customerInfo> .

<#header> a doco-fd:Header ;
    doco:title "Invoice" ;
    doco-fd:hasField <#invoiceNum> .

<#invoiceNum> a doco-fd:FormField ;
    doco-fd:fieldLabel "Invoice #:" ;
    schema:identifier "INV-2026-001" ;
    doco-fd:fieldValue "INV-2026-001" .

<#customerInfo> a doco-fd:FormSection ;
    doco:sectionTitle "Customer Information" ;
    doco-fd:hasField <#customer> .

<#customer> a schema:Person, doco-fd:FormField ;
    doco-fd:fieldLabel "Customer Name:" ;
    schema:name "John Smith" ;
    doco-fd:fieldValue "John Smith" .

<#items> a doco:Table ;
    doco-fd:hasRow <#item1>, <#item2> .

<#item1> a doco-fd:TableRow ;
    doco-fd:hasCell _:cell1, _:cell2 .

_:cell1 a doco-fd:TableCell ;
    doco-fd:cellValue "Widget A" .

_:cell2 a doco-fd:TableCell, schema:MonetaryAmount ;
    doco-fd:cellValue "$25.00" ;
    schema:value "$25.00" .

┌─────────────────────────────────────────────────────────────────┐
│        STEP 7: Training Data Output (NER Dataset Format)       │
└─────────────────────────────────────────────────────────────────┘

{
  "document_id": "invoice_001",
  "pages": [
    {
      "page_number": 1,
      "image_path": "invoice_001_page_1.png",
      "width": 612,
      "height": 792,
      "annotations": [
        {
          "text": "Invoice #:",
          "bbox": [50, 100, 120, 115],
          "label": "FIELD_LABEL",
          "entity_type": "FIELD_LABEL",
          "properties": {
            "doco-fd:fieldLabel": true
          }
        },
        {
          "text": "INV-2026-001",
          "bbox": [125, 100, 220, 115],
          "label": "IDENTIFIER",
          "entity_type": "IDENTIFIER",
          "properties": {
            "schema:identifier": true,
            "doco-fd:fieldValue": true
          },
          "parent_field": "invoiceNum"
        },
        {
          "text": "John Smith",
          "bbox": [200, 150, 300, 165],
          "label": "PERSON",
          "entity_type": "PERSON",
          "properties": {
            "schema:name": true,
            "doco-fd:fieldValue": true
          },
          "parent_field": "customer",
          "parent_section": "customerInfo"
        },
        {
          "text": "Widget A",
          "bbox": [50, 230, 150, 250],
          "label": "TABLE_CELL",
          "entity_type": "TABLE_CELL",
          "properties": {
            "doco-fd:cellValue": true
          },
          "parent_table": "items",
          "parent_row": "item1"
        }
      ]
    }
  ]
}
```

---

## How DoCO and DoCO-FD Work Together

### Role Division

```
┌─────────────────────────────────────────────────────────────────┐
│                         Your Template                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Uses both ontologies
                              ▼
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────────┐                    ┌────────────────────┐
│      DoCO        │                    │     DoCO-FD        │
│   (Official)     │                    │  (Our Extension)   │
└──────────────────┘                    └────────────────────┘
        │                                           │
        │ Provides:                                 │ Provides:
        │                                           │
        ├─ Section                                  ├─ FormSection
        ├─ Paragraph                                ├─ FormField
        ├─ Table                                    ├─ KeyValuePair
        ├─ Title                                    ├─ TableRow
        ├─ Label                                    ├─ TableCell
        ├─ TextBox                                  ├─ TableHeader
        ├─ FrontMatter                              ├─ Header
        ├─ BackMatter                               ├─ Footer
        ├─ BodyMatter                               ├─ fieldLabel
        │                                           ├─ fieldValue
        │                                           ├─ cellValue
        │                                           ├─ columnHeader
        │                                           └─ rowHeader
        │
        └─────────────────┬───────────────────────────┘
                          │
                          │ Combined in markup
                          ▼
              <div typeof="doco-fd:FormSection">
                      └─── Uses DoCO-FD

              <table typeof="doco:Table">
                      └─── Uses official DoCO

              <tr typeof="doco-fd:TableRow">
                      └─── Uses DoCO-FD (fills gap!)
```

### Practical Usage Pattern

```
PATTERN 1: Document-Level Structure (Use DoCO)
═══════════════════════════════════════════════

<body typeof="doco:BodyMatter">          ← DoCO class
  <section typeof="doco-fd:FormSection">  ← Extends doco:Section
    ...
  </section>
</body>


PATTERN 2: Form Fields (Use DoCO-FD)
════════════════════════════════════

<div typeof="doco-fd:FormField">         ← DoCO-FD class
  <span property="doco-fd:fieldLabel">   ← DoCO-FD property
    Customer Name:
  </span>
  <span property="doco-fd:fieldValue">   ← DoCO-FD property
    John Smith
  </span>
</div>


PATTERN 3: Tables (Use DoCO + DoCO-FD)
═══════════════════════════════════════

<table typeof="doco:Table">              ← DoCO class
  <tr typeof="doco-fd:TableRow">         ← DoCO-FD class (NEW!)
    <th typeof="doco-fd:TableHeader"     ← DoCO-FD class (NEW!)
        property="doco-fd:columnHeader"> ← DoCO-FD property (NEW!)
      Product
    </th>
  </tr>
  <tr typeof="doco-fd:TableRow">         ← DoCO-FD class
    <td typeof="doco-fd:TableCell"       ← DoCO-FD class (NEW!)
        property="doco-fd:cellValue">    ← DoCO-FD property (NEW!)
      Widget A
    </td>
  </tr>
</table>


PATTERN 4: Dual-Layer Semantic Markup
══════════════════════════════════════

<div typeof="schema:Person doco-fd:FormField" resource="#customer">
           └─Semantic    └─Structural

  <span property="schema:name doco-fd:fieldValue">John Smith</span>
               └─Semantic    └─Structural

This creates TWO sets of triples:
1. Structural: #customer doco-fd:fieldValue "John Smith"
2. Semantic:   #customer schema:name "John Smith"
```

### The Complete Information Flow

```
Template.html (RDFa)
        │
        │ 1. Jinja2 renders with data
        ▼
Rendered HTML (RDFa)
        │
        │ 2. PagedJS converts to PDF
        ├────────┬────────────┐
        │        │            │
        ▼        ▼            ▼
       PDF   Bounding    Screenshots
              Boxes
        │        │            │
        │        │            │
        │        │ 3. RDFLib parses RDFa
        │        ▼            │
        │    RDF Graph        │
        │    (Triples)        │
        │        │            │
        │        │ 4. Combine │
        └────────┴────────────┘
                 │
                 ▼
         Training Dataset
         {
           "text": "...",
           "bbox": [...],
           "label": "PERSON",
           "properties": {
             "schema:name": true,
             "doco-fd:fieldValue": true
           }
         }
                 │
                 ▼
         NER Model Training
```

---

## Real-World Example: Medical Record Template

Let's see a complete example with a medical record:

### Template Structure

```
medical_record_template/
├── template.html        # The markup (shown below)
├── styles.css          # Medical form styling
├── script.js           # Form validation
├── template.py         # Patient data generator
└── config.yaml         # Template metadata
```

### template.html (Annotated)

```html
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:schema="http://schema.org/"
      xmlns:doco="http://purl.org/spar/doco/"
      xmlns:doco-fd="http://purl.org/doco-fd/">
<head>
  <title>Medical Record</title>
  <link rel="stylesheet" href="styles.css">
</head>

<body typeof="schema:MedicalRecord doco:BodyMatter" resource="#record">

  <!-- HEADER: Use DoCO-FD -->
  <header typeof="doco-fd:Header" resource="#header">
    <h1 property="doco:title">Patient Medical Record</h1>

    <div typeof="doco-fd:FormField" resource="#recordId">
      <span property="doco-fd:fieldLabel">Record ID:</span>
      <span property="schema:identifier doco-fd:fieldValue">
        {{ record_id }}
      </span>
    </div>

    <div typeof="doco-fd:FormField" resource="#recordDate">
      <span property="doco-fd:fieldLabel">Date:</span>
      <span property="schema:dateCreated doco-fd:fieldValue">
        {{ date }}
      </span>
    </div>
  </header>

  <!-- PATIENT INFO SECTION: Use DoCO-FD FormSection -->
  <section typeof="doco-fd:FormSection" resource="#patientInfo">
    <h2 property="doco:sectionTitle">Patient Information</h2>

    <!-- Patient Name: Dual-layer markup -->
    <div typeof="schema:Patient doco-fd:FormField" resource="#patient">
      <span property="doco-fd:fieldLabel">Patient Name:</span>
      <span property="schema:name doco-fd:fieldValue">
        {{ patient_name }}
      </span>
    </div>

    <!-- Date of Birth -->
    <div typeof="doco-fd:FormField" resource="#dob">
      <span property="doco-fd:fieldLabel">Date of Birth:</span>
      <span property="schema:birthDate doco-fd:fieldValue">
        {{ date_of_birth }}
      </span>
    </div>

    <!-- Address -->
    <div typeof="schema:PostalAddress doco-fd:FormField" resource="#address">
      <span property="doco-fd:fieldLabel">Address:</span>
      <span property="schema:streetAddress doco-fd:fieldValue">
        {{ address }}
      </span>
    </div>
  </section>

  <!-- VITALS SECTION: Use DoCO Table + DoCO-FD internals -->
  <section typeof="doco-fd:FormSection" resource="#vitals">
    <h2 property="doco:sectionTitle">Vital Signs</h2>

    <table typeof="doco:Table" resource="#vitalsTable">
      <caption property="doco:caption">Patient Vitals</caption>

      <!-- Header Row: DoCO-FD TableRow + TableHeader -->
      <thead>
        <tr typeof="doco-fd:TableRow" resource="#vitalsHeader">
          <th typeof="doco-fd:TableHeader"
              property="doco-fd:columnHeader">Measurement</th>
          <th typeof="doco-fd:TableHeader"
              property="doco-fd:columnHeader">Value</th>
          <th typeof="doco-fd:TableHeader"
              property="doco-fd:columnHeader">Unit</th>
        </tr>
      </thead>

      <!-- Data Rows: DoCO-FD TableRow + TableCell -->
      <tbody>
        {% for vital in vitals %}
        <tr typeof="doco-fd:TableRow" resource="#vital{{ loop.index }}">
          <td typeof="doco-fd:TableCell"
              property="doco-fd:cellValue">{{ vital.measurement }}</td>
          <td typeof="doco-fd:TableCell schema:QuantitativeValue"
              property="doco-fd:cellValue schema:value">{{ vital.value }}</td>
          <td typeof="doco-fd:TableCell"
              property="doco-fd:cellValue">{{ vital.unit }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>

  <!-- FOOTER: Use DoCO-FD -->
  <footer typeof="doco-fd:Footer" resource="#footer">
    <p property="doco:footnote">
      This is a confidential medical record.
      For authorized personnel only.
    </p>
  </footer>

</body>
</html>
```

### What Gets Generated

```
┌──────────────────────────────────────────────────────────┐
│                  Patient Medical Record                  │
│                                                          │
│  Record ID: MR-2026-12345                               │
│  Date: January 13, 2026                                 │
├──────────────────────────────────────────────────────────┤
│  Patient Information                                     │
│                                                          │
│  Patient Name: Sarah Johnson                            │
│  Date of Birth: March 15, 1985                          │
│  Address: 456 Oak Avenue, Springfield, IL 62701         │
├──────────────────────────────────────────────────────────┤
│  Vital Signs                                             │
│                                                          │
│  ┌──────────────┬────────┬──────────────┐              │
│  │ Measurement  │ Value  │ Unit         │              │
│  ├──────────────┼────────┼──────────────┤              │
│  │ Blood Press. │ 120/80 │ mmHg         │              │
│  │ Heart Rate   │ 72     │ bpm          │              │
│  │ Temperature  │ 98.6   │ °F           │              │
│  │ Weight       │ 145    │ lbs          │              │
│  └──────────────┴────────┴──────────────┘              │
├──────────────────────────────────────────────────────────┤
│  This is a confidential medical record.                 │
│  For authorized personnel only.                          │
└──────────────────────────────────────────────────────────┘
```

### RDF Graph Output

```turtle
@prefix schema: <http://schema.org/> .
@prefix doco: <http://purl.org/spar/doco/> .
@prefix doco-fd: <http://purl.org/doco-fd/> .

# Document root
<#record> a schema:MedicalRecord, doco:BodyMatter ;
    doco-fd:hasHeader <#header> ;
    doco-fd:hasSection <#patientInfo>, <#vitals> ;
    doco-fd:hasFooter <#footer> .

# Header
<#header> a doco-fd:Header ;
    doco:title "Patient Medical Record" ;
    doco-fd:hasField <#recordId>, <#recordDate> .

<#recordId> a doco-fd:FormField ;
    doco-fd:fieldLabel "Record ID:" ;
    schema:identifier "MR-2026-12345" ;
    doco-fd:fieldValue "MR-2026-12345" .

# Patient Info Section
<#patientInfo> a doco-fd:FormSection ;
    doco:sectionTitle "Patient Information" ;
    doco-fd:hasField <#patient>, <#dob>, <#address> .

<#patient> a schema:Patient, doco-fd:FormField ;
    doco-fd:fieldLabel "Patient Name:" ;
    schema:name "Sarah Johnson" ;
    doco-fd:fieldValue "Sarah Johnson" .

<#dob> a doco-fd:FormField ;
    doco-fd:fieldLabel "Date of Birth:" ;
    schema:birthDate "March 15, 1985" ;
    doco-fd:fieldValue "March 15, 1985" .

# Vitals Table
<#vitalsTable> a doco:Table ;
    doco:caption "Patient Vitals" ;
    doco-fd:hasRow <#vital1>, <#vital2>, <#vital3>, <#vital4> .

<#vital1> a doco-fd:TableRow ;
    doco-fd:hasCell _:cell1_1, _:cell1_2, _:cell1_3 .

_:cell1_1 a doco-fd:TableCell ;
    doco-fd:cellValue "Blood Pressure" .

_:cell1_2 a doco-fd:TableCell, schema:QuantitativeValue ;
    doco-fd:cellValue "120/80" ;
    schema:value "120/80" .

_:cell1_3 a doco-fd:TableCell ;
    doco-fd:cellValue "mmHg" .

# Footer
<#footer> a doco-fd:Footer ;
    doco:footnote "This is a confidential medical record. For authorized personnel only." .
```

### Training Data Output

```json
{
  "document_id": "medical_record_001",
  "document_type": "schema:MedicalRecord",
  "pages": [
    {
      "page_number": 1,
      "image_path": "medical_record_001_page_1.png",
      "width": 612,
      "height": 792,
      "annotations": [
        {
          "id": "ann_1",
          "text": "Sarah Johnson",
          "bbox": [200, 180, 320, 195],
          "label": "PERSON",
          "entity_type": "PATIENT",
          "properties": {
            "schema:name": true,
            "doco-fd:fieldValue": true
          },
          "parent_field": "patient",
          "parent_section": "patientInfo",
          "rdf_types": ["schema:Patient", "doco-fd:FormField"]
        },
        {
          "id": "ann_2",
          "text": "March 15, 1985",
          "bbox": [210, 210, 320, 225],
          "label": "DATE",
          "entity_type": "DATE_OF_BIRTH",
          "properties": {
            "schema:birthDate": true,
            "doco-fd:fieldValue": true
          },
          "parent_field": "dob",
          "parent_section": "patientInfo"
        },
        {
          "id": "ann_3",
          "text": "120/80",
          "bbox": [160, 320, 220, 340],
          "label": "MEASUREMENT",
          "entity_type": "VITAL_SIGN",
          "properties": {
            "doco-fd:cellValue": true,
            "schema:value": true
          },
          "parent_row": "vital1",
          "parent_table": "vitalsTable",
          "rdf_types": ["doco-fd:TableCell", "schema:QuantitativeValue"]
        }
      ]
    }
  ],
  "rdf_graph": "graph.ttl"
}
```

---

## Summary: The Complete Picture

```
┌─────────────────────────────────────────────────────────────┐
│  1. Write template.html with DoCO + DoCO-FD markup         │
│     • Use doco:Table for tables                            │
│     • Use doco-fd:TableRow, TableCell for internals        │
│     • Use doco-fd:FormField for form fields                │
│     • Add schema.org types for semantics                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Generate data with template.py                          │
│     • Create realistic synthetic data                       │
│     • Fill Jinja2 variables                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Render with PagedJS                                     │
│     • Creates PDF                                           │
│     • Extracts bounding boxes (with FULL cell boxes!)       │
│     • Takes screenshots                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Parse RDFa with RDFLib                                  │
│     • Extracts RDF triples                                  │
│     • Creates knowledge graph                               │
│     • Exports to Turtle/N3/JSON-LD                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Combine into training dataset                           │
│     • Text + Bounding boxes                                 │
│     • Entity labels from properties                         │
│     • Hierarchical relationships                            │
│     • Ready for NER model training                          │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight:** DoCO provides the foundation for document structure, while DoCO-FD extends it with form-specific components. Together they enable full semantic markup that can be automatically converted into high-quality training data for machine learning models.

---

**End of Visual Guide**

For more information:
- [DoCO-FD README](README.md)
- [Examples](examples/)
- [Official DoCO](http://purl.org/spar/doco)
