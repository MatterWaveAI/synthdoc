# Batch Document Generator

The Batch Document Generator is a powerful system for creating multiple document variations with different templates, configurations, and data. It's particularly designed for generating training datasets for machine learning applications, such as layout segmentation and NER (Named Entity Recognition) models.

## Purpose

The Batch Generator system allows for:
- Generating large sets of documents with systematic variations
- Creating diverse datasets for ML training
- Testing model robustness against different layouts and styles
- Producing synthetic documents with realistic content for data augmentation

## Installation

The Batch Generator is part of the Document Generator system. First, install the required dependencies:

```bash
cd synthdoc
pip install -r requirements.txt
```

The system requires additional dependencies for generating realistic data:
- `faker`: For generating realistic test data

## Configuration System

The system uses a flexible configuration system based on the `TemplateConfig` dataclass. Each configuration includes styling and layout parameters:

- `font_family`: Font family for the document
- `font_size`: Font size (e.g., "12px", "12pt")
- `width`/`height`: Document dimensions (default: 8.5in x 11in)
- `margin`: Document margins
- `line_height`: Line height for text
- `color`/`background`: Text and background colors
- `border`: Border styling
- `layout_type`: Layout type ("standard", "grid", "form", "narrative")
- `components`: List of components to include in the template

Configurations can be stored in JSON or YAML files in the `template_configs` directory, and the system supports generating systematic variations of configurations.

## Usage

### Basic Batch Generation

Generate a batch of documents using a single template with cycling configurations:

```python
from synthdoc.templates import BatchGenerator

# Create a batch generator instance
batch_gen = BatchGenerator(output_dir="generated_documents")

# Define a data generator function
def data_generator(index):
    return {
        "title": f"Document {index}",
        "content": f"This is content for document {index}",
        "metadata": {"id": index, "date": "2023-01-01"}
    }

# Generate 10 documents using a legal pleading template
generated_files = batch_gen.generate_batch(
    template_name="legal_pleading",
    data_generator_func=data_generator,
    count=10,
    config_names=["legal_default", "legal_alt_style"],  # Optional: specific configs
    output_prefix="batch_"  # Optional: prefix for output files
)

print(f"Generated {len(generated_files)} documents")
```

### Template Variations

Generate documents with systematically varied configurations:

```python
from synthdoc.templates import BatchGenerator

batch_gen = BatchGenerator()

# Define parameter variations
variation_params = {
    "font_family": [
        "Arial, sans-serif",
        "'Times New Roman', serif",
        "'Courier New', Courier, monospace"
    ],
    "font_size": ["10pt", "11pt", "12pt"],
    "background": ["white", "#fafafa", "#f0f0f0"]
}

# Generate variations with different styling
variation_results = batch_gen.generate_template_variations(
    base_template_name="legal_pleading",
    variation_params=variation_params,
    data_generator_func=lambda i: {
        "plaintiff": f"Plaintiff {i}",
        "defendant": f"Defendant {i}",
        "content": [f"Content paragraph {j}" for j in range(3)]
    },
    count_per_variation=5  # Generate 5 documents per configuration variation
)

# variation_results is a dictionary mapping variation names to file lists
for variation_name, files in variation_results.items():
    print(f"Variation {variation_name}: {len(files)} documents")
```

### Layout Segmentation Dataset

Generate a comprehensive dataset for layout segmentation training:

```python
from synthdoc.templates import BatchGenerator

batch_gen = BatchGenerator()

# Generate a dataset with multiple document categories
dataset_results = batch_gen.generate_layout_segmentation_dataset(
    template_categories=["legal", "healthcare", "real_estate"],
    variations_per_template=3,    # 3 style variations per template
    docs_per_variation=10         # 10 documents per variation
)

# Print results by template
for template_name, files in dataset_results.items():
    print(f"{template_name}: {len(files)} documents")
```

## Available Methods

### `BatchGenerator(output_dir="generated_documents")`

Constructor for the batch generator. Creates the output directory if it doesn't exist.

### `generate_batch(template_name, data_generator_func, count, config_names=None, output_prefix="")`

Generates a batch of documents using a specified template and configurations.

- `template_name`: Name of the template to use
- `data_generator_func`: Function that returns data for each document (takes an index parameter)
- `count`: Number of documents to generate
- `config_names`: List of configuration names to cycle through (defaults to template-specific configs)
- `output_prefix`: Prefix for output filenames

Returns: List of generated file paths (HTML files) and corresponding JSON data files.

### `generate_template_variations(base_template_name, variation_params, data_generator_func, count_per_variation=1)`

Generates documents using template variations based on parameter options.

- `base_template_name`: Name of the base template to vary
- `variation_params`: Dictionary mapping config fields to lists of possible values
- `data_generator_func`: Function that returns data for each document
- `count_per_variation`: Number of documents to generate per variation

Returns: Dictionary mapping variation names to lists of generated file paths.

### `generate_layout_segmentation_dataset(template_categories, variations_per_template=5, docs_per_variation=10)`

Generates a comprehensive dataset for layout segmentation training.

- `template_categories`: List of template categories to include
- `variations_per_template`: Number of style/layout variations per template
- `docs_per_variation`: Number of documents per variation

Returns: Dictionary mapping template names to lists of generated file paths.

## File Output

The batch generator creates two files for each generated document:
1. HTML file: The rendered document
2. JSON file: The source data used to generate the document

File naming convention:
- Document: `{prefix}{template_name}_{index:03d}_{config_name}_{timestamp}.html`
- Data: `{prefix}{template_name}_{index:03d}_{config_name}_{timestamp}_data.json`

## Category-Specific Customizations

The system includes category-specific default variations:

- **Legal**: Uses specific font sizes (in points), line heights, and optional components like line numbers and caption boxes
- **Healthcare**: Uses smaller fonts, grid/form layouts, and medical-specific styling
- **Real Estate**: Uses serif fonts, narrative or form layouts, and property-specific styling
- **Financial**: Uses financial-specific layouts and styling

## Integration

The Batch Generator integrates with:
- Template registry system for accessing different document templates
- Configuration manager for managing styling options
- Faker library for generating realistic test data
- The core document generation system for rendering templates

This makes it an ideal tool for creating training datasets for ML models that need to handle diverse document layouts and styles.