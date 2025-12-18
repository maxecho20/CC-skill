#!/usr/bin/env python3
"""
GitHub Repository to Skill Converter

Converts GitHub repositories into Claude AI skills by extracting documentation,
code examples, and structure information.
"""

import os
import re
import sys
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import tempfile
import shutil
from datetime import datetime


class GitHubRepoConverter:
    """Converts GitHub repositories to Claude skills"""

    def __init__(self):
        self.api_base = "https://api.github.com"
        self.temp_dir = None

    def clone_or_fetch_repo(self, repo_url, branch="main"):
        """Clone or fetch repository content"""
        parsed = urlparse(repo_url)
        if 'github.com' not in parsed.netloc:
            raise ValueError("Only GitHub repositories are supported")

        # Extract owner and repo from URL
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")

        owner, repo = path_parts[0], path_parts[1]
        clone_url = f"https://github.com/{owner}/{repo}.git"

        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="repo_convert_")

        try:
            # Clone repository
            result = subprocess.run(
                ["git", "clone", clone_url, self.temp_dir],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(f"Failed to clone repository: {result.stderr}")

            return self.temp_dir

        except Exception as e:
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            raise e

    def extract_repo_info(self, repo_path):
        """Extract repository information"""
        info = {}

        # Get basic repo info
        readme_path = self.find_readme(repo_path)
        if readme_path:
            info['readme'] = self.parse_readme(readme_path)

        # Extract documentation files
        info['docs'] = self.extract_documentation(repo_path)

        # Extract code examples
        info['examples'] = self.extract_code_examples(repo_path)

        # Get repository structure
        info['structure'] = self.get_repo_structure(repo_path)

        # Analyze main language
        info['language'] = self.detect_primary_language(repo_path)

        return info

    def find_readme(self, repo_path):
        """Find README file"""
        readme_names = ['README.md', 'README.rst', 'README.txt', 'README']
        for name in readme_names:
            path = Path(repo_path) / name
            if path.exists():
                return path
        return None

    def parse_readme(self, readme_path):
        """Parse README file"""
        content = readme_path.read_text(encoding='utf-8', errors='ignore')

        # Extract title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else readme_path.stem

        # Extract description
        lines = content.split('\n')
        description = ""
        in_description = False

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                if not in_description and line != f"# {title}":
                    in_description = True
                    if description:
                        break
                continue
            if in_description and line:
                description += line + " "

        # Extract code examples
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)
        examples = [{'language': lang or 'text', 'code': code}
                   for lang, code in code_blocks]

        # Extract badges and metadata
        badges = re.findall(r'!\[.*?\]\(.*?\)', content)

        return {
            'title': title,
            'description': description.strip(),
            'content': content,
            'examples': examples,
            'badges': badges
        }

    def extract_documentation(self, repo_path):
        """Extract documentation files"""
        docs = []
        doc_extensions = ['.md', '.rst', '.txt', '.doc', '.docx']
        doc_dirs = ['docs', 'documentation', 'guide', 'manual']

        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common non-doc dirs
            dirs[:] = [d for d in dirs if not d.startswith('.')
                      and d not in ['node_modules', '__pycache__', '.git']]

            for file in files:
                if any(file.endswith(ext) for ext in doc_extensions):
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(repo_path)

                    # Read file content
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        docs.append({
                            'path': str(relative_path),
                            'content': content,
                            'size': len(content)
                        })
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")

        return docs

    def extract_code_examples(self, repo_path):
        """Extract code examples from repository"""
        examples = []
        code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']
        example_dirs = ['examples', 'sample', 'demo', 'tutorial']

        # Look in example directories first
        for root, dirs, files in os.walk(repo_path):
            # Prioritize example directories
            if any(parent_dir in Path(root).parts for parent_dir in example_dirs):
                for file in files:
                    if any(file.endswith(ext) for ext in code_extensions):
                        file_path = Path(root) / file
                        relative_path = file_path.relative_to(repo_path)

                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            examples.append({
                                'path': str(relative_path),
                                'language': file_path.suffix[1:],
                                'content': content,
                                'is_example': True
                            })
                        except Exception as e:
                            print(f"Warning: Could not read {file_path}: {e}")

        return examples

    def get_repo_structure(self, repo_path):
        """Get repository structure"""
        structure = {'dirs': [], 'files': []}

        for root, dirs, files in os.walk(repo_path):
            # Skip hidden and common non-essential directories
            dirs[:] = [d for d in dirs if not d.startswith('.')
                      and d not in ['node_modules', '__pycache__', '.git', 'dist', 'build']]

            root_path = Path(root).relative_to(repo_path)

            for dir_name in dirs:
                structure['dirs'].append(str(root_path / dir_name))

            for file_name in files:
                file_path = Path(root_path) / file_name
                structure['files'].append(str(file_path))

        return structure

    def detect_primary_language(self, repo_path):
        """Detect primary programming language"""
        lang_counts = {}
        extensions = {
            'python': ['.py'],
            'javascript': ['.js', '.jsx'],
            'typescript': ['.ts', '.tsx'],
            'java': ['.java'],
            'cpp': ['.cpp', '.cc', '.cxx'],
            'c': ['.c'],
            'go': ['.go'],
            'rust': ['.rs'],
            'php': ['.php'],
            'ruby': ['.rb'],
            'swift': ['.swift'],
            'kotlin': ['.kt', '.kts']
        }

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')
                      and d not in ['node_modules', '__pycache__', '.git']]

            for file in files:
                ext = Path(file).suffix.lower()
                for lang, lang_exts in extensions.items():
                    if ext in lang_exts:
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1

        return max(lang_counts.items(), key=lambda x: x[1])[0] if lang_counts else 'unknown'

    def generate_skill_metadata(self, repo_info, repo_name):
        """Generate skill metadata from repository information"""
        readme = repo_info.get('readme', {})

        # Generate skill name
        skill_name = repo_name.lower().replace(' ', '-').replace('_', '-')

        # Generate description
        description = readme.get('description', '')
        if not description:
            # Use first paragraph from README
            content = readme.get('content', '')
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
            if paragraphs:
                description = paragraphs[0][:200] + ('...' if len(paragraphs[0]) > 200 else '')

        return {
            'name': skill_name,
            'description': f"Convert and use {repo_name} - {description}" if description else f"Convert and use {repo_name}",
            'title': readme.get('title', repo_name),
            'language': repo_info.get('language', 'unknown'),
            'created_at': datetime.now().isoformat()
        }

    def generate_skill_content(self, repo_info, metadata):
        """Generate skill content from repository information"""
        content = []

        # Add overview section
        content.append("## Overview")
        content.append(f"This skill enables working with {metadata['title']}, a {metadata['language']} project.")

        if repo_info.get('readme', {}).get('description'):
            content.append(f"\n{repo_info['readme']['description']}")

        # Add quick start if examples exist
        if repo_info.get('examples'):
            content.append("\n## Quick Start")
            content.append("Below are code examples extracted from the repository:")

            for i, example in enumerate(repo_info['examples'][:5], 1):  # Limit to 5 examples
                content.append(f"\n### Example {i}: {Path(example['path']).name}")
                content.append(f"```{example['language']}")
                content.append(example['content'][:500] + ('...' if len(example['content']) > 500 else ''))
                content.append("```")

        # Add usage instructions
        content.append("\n## Usage Instructions")
        content.append("To use this skill effectively:")
        content.append("1. Review the code examples above")
        content.append("2. Adapt them to your specific use case")
        content.append("3. Refer to the original repository for complete documentation")

        # Add resources section
        if repo_info.get('docs'):
            content.append(f"\n## Documentation")
            content.append(f"This skill is based on {len(repo_info['docs'])} documentation files:")
            for doc in repo_info['docs'][:10]:  # Limit to 10 docs
                content.append(f"- {doc['path']}")

        return '\n'.join(content)

    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def convert_repo_to_skill(self, repo_url, output_dir):
        """Main conversion function"""
        try:
            # Clone repository
            repo_path = self.clone_or_fetch_repo(repo_url)

            # Extract information
            repo_info = self.extract_repo_info(repo_path)

            # Generate metadata
            repo_name = Path(urlparse(repo_url).path).name.replace('.git', '')
            metadata = self.generate_skill_metadata(repo_info, repo_name)

            # Generate skill content
            skill_content = self.generate_skill_content(repo_info, metadata)

            # Create skill directory structure
            skill_dir = Path(output_dir) / metadata['name']
            skill_dir.mkdir(parents=True, exist_ok=True)

            # Write SKILL.md
            skill_md = skill_dir / 'SKILL.md'
            frontmatter = f"""---
name: {metadata['name']}
description: {metadata['description']}
---

"""
            skill_md.write_text(frontmatter + skill_content)

            # Create scripts directory with examples
            if repo_info.get('examples'):
                scripts_dir = skill_dir / 'scripts'
                scripts_dir.mkdir(exist_ok=True)

                for example in repo_info['examples'][:10]:  # Limit to 10 examples
                    example_name = Path(example['path']).name
                    example_file = scripts_dir / example_name
                    example_file.write_text(example['content'])

            # Create references directory with documentation
            if repo_info.get('docs'):
                refs_dir = skill_dir / 'references'
                refs_dir.mkdir(exist_ok=True)

                for doc in repo_info['docs'][:20]:  # Limit to 20 docs
                    doc_name = Path(doc['path']).name
                    doc_file = refs_dir / doc_name
                    doc_file.write_text(doc['content'])

            return skill_dir

        except Exception as e:
            print(f"Error converting repository: {e}")
            return None
        finally:
            self.cleanup()


def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_github_repo.py <github-repo-url> <output-directory>")
        print("Example: python convert_github_repo.py https://github.com/owner/repo ./output")
        sys.exit(1)

    repo_url = sys.argv[1]
    output_dir = sys.argv[2]

    converter = GitHubRepoConverter()
    skill_dir = converter.convert_repo_to_skill(repo_url, output_dir)

    if skill_dir:
        print(f"✅ Successfully converted repository to skill: {skill_dir}")
    else:
        print("❌ Failed to convert repository")
        sys.exit(1)


if __name__ == "__main__":
    main()