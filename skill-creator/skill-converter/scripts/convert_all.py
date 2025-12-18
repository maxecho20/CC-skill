#!/usr/bin/env python3
"""
Skill Converter - Main Interface

Provides a unified interface for converting various sources into Claude skills.
"""

import argparse
import sys
from pathlib import Path

# Import converter modules
try:
    from convert_github_repo import GitHubRepoConverter
    from process_documentation import DocumentationProcessor
    from pdf_to_skill import PDFProcessor
    from package_generator import SkillPackageGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all converter scripts are in the same directory")
    sys.exit(1)


def convert_github_repo(args):
    """Convert GitHub repository to skill"""
    converter = GitHubRepoConverter()
    skill_dir = converter.convert_repo_to_skill(args.url, args.output)

    if skill_dir:
        print(f"✅ Repository converted successfully: {skill_dir}")

        # Package if requested
        if args.package:
            package_skill(skill_dir, args.output)
    else:
        print("❌ Failed to convert repository")
        return False
    return True


def convert_documentation(args):
    """Convert documentation to skill"""
    processor = DocumentationProcessor()

    try:
        doc_path = Path(args.file)
        doc_info = processor.process_file(doc_path)
        skill_data = processor.generate_skill_from_doc(doc_info, doc_path.stem)

        # Create skill directory
        output_dir = Path(args.output)
        skill_dir = output_dir / skill_data['name']
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        skill_md = skill_dir / 'SKILL.md'
        import json
        frontmatter = f"""---
name: {skill_data['name']}
description: {skill_data['description']}
---

"""
        skill_md.write_text(frontmatter + skill_data['content'])

        print(f"✅ Documentation converted successfully: {skill_dir}")

        # Package if requested
        if args.package:
            package_skill(skill_dir, args.output)

        return True

    except Exception as e:
        print(f"❌ Error converting documentation: {e}")
        return False


def convert_pdf(args):
    """Convert PDF to skill"""
    processor = PDFProcessor()

    try:
        pdf_path = Path(args.file)
        pdf_info = processor.extract_pdf_content(pdf_path)
        skill_data = processor.generate_skill_from_pdf(pdf_info, pdf_path.stem)

        # Create skill directory
        output_dir = Path(args.output)
        skill_dir = output_dir / skill_data['name']
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        skill_md = skill_dir / 'SKILL.md'
        import json
        frontmatter = f"""---
name: {skill_data['name']}
description: {skill_data['description']}
---

"""
        skill_md.write_text(frontmatter + skill_data['content'])

        print(f"✅ PDF converted successfully: {skill_dir}")
        print(f"   Document type: {skill_data.get('document_type', 'unknown')}")

        # Package if requested
        if args.package:
            package_skill(skill_dir, args.output)

        return True

    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        return False


def package_skill(skill_dir, output_dir):
    """Package a skill into zip file"""
    generator = SkillPackageGenerator()
    result = generator.package_skill(skill_dir, Path(output_dir), include_conflict_report=True)

    if result['success']:
        print(f"✅ Skill packaged successfully: {result['output_path']}")
    else:
        print(f"⚠️  Packaging failed: {result.get('error', 'Unknown error')}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert various sources into Claude AI skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a GitHub repository
  python convert_all.py github https://github.com/owner/repo ./output

  # Convert documentation
  python convert_all.py docs ./guide.md ./output

  # Convert PDF
  python convert_all.py pdf ./manual.pdf ./output

  # Convert and package
  python convert_all.py github https://github.com/owner/repo ./output --package
        """
    )

    subparsers = parser.add_subparsers(dest='command', required=True, help='Conversion type')

    # GitHub repository converter
    github_parser = subparsers.add_parser('github', help='Convert GitHub repository')
    github_parser.add_argument('url', help='GitHub repository URL')
    github_parser.add_argument('output', help='Output directory')
    github_parser.add_argument('--package', action='store_true', help='Package into .zip file')
    github_parser.set_defaults(func=convert_github_repo)

    # Documentation converter
    docs_parser = subparsers.add_parser('docs', help='Convert documentation')
    docs_parser.add_argument('file', help='Documentation file path')
    docs_parser.add_argument('output', help='Output directory')
    docs_parser.add_argument('--package', action='store_true', help='Package into .zip file')
    docs_parser.set_defaults(func=convert_documentation)

    # PDF converter
    pdf_parser = subparsers.add_parser('pdf', help='Convert PDF document')
    pdf_parser.add_argument('file', help='PDF file path')
    pdf_parser.add_argument('output', help='Output directory')
    pdf_parser.add_argument('--package', action='store_true', help='Package into .zip file')
    pdf_parser.set_defaults(func=convert_pdf)

    # Parse arguments
    args = parser.parse_args()

    # Execute conversion
    success = args.func(args)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()