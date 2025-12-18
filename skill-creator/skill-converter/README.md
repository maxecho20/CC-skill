# Skill Converter

A comprehensive tool for converting various source materials (documentation, GitHub repositories, and PDFs) into Claude AI skills with conflict detection and validation.

## Features

- **GitHub Repository Conversion**: Clone and analyze repositories, extract documentation and code examples
- **Documentation Processing**: Support for Markdown, HTML, text, reStructuredText, and Word documents
- **PDF Processing**: Extract text, code blocks, and structure from PDF documents
- **Conflict Detection**: Identify inconsistencies between documentation and implementation
- **Validation**: Ensure skills meet quality standards and proper structure
- **Packaging**: Generate distributable .zip files with metadata and conflict reports

## Usage

### Individual Converters

#### Convert a GitHub Repository
```bash
python scripts/convert_github_repo.py <github-url> <output-dir>
```

#### Convert Documentation
```bash
python scripts/process_documentation.py <doc-file> <output-dir>
```

#### Convert PDF
```bash
python scripts/pdf_to_skill.py <pdf-file> <output-dir>
```

#### Detect Conflicts
```bash
python scripts/conflict_detector.py <skill-dir> <report-output.json>
```

#### Package Skill
```bash
python scripts/package_generator.py <skill-dir> <output-dir>
```

### Unified Interface

Use the main interface for all conversion types:

```bash
python scripts/convert_all.py <command> <args> [options]

# Examples:
python scripts/convert_all.py github https://github.com/owner/repo ./output
python scripts/convert_all.py docs ./guide.md ./output
python scripts/convert_all.py pdf ./manual.pdf ./output
python scripts/convert_all.py github https://github.com/owner/repo ./output --package
```

## Requirements

### Python Dependencies
- Python 3.6+
- Standard library modules: `os`, `sys`, `re`, `json`, `zipfile`, `pathlib`, `datetime`, `tempfile`, `hashlib`, `subprocess`, `argparse`

### Optional Dependencies (for enhanced functionality)

#### PDF Processing
- `pdfplumber`: Primary PDF text extraction
- `PyPDF2`: Alternative PDF extraction
- `pdftotext`: Command-line PDF tool (poppler-utils)

#### Word Document Processing
- `pandoc`: Document conversion
- `python-docx`: Direct Word document processing

#### Document Analysis
- `PyYAML`: For frontmatter parsing
- `ast`: Python code analysis (built-in)

## Installation

1. Clone or download this skill
2. Ensure Python 3.6+ is installed
3. Install optional dependencies as needed:
   ```bash
   pip install pdfplumber PyPDF2 python-docx PyYAML
   ```

## Output Structure

Converted skills follow the standard Claude skill structure:

```
skill-name/
├── SKILL.md              # Main skill documentation with frontmatter
├── scripts/              # Extracted code examples and utilities
├── references/           # Reference documentation and data
├── assets/              # Templates, images, and other assets
├── conflict_report.json   # Optional conflict analysis
└── package_manifest.json  # Package metadata
```

## Conflict Detection

The conflict detector identifies:

- **Syntax errors** in code examples
- **Missing implementations** for documented functions
- **Undocumented functions** in implementation
- **Deprecated method usage**
- **Missing imports**
- **Version mismatches**
- **Inconsistent naming**

## Quality Metrics

Each generated skill includes quality metrics:
- Completeness score (0-1)
- Conflict count by severity
- Validation errors and warnings
- File structure analysis

## Examples

### Converting a Repository with Documentation
```bash
# Convert and package
python scripts/convert_all.py github \
  https://github.com/psf/requests \
  ./output \
  --package

# Result: requests.skill.zip with:
# - Extracted README as main documentation
# - Code examples from the repository
# - API documentation in references/
# - Conflict detection report
```

### Converting Technical Documentation
```bash
# Convert API documentation
python scripts/process_documentation.py ./api-guide.md ./skills

# Result: api-guide skill with:
# - Structured sections from the document
# - Code examples in scripts/
# - Reference tables in references/
```

### Converting PDF Manual
```bash
# Convert user manual
python scripts/pdf_to_skill.py ./user-manual.pdf ./skills

# Result: user-manual skill with:
# - Extracted chapters as sections
# - Tutorial steps
# - Code examples if present
```

## Contributing

To add support for new document types or enhance existing functionality:

1. Create a new converter script in `scripts/`
2. Follow the established pattern for error handling
3. Add conflict detection rules as needed
4. Update the unified interface in `convert_all.py`
5. Update this README

## License

This skill is provided under the same license as the Skill Creator template.