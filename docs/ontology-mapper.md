# Ontology-Based Type Mapper

## Overview

The ontology mapper dynamically loads and uses RDF ontologies (Schema.org, DOCO) to map RDFa types and properties to entity types, replacing hard-coded mappings with flexible, extensible ontology-based inference.

## Benefits

### ✅ Before (Hard-coded)
```javascript
// pagedjs_renderer.py had hard-coded mappings:
const typeMap = {
    'Person': 'PERSON',
    'Organization': 'ORG',
    // ... 10+ more hard-coded entries
};
```

**Problems:**
- Brittle and unmaintainable
- Doesn't leverage ontology semantics
- Requires code changes to add new types
- Doesn't understand type hierarchies

### ✅ After (Ontology-based)
```python
# Automatically loads Schema.org and DOCO ontologies
mapper = get_ontology_mapper()
entity_type = mapper.map_type_to_entity("Person", "schema")  # Returns "PERSON"
entity_type = mapper.map_type_to_entity("EducationalOrganization", "schema")  # Returns "ORG" (via subclass inference)
```

**Benefits:**
- Uses actual ontology definitions
- Understands type hierarchies (subclass relationships)
- Caches ontologies locally for performance
- Extensible without code changes
- Falls back to defaults if ontologies unavailable

## Usage

### Basic Usage

```python
from synthdoc.ontology_mapper import get_ontology_mapper

# Get singleton instance
mapper = get_ontology_mapper()

# Map Schema.org types to entity types
entity_type = mapper.map_type_to_entity("Person", "schema")
# Returns: "PERSON"

entity_type = mapper.map_type_to_entity("PostalAddress", "schema")
# Returns: "ADDRESS"

# Map properties to entity types
entity_type = mapper.map_property_to_entity("birthDate", "schema")
# Returns: "DATE"

# Map DOCO structural properties
entity_type = mapper.map_property_to_entity("fieldLabel", "doco-fd")
# Returns: "FIELD_LABEL"
```

### Loading Ontologies

Ontologies are loaded automatically on first use, but you can force loading:

```python
# Load Schema.org ontology
mapper.load_schema_org(force_reload=True)

# Load DOCO ontology
mapper.load_doco(force_reload=True)
```

Ontologies are cached in `synthdoc/ontology_cache/` for fast subsequent loads.

### JavaScript Integration

The mapper generates JavaScript configuration for browser-based extraction:

```python
# Generate JavaScript code with mappings
js_config = mapper.generate_javascript_config()

# This creates:
# - ONTOLOGY_CONFIG object with type/property mappings
# - getSchemaType(el) function
# - getPropertyName(el) function  
# - inferEntityTypeFromProperty(name) function
# - mapStructuralProperty(attr) function
```

This is injected into Playwright page evaluation in `pagedjs_renderer.py`.

## Architecture

```
┌─────────────────────────────────────────┐
│ OntologyMapper (Python)                 │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Schema.org RDF Graph              │ │
│  │ - Type hierarchy (subClassOf)     │ │
│  │ - Property ranges                 │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ DOCO RDF Graph                    │ │
│  │ - Document structure vocabulary   │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Mapping Caches                    │ │
│  │ - Type → Entity mappings          │ │
│  │ - Property → Entity mappings      │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
                  │
                  │ generates
                  ▼
    ┌──────────────────────────────┐
    │ JavaScript Config            │
    │ - ONTOLOGY_CONFIG object     │
    │ - Helper functions           │
    └──────────────────────────────┘
                  │
                  │ injected into
                  ▼
    ┌──────────────────────────────┐
    │ Playwright Page              │
    │ - RDFa extraction            │
    │ - Type inference             │
    └──────────────────────────────┘
```

## Extending Mappings

### Adding New Schema.org Types

Since the system uses ontology inference, new Schema.org types often work automatically via subclass relationships:

```python
# If EducationalOrganization is a subclass of Organization,
# it will automatically map to 'ORG' without code changes

entity_type = mapper.map_type_to_entity("EducationalOrganization", "schema")
# Returns: "ORG" (via subclass inference)
```

### Adding Custom Type Mappings

If you need to override or add mappings:

```python
mapper = get_ontology_mapper()

# Add custom type mapping
mapper._default_type_map['MedicalEntity'] = 'MEDICAL'

# Add custom property mapping  
mapper._default_property_map['diagnosisDate'] = 'DATE'

# Clear cache to force remapping
mapper._type_to_entity_cache.clear()
mapper._property_to_entity_cache.clear()
```

### Adding New Structural Properties

For DOCO/DOCO-FD structural elements:

```python
mapper._structural_properties['customField'] = 'CUSTOM_FIELD'
```

## Ontology Caching

Ontologies are cached in `synthdoc/ontology_cache/`:
- `schema_org.ttl` - Schema.org ontology (Turtle format)
- `doco.ttl` - DOCO ontology (Turtle format)

To force re-download:
```python
mapper.load_schema_org(force_reload=True)
mapper.load_doco(force_reload=True)
```

Or delete cache files:
```bash
rm -rf synthdoc/ontology_cache/*.ttl
```

## Performance

- **First load**: Downloads ontologies (~5-10 seconds)
- **Subsequent loads**: Reads from cache (~100ms)
- **Type mapping**: O(1) lookup from cache
- **Subclass inference**: O(n) where n = depth of hierarchy (max 3 levels)

## Fallback Behavior

If ontologies fail to load:
1. System logs warning
2. Falls back to default hard-coded mappings
3. Extraction continues normally

This ensures robustness even without internet connectivity.

## Testing

```python
from synthdoc.ontology_mapper import OntologyMapper

# Create test instance with custom cache
mapper = OntologyMapper(cache_dir=Path("test_cache"))

# Test Schema.org mapping
assert mapper.map_type_to_entity("Person", "schema") == "PERSON"
assert mapper.map_type_to_entity("Organization", "schema") == "ORG"

# Test property mapping
assert mapper.map_property_to_entity("birthDate", "schema") == "DATE"
assert mapper.map_property_to_entity("email", "schema") == "EMAIL"

# Test structural mapping
assert mapper.map_property_to_entity("fieldLabel", "doco-fd") == "FIELD_LABEL"
```

## Migration from Hard-coded Mappings

The existing hard-coded mappings in `pagedjs_renderer.py` have been:
1. **Extracted** to `ontology_mapper.py` as default fallbacks
2. **Enhanced** with ontology-based inference
3. **Made extensible** without code changes

No changes needed to templates or existing data - the API is backward compatible.

## Future Enhancements

Potential improvements:
- Support for custom domain ontologies
- SPARQL queries for complex type inference
- Automatic entity type discovery from ontology
- Integration with external knowledge graphs
- Web UI for managing type mappings

## References

- [Schema.org](https://schema.org/) - Vocabulary for structured data
- [DOCO Ontology](http://purl.org/spar/doco/) - Document Components Ontology
- [RDFLib Documentation](https://rdflib.readthedocs.io/) - Python RDF library
- [RDFa Primer](https://www.w3.org/TR/rdfa-primer/) - RDFa specification
