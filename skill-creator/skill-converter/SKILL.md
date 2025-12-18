---
name: skill-converter
description: Convert documentation, GitHub repositories, and PDFs into Claude AI skills with conflict detection. Use this skill when users want to transform existing documentation or code repositories into structured Claude skills, identify discrepancies between docs and implementation, and package everything into distributable .zip files.
---

# Skill Converter

## Overview

This skill enables the conversion of various source materials (documentation, GitHub repositories, and PDFs) into properly formatted Claude AI skills. It automatically analyzes content, detects conflicts between documentation and implementation, and packages everything into distributable skill packages.

## Core Capabilities

### 1. Source Content Processing

The skill handles three main types of source content:

#### Documentation Files
- Markdown files (.md)
- HTML documentation
- Text files (.txt, .rst)
- Word documents (.docx)

#### GitHub Repositories
- Public and private repositories
- Complete repository structure
- README files, wikis, and documentation
- Source code analysis

#### PDF Documents
- Technical documentation
- API specifications
- User manuals and guides

### 2. Content Analysis and Structuring

#### Information Extraction
- Identify key concepts and workflows
- Extract code examples and patterns
- Detect configuration and setup instructions
- Parse API documentation

#### Skill Structure Generation
- Generate appropriate SKILL.md metadata
- Create structured content sections
- Organize into workflow-based or task-based format
- Add progressive disclosure design

### 3. Conflict Detection

#### Documentation vs Implementation Analysis
- Compare documented behavior with actual code
- Identify outdated examples or deprecated methods
- Detect missing error handling or edge cases
- Flag version mismatches

#### Consistency Checks
- Verify code examples are executable
- Check for naming convention consistency
- Validate parameter types and return values
- Ensure all prerequisites are documented

### 4. Skill Packaging

#### Output Structure
```
generated-skill/
├── SKILL.md (required)
├── scripts/ (optional - extracted utilities)
├── references/ (optional - detailed docs)
└── assets/ (optional - templates, images)
```

#### Zip File Generation
- Automatic validation of generated skill
- Proper directory structure maintenance
- Include all necessary dependencies
- Generate metadata for skill marketplace

## Workflow

### Step 1: Source Input
Accept input through:
- Local file paths
- GitHub repository URLs
- Direct file uploads
- Web URLs for documentation

### Step 2: Content Processing
1. Parse and clean source content
2. Extract relevant information blocks
3. Identify code examples and patterns
4. Detect structure and organization

### Step 3: Skill Generation
1. Generate SKILL.md with proper metadata
2. Create appropriate resource directories
3. Organize content using best practices
4. Add conflict detection reports

### Step 4: Validation and Packaging
1. Validate skill structure and format
2. Run conflict detection checks
3. Generate validation report
4. Package into distributable .zip file

## Usage Examples

### Converting a GitHub Repository
```
Input: https://github.com/owner/repo-name
Output: repo-name.skill.zip with:
- Extracted README as main skill documentation
- Code examples in scripts/
- API docs in references/
- Conflict detection report
```

### Converting Documentation
```
Input: ./documentation/api-guide.md
Output: api-guide.skill.zip with:
- Structured skill based on documentation
- Extracted code snippets
- Workflow steps
- Asset files if referenced
```

### Converting PDF Documentation
```
Input: ./manual.pdf
Output: manual.skill.zip with:
- Text extraction and structuring
- Code example identification
- Step-by-step workflows
- Supporting assets
```

## Implementation Notes

### Conflict Detection Algorithm
1. Parse code examples from documentation
2. Attempt to validate syntax and logic
3. Cross-reference with actual implementation (if available)
4. Flag discrepancies with severity levels
5. Generate suggestions for resolution

### Quality Assurance
- Minimum content requirements check
- Structural validation
- Link and reference verification
- Code example testing
- Metadata completeness validation

### Customization Options
- Skill naming conventions
- Output format preferences
- Conflict detection sensitivity
- Template selection
- Inclusion/exclusion rules

## Resources

### scripts/

**convert_github_repo.py** - Repository conversion utilities:
- Clone or fetch repository content
- Parse README and documentation files
- Extract code examples and patterns
- Generate skill structure
- Run conflict detection

**process_documentation.py** - Documentation processing:
- Parse various documentation formats
- Extract structured information
- Identify workflows and procedures
- Convert to skill format
- Handle cross-references

**pdf_to_skill.py** - PDF conversion tools:
- Extract text with formatting preservation
- Identify code blocks and examples
- Parse tables and structured data
- Generate skill-friendly structure
- Handle embedded images

**conflict_detector.py** - Conflict detection engine:
- Parse and validate code examples
- Compare docs with implementation
- Detect inconsistencies
- Generate severity ratings
- Create resolution suggestions

**package_generator.py** - Skill packaging:
- Validate skill structure
- Create proper directory layout
- Generate zip files with metadata
- Include all necessary assets
- Create distribution package

### references/

**skill_templates.md** - Template library:
- Workflow-based templates
- Task-based templates
- Reference/guideline templates
- Mixed-structure templates
- Custom template guidelines

**conflict_patterns.md** - Common conflict patterns:
- Documentation vs code mismatches
- Version compatibility issues
- Deprecated method usage
- Missing error handling
- Incomplete examples

**quality_standards.md** - Skill quality criteria:
- Content requirements
- Structural guidelines
- Validation checklists
- Best practices
- Common pitfalls

### assets/

**skill_templates/** - Template directories:
- Basic workflow template
- API documentation template
- Tool integration template
- Process automation template
- Custom examples

**conflict_reports/** - Report templates:
- Conflict summary template
- Detailed analysis template
- Resolution suggestion template
- Quality metrics template