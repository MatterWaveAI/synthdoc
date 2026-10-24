# Integrated Document Generator System Documentation

## Overview
The document generator system has been refactored to integrate all previously disconnected components into a cohesive system. The system now primarily uses the template system as the main document generation approach while maintaining backward compatibility.

## Architecture

### Core Components
1. **Unified Document Generator** (`services/unified_generator.py`)
   - Primary generator that uses the advanced template system
   - Maintains backward compatibility with legacy generators
   - Provides access to all advanced features

2. **NER Data Generator** (`ner_data_generator.py`)
   - Generates NER training datasets with pixel-perfect ground truth coordinates
   - Extracts bounding boxes using Playwright and JavaScript DOM access
   - Creates JSON annotation files for NER model training

3. **Template System** (`templates/`)
   - Configurable document templates with styling options
   - Registry for managing different templates
   - Configuration manager for styling variations
   - Scalable document templates for handling documents with many paragraphs/sections

4. **API Interface** (`api/main.py`)
   - Web API endpoints for all document generation features
   - CRUD operations for documents
   - Template and configuration management endpoints

5. **CLI Interface** (`main.py`)
   - Command-line access to all features
   - Server mode and standalone operations
   - Batch generation capabilities

## Key Features

### 1. Template-Based Generation (Primary)
The system now uses configurable templates as the primary generation method:
- Legal pleadings with line numbers
- Healthcare forms (CMS-1500)
- Lab reports
- Real estate documents (closing disclosures, warranty deeds)
- Financial documents (bank statements)

### 2. Configuration Management
- Create custom configurations for different styling options
- Apply configurations to individual or batch document generation
- JSON/YAML-based configuration storage

### 3. NER Annotation Generation
- Automatic extraction of bounding box coordinates using Playwright
- HTML elements with `data-label` attributes are automatically annotated
- Optional `data-entity-type` attributes provide semantic NER labels
- Creates JSON files in Qwen-compatible format for NER training

### 4. Batch Generation
- Generate multiple documents with different configurations
- Create layout segmentation datasets
- Support for template variations

## NER Annotation System

### Annotation Attributes
Each template element can have two annotation-related attributes:

1. **`data-label`** - A unique identifier for the annotation (required for coordinate extraction)
2. **`data-entity-type`** - The semantic NER entity type (optional, for enhanced training)

### Scalable Entity Type System
The system supports scalable entity types using an `N` pattern for documents with many elements:

**Scalable Text Elements:**
- `PARAGRAPH_N` - Where N is any paragraph number (PARAGRAPH_20, PARAGRAPH_100, etc.)
- `PARA_NUM_N` - Where N is any paragraph number for the paragraph number itself
- `PARA_TEXT_N` - Where N is any paragraph number for the paragraph text
- `SECTION_N` - Where N is any section number
- `CLAUSE_N` - Where N is any clause number
- `CLAIM_N` - Where N is any claim number
- `CITATION_N` - Where N is any citation number
- `FOOTNOTE_N` - Where N is any footnote number
- `ENDNOTE_N` - Where N is any endnote number
- `APPENDIX_CONTENT_N` - Where N is any appendix number
- `ANNEX_CONTENT_N` - Where N is any annex number
- `SCHEDULE_CONTENT_N` - Where N is any schedule number
- `EXHIBIT_CONTENT_N` - Where N is any exhibit number

### Standard Entity Types

**Legal Documents:**
- `COURT_NAME` - Name of the court
- `JURISDICTION_STATE` - Court's jurisdiction
- `PLAINTIFF_NAME` - Name of the plaintiff
- `DEFENDANT_NAME` - Name of the defendant
- `CASE_NUMBER` - The case identification number
- `CLAIM_TYPE` - General type of legal claim (scalable - use for any number of claims)
- `CLAIM_N` - Where N is any claim number for documents with many claims
- `ATTORNEY_NAME` - Name of the attorney
- `LAW_FIRM` - Name of the law firm
- `STATE_BAR_NUMBER` - Attorney's state bar number
- `DATE_FILED` - Date the document was filed
- `DAMAGES_AMOUNT` - Monetary damages requested
- `SIGNATURE_DATE` - Date of signature

