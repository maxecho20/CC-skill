#!/usr/bin/env python3
"""
PDF to Skill Converter

Extracts content from PDF documents and converts them into Claude AI skills.
Handles text extraction, code block identification, and structured content parsing.
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import subprocess


class PDFProcessor:
    """Processes PDF files and converts them to skills"""

    def __init__(self):
        self.text_extractors = [
            self._extract_with_pdfplumber,
            self._extract_with_pypdf2,
            self._extract_with_pdftotext
        ]

    def extract_pdf_content(self, pdf_path: Path) -> Dict:
        """Extract content from PDF file"""
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"Not a PDF file: {pdf_path}")

        # Try different extraction methods
        for extractor in self.text_extractors:
            try:
                content = extractor(pdf_path)
                if content and len(content.strip()) > 100:  # Minimum content threshold
                    return self._parse_pdf_content(content)
            except Exception as e:
                print(f"Extractor {extractor.__name__} failed: {e}")
                continue

        raise RuntimeError("All PDF extraction methods failed")

    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber"""
        try:
            import pdfplumber

            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)

            return '\n\n'.join(text_content)

        except ImportError:
            raise RuntimeError("pdfplumber not available")

    def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2"""
        try:
            import PyPDF2

            text_content = []
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text_content.append(page.extract_text())

            return '\n\n'.join(text_content)

        except ImportError:
            raise RuntimeError("PyPDF2 not available")

    def _extract_with_pdftotext(self, pdf_path: Path) -> str:
        """Extract text using pdftotext command line tool"""
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(pdf_path), '-'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return result.stdout
            else:
                raise RuntimeError(f"pdftotext failed: {result.stderr}")

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"pdftotext not available or failed: {e}")

    def _parse_pdf_content(self, content: str) -> Dict:
        """Parse extracted PDF content into structured format"""
        # Split into pages (approximate)
        pages = self._split_into_pages(content)

        # Extract title
        title = self._extract_title_from_pdf(content, pages)

        # Identify sections
        sections = self._identify_pdf_sections(content)

        # Extract code blocks
        code_blocks = self._extract_code_from_text(content)

        # Extract tables
        tables = self._extract_tables_from_text(content)

        # Extract lists
        lists = self._extract_lists_from_text(content)

        # Detect document structure
        structure = self._analyze_document_structure(sections, pages)

        return {
            'title': title,
            'content': content,
            'pages': pages,
            'sections': sections,
            'code_blocks': code_blocks,
            'tables': tables,
            'lists': lists,
            'structure': structure,
            'format': 'pdf'
        }

    def _split_into_pages(self, content: str) -> List[Dict]:
        """Split content into approximate pages"""
        # Simple heuristic: split on form feeds or after large gaps
        pages = []

        # Try form feed character first
        if '\f' in content:
            raw_pages = content.split('\f')
        else:
            # Split on large gaps (multiple newlines)
            raw_pages = re.split(r'\n\s*\n\s*\n\s*\n+', content)

        for i, page in enumerate(raw_pages, 1):
            if page.strip():
                pages.append({
                    'number': i,
                    'content': page.strip(),
                    'line_count': len(page.split('\n'))
                })

        return pages

    def _extract_title_from_pdf(self, content: str, pages: List[Dict]) -> str:
        """Extract title from PDF content"""
        # Try first few lines of first page
        if pages:
            first_page_lines = pages[0]['content'].split('\n')[:5]

            for line in first_page_lines:
                line = line.strip()
                # Look for title-like patterns
                if (len(line) > 10 and len(line) < 100 and
                    not line.lower().startswith(('chapter', 'section', 'page')) and
                    not re.match(r'^\d+\.?\s*', line) and
                    line[0].isupper()):
                    return line

            # Fall back to first line
            if first_page_lines:
                return first_page_lines[0].strip()

        return "PDF Document"

    def _identify_pdf_sections(self, content: str) -> List[Dict]:
        """Identify sections in PDF content"""
        sections = []
        lines = content.split('\n')
        current_section = None

        # Pattern for section headers
        section_patterns = [
            r'^\d+\.\s+(.+)$',  # "1. Section Title"
            r'^\d+\.\d+\s+(.+)$',  # "1.1 Subsection"
            r'^[A-Z][A-Z\s]{5,}$',  # ALL CAPS headers
            r'^[A-Z][a-z\s]+:$',  # "Title:"
        ]

        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Check if this line is a section header
            is_header = False
            for pattern in section_patterns:
                match = re.match(pattern, line)
                if match:
                    is_header = True
                    if current_section:
                        sections.append(current_section)

                    title = match.group(1) if match.groups() else line
                    current_section = {
                        'title': title,
                        'line_number': line_num + 1,
                        'content': []
                    }
                    break

            if not is_header and current_section:
                current_section['content'].append(line)

        # Add last section
        if current_section:
            sections.append(current_section)

        return sections

    def _extract_code_from_text(self, content: str) -> List[Dict]:
        """Extract code blocks from text"""
        code_blocks = []

        # Patterns for code identification
        code_patterns = [
            r'```(\w+)?\n(.*?)\n```',  # Markdown code blocks
            r'```\n(.*?)\n```',  # Unmarked code blocks
            r'/\*.*?\*/',  # C-style comments
            r'<[^>]+>',  # HTML/XML tags
            r'function\s+\w+\s*\([^)]*\)\s*{',  # JavaScript functions
            r'def\s+\w+\s*\([^)]*\)\s*:',  # Python functions
            r'class\s+\w+\s*[:{]',  # Class definitions
            r'import\s+\w+',  # Import statements
            r'#include\s*[<"][^>"]*[>"]',  # C/C++ includes
        ]

        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    lang, code = match
                    code_blocks.append({
                        'language': lang or 'unknown',
                        'code': code.strip(),
                        'pattern': pattern
                    })
                else:
                    code_blocks.append({
                        'language': 'unknown',
                        'code': match.strip(),
                        'pattern': pattern
                    })

        # Remove duplicates while preserving order
        seen = set()
        unique_blocks = []
        for block in code_blocks:
            code_hash = hash(block['code'][:100])  # First 100 chars as hash
            if code_hash not in seen:
                seen.add(code_hash)
                unique_blocks.append(block)

        return unique_blocks

    def _extract_tables_from_text(self, content: str) -> List[Dict]:
        """Extract table data from text"""
        tables = []

        # Look for tabular data patterns
        lines = content.split('\n')
        current_table = None

        for line in lines:
            # Simple heuristic: lines with multiple consistent separators
            if re.search(r'(\s{3,}|\t{2,}).*\1.*\1', line):
                if not current_table:
                    current_table = {'headers': [], 'rows': []}

                # Split on consistent whitespace
                row = re.split(r'\s{3,}|\t{2,}', line.strip())
                if not current_table['headers']:
                    current_table['headers'] = row
                else:
                    current_table['rows'].append(row)
            else:
                if current_table:
                    tables.append(current_table)
                    current_table = None

        # Add final table if exists
        if current_table:
            tables.append(current_table)

        return tables

    def _extract_lists_from_text(self, content: str) -> List[Dict]:
        """Extract list structures from text"""
        lists = []

        # Pattern for list items
        list_patterns = [
            r'^\s*[-•*]\s+(.+)$',  # Bullet points
            r'^\s*\d+\.\s+(.+)$',  # Numbered lists
            r'^\s*[a-zA-Z]\.\s+(.+)$',  # Lettered lists
            r'^\s*\(\d+\)\s+(.+)$',  # Parenthesized numbers
        ]

        lines = content.split('\n')
        current_list = None

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                if current_list:
                    lists.append(current_list)
                    current_list = None
                continue

            # Check if this is a list item
            for pattern in list_patterns:
                match = re.match(pattern, line)
                if match:
                    if not current_list:
                        current_list = {
                            'type': self._get_list_type(pattern),
                            'items': []
                        }

                    current_list['items'].append({
                        'text': match.group(1),
                        'indent': len(line) - len(line.lstrip())
                    })
                    break

        # Add final list if exists
        if current_list:
            lists.append(current_list)

        return lists

    def _get_list_type(self, pattern: str) -> str:
        """Determine list type from pattern"""
        if '[-•*]' in pattern:
            return 'bullet'
        elif r'\d+\.' in pattern:
            return 'numbered'
        elif r'[a-zA-Z]\.' in pattern:
            return 'lettered'
        elif r'\(\d+\)' in pattern:
            return 'parenthesized'
        else:
            return 'unknown'

    def _analyze_document_structure(self, sections: List[Dict], pages: List[Dict]) -> Dict:
        """Analyze document structure and categorize"""
        structure = {
            'type': 'unknown',
            'has_code': False,
            'has_tables': False,
            'has_lists': False,
            'section_count': len(sections),
            'page_count': len(pages),
            'complexity': 'medium'
        }

        # Analyze section titles to determine document type
        section_titles = [s['title'].lower() for s in sections]

        if any(keyword in ' '.join(section_titles) for keyword in ['api', 'reference', 'method', 'function']):
            structure['type'] = 'api_documentation'
        elif any(keyword in ' '.join(section_titles) for keyword in ['tutorial', 'guide', 'how to', 'step']):
            structure['type'] = 'tutorial'
        elif any(keyword in ' '.join(section_titles) for keyword in ['manual', 'handbook', 'documentation']):
            structure['type'] = 'manual'
        elif any(keyword in ' '.join(section_titles) for keyword in ['chapter', 'section', 'part']):
            structure['type'] = 'book'

        # Determine complexity
        if structure['section_count'] > 20:
            structure['complexity'] = 'high'
        elif structure['section_count'] < 5:
            structure['complexity'] = 'low'

        return structure

    def generate_skill_from_pdf(self, pdf_info: Dict, pdf_name: str) -> Dict:
        """Generate skill structure from PDF content"""
        # Generate skill name
        skill_name = pdf_name.lower().replace(' ', '-').replace('_', '-')
        skill_name = re.sub(r'[^a-z0-9-]', '', skill_name)

        # Generate content based on document type
        doc_type = pdf_info.get('structure', {}).get('type', 'unknown')

        if doc_type == 'api_documentation':
            content = self._generate_api_skill_content(pdf_info)
        elif doc_type == 'tutorial':
            content = self._generate_tutorial_skill_content(pdf_info)
        elif doc_type == 'manual':
            content = self._generate_manual_skill_content(pdf_info)
        else:
            content = self._generate_general_skill_content(pdf_info)

        # Generate description
        description = self._generate_pdf_description(pdf_info)

        return {
            'name': skill_name,
            'description': description,
            'title': pdf_info.get('title', pdf_name),
            'content': content,
            'document_type': doc_type,
            'assets': self._extract_pdf_assets(pdf_info),
            'references': self._generate_pdf_references(pdf_info)
        }

    def _generate_api_skill_content(self, pdf_info: Dict) -> str:
        """Generate skill content for API documentation"""
        content = []

        # Overview
        content.append("## API Reference")
        content.append(f"This skill provides reference information for {pdf_info.get('title', 'the API')}.")
        content.append("")

        # Sections as API endpoints or methods
        sections = pdf_info.get('sections', [])
        for section in sections[:10]:  # Limit to 10 sections
            content.append(f"### {section['title']}")
            if section.get('content'):
                section_text = '\n'.join(section['content'][:5])  # Limit content per section
                content.append(section_text)
            content.append("")

        # Code examples
        if pdf_info.get('code_blocks'):
            content.append("## Code Examples")
            for i, block in enumerate(pdf_info['code_blocks'][:5], 1):
                content.append(f"### Example {i}")
                content.append(f"```{block.get('language', 'text')}")
                # Limit code block size
                code = block['code']
                if len(code) > 500:
                    code = code[:500] + '...'
                content.append(code)
                content.append("```")
                content.append("")

        return '\n'.join(content)

    def _generate_tutorial_skill_content(self, pdf_info: Dict) -> str:
        """Generate skill content for tutorials"""
        content = []

        # Overview
        content.append("## Tutorial")
        content.append(f"This skill guides you through {pdf_info.get('title', 'the process')}.")
        content.append("")

        # Tutorial steps
        content.append("## Steps")
        sections = pdf_info.get('sections', [])
        for i, section in enumerate(sections[:15], 1):  # Limit to 15 steps
            content.append(f"### Step {i}: {section['title']}")
            if section.get('content'):
                step_content = '\n'.join(section['content'][:3])  # Limit per step
                content.append(step_content)
            content.append("")

        # Lists as action items
        if pdf_info.get('lists'):
            content.append("## Key Points")
            for lst in pdf_info['lists'][:3]:  # Limit to 3 lists
                for item in lst['items'][:5]:  # Limit to 5 items per list
                    content.append(f"- {item['text']}")
            content.append("")

        return '\n'.join(content)

    def _generate_manual_skill_content(self, pdf_info: Dict) -> str:
        """Generate skill content for manuals"""
        content = []

        # Overview
        content.append("## Manual")
        content.append(f"This skill contains information from {pdf_info.get('title', 'the manual')}.")
        content.append("")

        # Manual sections
        sections = pdf_info.get('sections', [])
        for section in sections[:20]:  # Limit to 20 sections
            content.append(f"### {section['title']}")
            if section.get('content'):
                section_text = '\n'.join(section['content'][:3])  # Limit per section
                content.append(section_text)
            content.append("")

        # Tables as reference data
        if pdf_info.get('tables'):
            content.append("## Reference Tables")
            for i, table in enumerate(pdf_info['tables'][:3], 1):
                content.append(f"### Table {i}")
                if table.get('headers'):
                    content.append(f"Headers: {', '.join(table['headers'])}")
                if table.get('rows'):
                    content.append(f"Data: {len(table['rows'])} rows")
                content.append("")

        return '\n'.join(content)

    def _generate_general_skill_content(self, pdf_info: Dict) -> str:
        """Generate skill content for general documents"""
        content = []

        # Overview
        content.append("## Overview")
        content.append(f"This skill is based on {pdf_info.get('title', 'PDF document')}.")
        content.append("")

        # Key sections
        sections = pdf_info.get('sections', [])
        if sections:
            content.append("## Key Sections")
            for section in sections[:10]:  # Limit to 10 sections
                content.append(f"### {section['title']}")
                if section.get('content'):
                    section_text = '\n'.join(section['content'][:2])  # Limit per section
                    content.append(section_text)
                content.append("")

        # General content
        if not sections and pdf_info.get('content'):
            content.append("## Content")
            # Take first part of content
            content_text = pdf_info['content'][:1000] + ('...' if len(pdf_info['content']) > 1000 else '')
            content.append(content_text)
            content.append("")

        return '\n'.join(content)

    def _generate_pdf_description(self, pdf_info: Dict) -> str:
        """Generate skill description for PDF"""
        title = pdf_info.get('title', 'PDF document')
        doc_type = pdf_info.get('structure', {}).get('type', 'document')
        page_count = pdf_info.get('structure', {}).get('page_count', 0)

        if page_count:
            return f"A skill based on {title} ({doc_type}, {page_count} pages)"
        else:
            return f"A skill based on {title} ({doc_type})"

    def _extract_pdf_assets(self, pdf_info: Dict) -> List:
        """Extract assets from PDF information"""
        assets = []

        # Tables as assets
        for table in pdf_info.get('tables', []):
            assets.append({
                'type': 'table',
                'data': table,
                'format': 'json'
            })

        return assets

    def _generate_pdf_references(self, pdf_info: Dict) -> List:
        """Generate reference materials from PDF"""
        references = []

        # Add sections as reference
        if pdf_info.get('sections'):
            references.append({
                'type': 'sections',
                'content': pdf_info['sections']
            })

        # Add code examples as reference
        if pdf_info.get('code_blocks'):
            references.append({
                'type': 'code_examples',
                'content': pdf_info['code_blocks']
            })

        return references


def main():
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_skill.py <pdf-file> <output-directory>")
        print("Example: python pdf_to_skill.py ./manual.pdf ./output")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    processor = PDFProcessor()

    try:
        # Extract PDF content
        pdf_info = processor.extract_pdf_content(pdf_path)

        # Generate skill
        skill_data = processor.generate_skill_from_pdf(pdf_info, pdf_path.stem)

        # Create skill directory
        skill_dir = output_dir / skill_data['name']
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        skill_md = skill_dir / 'SKILL.md'
        frontmatter = f"""---
name: {skill_data['name']}
description: {skill_data['description']}
---

"""
        skill_md.write_text(frontmatter + skill_data['content'])

        # Save assets
        if skill_data['assets']:
            assets_dir = skill_dir / 'assets'
            assets_dir.mkdir(exist_ok=True)

            for asset in skill_data['assets']:
                asset_file = assets_dir / f"{asset['type']}.{asset.get('format', 'json')}"
                if isinstance(asset['data'], str):
                    asset_file.write_text(asset['data'])
                else:
                    asset_file.write_text(json.dumps(asset['data'], indent=2))

        # Save references
        if skill_data['references']:
            refs_dir = skill_dir / 'references'
            refs_dir.mkdir(exist_ok=True)

            for ref in skill_data['references']:
                ref_file = refs_dir / f"{ref['type']}.json"
                ref_file.write_text(json.dumps(ref['content'], indent=2))

        print(f"✅ Successfully converted PDF to skill: {skill_dir}")
        print(f"   Document type: {skill_data.get('document_type', 'unknown')}")
        print(f"   Sections found: {len(pdf_info.get('sections', []))}")

    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()