#!/usr/bin/env python3
"""
Skill Package Generator

Creates distributable .zip packages from converted skills with proper
validation, metadata, and conflict reports.
"""

import os
import sys
import json
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import tempfile
import hashlib

# Import our conflict detector
try:
    from conflict_detector import ConflictDetector
except ImportError:
    ConflictDetector = None


class SkillPackageGenerator:
    """Generates distributable skill packages"""

    def __init__(self):
        self.required_files = ['SKILL.md']
        self.optional_dirs = ['scripts', 'references', 'assets']
        self.max_zip_size = 50 * 1024 * 1024  # 50MB limit

    def package_skill(self, skill_path: Path, output_dir: Path,
                     include_conflict_report: bool = True) -> Dict:
        """Package a skill into a distributable .zip file"""

        result = {
            'success': False,
            'skill_path': str(skill_path),
            'output_path': None,
            'validation': {},
            'conflict_report': None,
            'metadata': {}
        }

        try:
            # Validate skill structure
            validation = self.validate_skill(skill_path)
            result['validation'] = validation

            if not validation['valid']:
                result['error'] = "Skill validation failed"
                return result

            # Generate conflict report if requested
            if include_conflict_report and ConflictDetector:
                conflict_report = self._generate_conflict_report(skill_path)
                result['conflict_report'] = conflict_report

            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate package filename
            skill_name = skill_path.name
            zip_filename = output_dir / f"{skill_name}.zip"
            metadata_filename = output_dir / f"{skill_name}.metadata.json"

            # Create the package
            self._create_zip_package(skill_path, zip_filename,
                                   include_conflict_report and result['conflict_report'])

            # Generate metadata
            metadata = self._generate_package_metadata(skill_path, validation,
                                                     result.get('conflict_report'))
            result['metadata'] = metadata

            # Save metadata
            with open(metadata_filename, 'w') as f:
                json.dump(metadata, f, indent=2)

            result['success'] = True
            result['output_path'] = str(zip_filename)

        except Exception as e:
            result['error'] = str(e)

        return result

    def validate_skill(self, skill_path: Path) -> Dict:
        """Validate skill structure and content"""
        validation = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': {}
        }

        # Check if skill directory exists
        if not skill_path.exists():
            validation['valid'] = False
            validation['errors'].append(f"Skill directory does not exist: {skill_path}")
            return validation

        # Check required files
        for required_file in self.required_files:
            file_path = skill_path / required_file
            if not file_path.exists():
                validation['valid'] = False
                validation['errors'].append(f"Required file missing: {required_file}")

        # Validate SKILL.md format
        skill_md = skill_path / 'SKILL.md'
        if skill_md.exists():
            md_validation = self._validate_skill_md(skill_md)
            validation.update(md_validation)

        # Check optional directories
        for optional_dir in self.optional_dirs:
            dir_path = skill_path / optional_dir
            if dir_path.exists():
                validation['info'][optional_dir] = {
                    'exists': True,
                    'file_count': len(list(dir_path.rglob('*'))),
                    'size_mb': self._get_dir_size_mb(dir_path)
                }
            else:
                validation['info'][optional_dir] = {'exists': False}

        # Check total size
        total_size = self._get_dir_size_mb(skill_path)
        validation['info']['total_size_mb'] = total_size

        if total_size > 100:  # Warn if > 100MB
            validation['warnings'].append(f"Skill is large ({total_size:.1f}MB), consider optimizing")

        return validation

    def _validate_skill_md(self, skill_md: Path) -> Dict:
        """Validate SKILL.md file format"""
        validation = {'errors': [], 'warnings': [], 'info': {}}

        try:
            content = skill_md.read_text(encoding='utf-8')

            # Check for YAML frontmatter
            if not content.startswith('---'):
                validation['errors'].append("Missing YAML frontmatter")
                return validation

            # Extract frontmatter
            frontmatter_end = content.find('---', 3)
            if frontmatter_end == -1:
                validation['errors'].append("Invalid YAML frontmatter format")
                return validation

            frontmatter = content[3:frontmatter_end]

            # Check required fields
            required_fields = ['name', 'description']
            for field in required_fields:
                if f'{field}:' not in frontmatter:
                    validation['errors'].append(f"Missing required field in frontmatter: {field}")

            # Validate name format
            name_match = None
            for line in frontmatter.split('\n'):
                if line.strip().startswith('name:'):
                    name_match = line
                    break

            if name_match:
                name = name_match.split(':', 1)[1].strip()
                if not re.match(r'^[a-z0-9-]+$', name):
                    validation['errors'].append(f"Invalid skill name format: {name}")
                if len(name) > 40:
                    validation['warnings'].append(f"Skill name is long ({len(name)} chars), consider shortening")

            # Check content length
            body_content = content[frontmatter_end + 3:].strip()
            if len(body_content) < 100:
                validation['warnings'].append("SKILL.md content is very short")

            validation['info'] = {
                'content_length': len(content),
                'frontmatter_length': len(frontmatter),
                'body_length': len(body_content)
            }

        except Exception as e:
            validation['errors'].append(f"Error reading SKILL.md: {str(e)}")

        return validation

    def _generate_conflict_report(self, skill_path: Path) -> Optional[Dict]:
        """Generate conflict report for the skill"""
        if not ConflictDetector:
            return None

        try:
            detector = ConflictDetector()
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                report_path = f.name
                detector.generate_conflict_report(
                    detector.analyze_skill(skill_path),
                    Path(report_path)
                )

            # Read and return the report
            with open(report_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {'error': f"Failed to generate conflict report: {str(e)}"}

    def _create_zip_package(self, skill_path: Path, zip_path: Path,
                          conflict_report: Optional[Dict] = None):
        """Create the zip package"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Calculate relative path within zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)

            # Add conflict report if provided
            if conflict_report and 'error' not in conflict_report:
                conflict_json = json.dumps(conflict_report, indent=2)
                zipf.writestr(f"{skill_path.name}/conflict_report.json", conflict_json)

            # Add package manifest
            manifest = self._create_package_manifest(skill_path, conflict_report)
                manifest_json = json.dumps(manifest, indent=2)
                zipf.writestr(f"{skill_path.name}/package_manifest.json", manifest_json)

        # Verify zip size
        if zip_path.stat().st_size > self.max_zip_size:
            zip_path.unlink()
            raise RuntimeError(f"Package too large: {zip_path.stat().st_size} bytes")

    def _create_package_manifest(self, skill_path: Path,
                               conflict_report: Optional[Dict] = None) -> Dict:
        """Create package manifest"""
        manifest = {
            'package_name': skill_path.name,
            'created_at': datetime.now().isoformat(),
            'created_by': 'skill-converter',
            'version': '1.0.0',
            'files': [],
            'directories': [],
            'conflicts_summary': None
        }

        # List files
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(skill_path)
                manifest['files'].append({
                    'path': str(rel_path),
                    'size': file_path.stat().st_size,
                    'hash': self._get_file_hash(file_path)
                })

        # List directories
        for dir_path in skill_path.iterdir():
            if dir_path.is_dir():
                manifest['directories'].append(dir_path.name)

        # Add conflicts summary
        if conflict_report and 'error' not in conflict_report:
            manifest['conflicts_summary'] = {
                'total_conflicts': len(conflict_report.get('conflicts', [])),
                'high_severity': len([c for c in conflict_report.get('conflicts', [])
                                    if c.get('severity') == 'high']),
                'medium_severity': len([c for c in conflict_report.get('conflicts', [])
                                      if c.get('severity') == 'medium']),
                'low_severity': len([c for c in conflict_report.get('conflicts', [])
                                   if c.get('severity') == 'low'])
            }

        return manifest

    def _generate_package_metadata(self, skill_path: Path, validation: Dict,
                                 conflict_report: Optional[Dict] = None) -> Dict:
        """Generate package metadata"""
        metadata = {
            'skill_name': skill_path.name,
            'package_info': {
                'created_at': datetime.now().isoformat(),
                'generator': 'skill-converter',
                'version': '1.0.0'
            },
            'validation': validation,
            'file_structure': {},
            'quality_metrics': {}
        }

        # Analyze file structure
        for item in skill_path.iterdir():
            if item.is_file():
                metadata['file_structure'][item.name] = {
                    'type': 'file',
                    'size': item.stat().st_size
                }
            elif item.is_dir():
                file_count = len(list(item.rglob('*')))
                metadata['file_structure'][item.name] = {
                    'type': 'directory',
                    'file_count': file_count
                }

        # Calculate quality metrics
        metadata['quality_metrics'] = {
            'has_conflicts': conflict_report is not None and
                           'error' not in conflict_report and
                           len(conflict_report.get('conflicts', [])) > 0,
            'conflict_count': len(conflict_report.get('conflicts', [])) if conflict_report else 0,
            'validation_errors': len(validation.get('errors', [])),
            'validation_warnings': len(validation.get('warnings', [])),
            'completeness_score': self._calculate_completeness_score(skill_path)
        }

        return metadata

    def _calculate_completeness_score(self, skill_path: Path) -> float:
        """Calculate skill completeness score (0-1)"""
        score = 0.0
        max_score = 5.0

        # Has SKILL.md (required)
        if (skill_path / 'SKILL.md').exists():
            score += 1.0

        # Has scripts
        if (skill_path / 'scripts').exists() and len(list((skill_path / 'scripts').iterdir())) > 0:
            score += 1.0

        # Has references
        if (skill_path / 'references').exists() and len(list((skill_path / 'references').iterdir())) > 0:
            score += 1.0

        # Has assets
        if (skill_path / 'assets').exists() and len(list((skill_path / 'assets').iterdir())) > 0:
            score += 1.0

        # Has substantial content
        skill_md = skill_path / 'SKILL.md'
        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            if len(content) > 1000:  # Substantial content
                score += 1.0

        return score / max_score

    def _get_dir_size_mb(self, dir_path: Path) -> float:
        """Get directory size in MB"""
        total_size = 0
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size / (1024 * 1024)

    def _get_file_hash(self, file_path: Path) -> str:
        """Get SHA256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()


def main():
    if len(sys.argv) < 3:
        print("Usage: python package_generator.py <skill-directory> <output-directory> [--no-conflicts]")
        print("Example: python package_generator.py ./my-skill ./dist")
        print("         python package_generator.py ./my-skill ./dist --no-conflicts")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    include_conflicts = '--no-conflicts' not in sys.argv

    generator = SkillPackageGenerator()

    try:
        # Package the skill
        result = generator.package_skill(skill_path, output_dir, include_conflicts)

        if result['success']:
            print(f"✅ Successfully packaged skill")
            print(f"   Output: {result['output_path']}")
            print(f"   Metadata: {Path(result['output_path']).parent / Path(result['output_path']).stem + '.metadata.json'}")

            # Print validation summary
            validation = result['validation']
            if validation.get('errors'):
                print(f"   ⚠️  Validation errors: {len(validation['errors'])}")
            if validation.get('warnings'):
                print(f"   ⚠️  Validation warnings: {len(validation['warnings'])}")

            # Print conflict summary if generated
            if result.get('conflict_report') and 'error' not in result['conflict_report']:
                conflicts = len(result['conflict_report'].get('conflicts', []))
                if conflicts > 0:
                    print(f"   ⚠️  Conflicts found: {conflicts}")
                else:
                    print(f"   ✅ No conflicts detected")

            # Print quality metrics
            metrics = result['metadata'].get('quality_metrics', {})
            completeness = metrics.get('completeness_score', 0)
            print(f"   Quality score: {completeness:.1%}")

        else:
            print(f"❌ Failed to package skill: {result.get('error', 'Unknown error')}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()