**Financial Documents:**
- `BANK_NAME` - Name of the financial institution
- `ACCOUNT_NUMBER` - Account identification
- `BALANCE_AMOUNT` - Monetary balance
- `DATE_PERIOD` - Date range for statements
- `TRANSACTION_DATE` - Date of a transaction
- `TRANSACTION_DESCRIPTION` - Description of transaction
- `TRANSACTION_AMOUNT` - Transaction monetary value

**Identity Documents:**
- `HOLDER_NAME` - Name of document holder
- `HOLDER_BIRTH_DATE` - Date of birth
- `HOLDER_ADDRESS` - Address of holder
- `HOLDER_HEIGHT` - Physical description
- `HOLDER_WEIGHT` - Physical description
- `HOLDER_EYE_COLOR` - Physical description
- `HOLDER_SEX` - Gender identifier
- `LICENSE_NUMBER` - License identifier
- `LICENSE_CLASS` - License classification
- `ISSUE_DATE` - Issue date of document
- `EXPIRY_DATE` - Expiration date of document

**Healthcare Documents:**
- `HOSPITAL_NAME` - Name of healthcare facility
- `PATIENT_NAME` - Name of patient
- `PATIENT_DOB` - Patient's date of birth
- `PATIENT_SSN` - Patient's social security number
- `PHYSICIAN_NAME` - Name of attending physician
- `DIAGNOSIS_CODE` - Medical diagnostic codes
- `DIAGNOSIS_DESCRIPTION` - Medical condition description
- `PRESCRIPTION_DRUG` - Name of prescribed medication
- `PRESCRIPTION_DOSAGE` - Dosage information
- `PRESCRIPTION_QUANTITY` - Quantity of medication

### Example Annotation
```html
<span data-entity-type="PLAINTIFF_NAME" data-label="plaintiff">{{ plaintiff }}</span>
<span data-entity-type="PARAGRAPH_N" data-label="paragraph_45">{{ paragraph_content }}</span>
```

## Usage

### Web Interface
Start the server: `python main.py server`
Access at: `http://localhost:8000`

### CLI Commands

#### Generate Single Documents
```bash
python main.py generate <template_name> [options]
```
Example:
```bash
python main.py generate legal_pleading --plaintiff "John Doe" --defendant "Acme Corp" --include-pdf
```

#### Generate Batch Documents
```bash
python main.py batch <template_name> --count <number> [options]
```
Example:
```bash
python main.py batch legal_pleading --count 10 --include-pdf
```

#### Generate Documents with NER Annotations
```bash
python main.py unified <template_name> --formats annotations --count <number>
```
Example:
```bash
python main.py unified legal_pleading --formats annotations,jpg --count 5
```

#### Template and Configuration Management
- `python main.py list-templates` - List all available templates
- `python main.py list-configs` - List all available configurations
- `python main.py create-config <name> [options]` - Create a new configuration

#### Layout Dataset Generation
```bash
python main.py layout-dataset --categories legal,healthcare --variations-per-template 3
```

### API Endpoints

#### Document Generation
- `POST /api/generate` - Generate documents
- `POST /api/generate/batch` - Generate batch documents

#### Templates and Configurations
- `GET /api/templates` - List all templates
- `GET /api/configs` - List all configurations
- `POST /api/configs` - Create a new configuration
- `GET /api/template/{id}/preview` - Preview a template

## Configuration Files
Configuration files are stored in the `template_configs/` directory as JSON or YAML files. Each configuration defines styling parameters like:
- Font family and size
- Colors
- Document dimensions
- Layout settings

## Template System
The template system provides:
- Jinja2-based templates for dynamic content
- Configurable styling through configuration files
- Reusable components
- Category-based organization (legal, healthcare, real estate, financial)

## Backward Compatibility
The system maintains backward compatibility with existing API endpoints and usage patterns while providing access to the advanced features through the new unified generator.

## File Output
Generated documents are saved to the `generated_documents/` directory in both HTML and (optionally) PDF formats.
NER annotation files are saved to `ner_dataset/labels/` in JSON format.