#!/usr/bin/env python3
"""
Conflict Detection Engine

Detects conflicts between documentation and implementation in skills.
Identifies inconsistencies, deprecated methods, and missing information.
"""

import os
import re
import sys
import json
import ast
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import hashlib


class ConflictDetector:
    """Detects conflicts between documentation and implementation"""

    def __init__(self):
        self.conflict_types = {
            'syntax_error': 'Code examples have syntax errors',
            'deprecated_method': 'Uses deprecated methods or APIs',
            'missing_import': 'Code examples missing required imports',
            'invalid_parameters': 'Function calls with incorrect parameters',
            'version_mismatch': 'Code incompatible with documented version',
            'incomplete_example': 'Code examples are incomplete or non-executable',
            'security_issue': 'Potential security vulnerabilities',
            'performance_issue': 'Code with performance problems',
            'missing_error_handling': 'Lacks proper error handling',
            'inconsistent_naming': 'Naming convention inconsistencies'
        }

        self.language_patterns = {
            'python': {
                'import_pattern': r'^import\s+\w+|^from\s+\w+\s+import',
                'function_def': r'^def\s+(\w+)\s*\(',
                'class_def': r'^class\s+(\w+)',
                'deprecated_patterns': [
                    r'\.deprecated\(',
                    r'@deprecated',
                    r'#.*deprecated'
                ]
            },
            'javascript': {
                'import_pattern': r'^import\s+|^const\s+.*=\s+require\(',
                'function_def': r'^function\s+(\w+|^const\s+(\w+)\s*=\s*\(',
                'class_def': r'^class\s+(\w+)',
                'deprecated_patterns': [
                    r'\.deprecated',
                    r'@deprecated',
                    r'//.*deprecated'
                ]
            },
            'java': {
                'import_pattern': r'^import\s+',
                'function_def': r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\(',
                'class_def': r'^(public\s+)?class\s+(\w+)',
                'deprecated_patterns': [
                    r'@Deprecated',
                    r'//.*deprecated'
                ]
            }
        }

    def analyze_skill(self, skill_path: Path) -> Dict:
        """Analyze a skill for conflicts"""
        if not skill_path.exists():
            raise FileNotFoundError(f"Skill directory not found: {skill_path}")

        analysis = {
            'skill_name': skill_path.name,
            'analysis_date': datetime.now().isoformat(),
            'conflicts': [],
            'warnings': [],
            'info': [],
            'statistics': {}
        }

        # Read SKILL.md
        skill_md = skill_path / 'SKILL.md'
        if skill_md.exists():
            skill_content = skill_md.read_text(encoding='utf-8')
            doc_analysis = self._analyze_documentation(skill_content)
            analysis.update(doc_analysis)

        # Analyze scripts if they exist
        scripts_dir = skill_path / 'scripts'
        if scripts_dir.exists():
            code_analysis = self._analyze_code_files(scripts_dir)
            analysis['code_analysis'] = code_analysis

        # Analyze references
        refs_dir = skill_path / 'references'
        if refs_dir.exists():
            ref_analysis = self._analyze_references(refs_dir)
            analysis['reference_analysis'] = ref_analysis

        # Cross-analysis between docs and code
        if 'doc_analysis' in analysis and 'code_analysis' in analysis:
            cross_conflicts = self._cross_analyze_docs_code(analysis)
            analysis['conflicts'].extend(cross_conflicts)

        # Generate statistics
        analysis['statistics'] = self._generate_statistics(analysis)

        return analysis

    def _analyze_documentation(self, content: str) -> Dict:
        """Analyze documentation content"""
        analysis = {
            'doc_analysis': {
                'code_blocks': [],
                'function_references': [],
                'api_references': [],
                'version_info': []
            }
        }

        # Extract code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)
        for lang, code in code_blocks:
            analysis['doc_analysis']['code_blocks'].append({
                'language': lang or 'unknown',
                'code': code.strip(),
                'line_count': len(code.split('\n')),
                'hash': hashlib.md5(code.encode()).hexdigest()
            })

        # Extract function references
        func_patterns = [
            r'`(\w+)\(\)`',  # `function()`
            r'(\w+)\(\s*\)',  # function()
            r'`(\w+)\([^)]*\)`',  # `function(param)`
        ]

        for pattern in func_patterns:
            matches = re.findall(pattern, content)
            analysis['doc_analysis']['function_references'].extend(matches)

        # Extract API references
        api_patterns = [
            r'(\w+\.\w+)',  # object.method
            r'(\w+\s*\.\s*\w+\s*\([^)]*\))',  # object.method()
        ]

        for pattern in api_patterns:
            matches = re.findall(pattern, content)
            analysis['doc_analysis']['api_references'].extend(matches)

        # Extract version information
        version_patterns = [
            r'version\s+(\d+\.\d+(\.\d+)?)',
            r'v(\d+\.\d+(\.\d+)?)',
            r'requires\s+(\d+\.\d+(\.\d+)?)'
        ]

        for pattern in version_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis['doc_analysis']['version_info'].extend(matches)

        return analysis

    def _analyze_code_files(self, scripts_dir: Path) -> Dict:
        """Analyze code files in scripts directory"""
        analysis = {
            'files': [],
            'functions': [],
            'classes': [],
            'imports': [],
            'language': 'unknown'
        }

        for file_path in scripts_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                file_analysis = self._analyze_code_file(file_path)
                if file_analysis:
                    analysis['files'].append(file_analysis)

                    # Update overall language if detected
                    if file_analysis.get('language') != 'unknown':
                        analysis['language'] = file_analysis['language']

                    # Collect functions and classes
                    analysis['functions'].extend(file_analysis.get('functions', []))
                    analysis['classes'].extend(file_analysis.get('classes', []))
                    analysis['imports'].extend(file_analysis.get('imports', []))

        return analysis

    def _analyze_code_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a single code file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            ext = file_path.suffix.lower()

            # Determine language
            lang_map = {'.py': 'python', '.js': 'javascript', '.java': 'java', '.ts': 'typescript'}
            language = lang_map.get(ext, 'unknown')

            analysis = {
                'file': str(file_path.relative_to(file_path.parent.parent)),
                'language': language,
                'size': len(content),
                'lines': len(content.split('\n')),
                'functions': [],
                'classes': [],
                'imports': [],
                'syntax_valid': True,
                'errors': []
            }

            # Language-specific analysis
            if language in self.language_patterns:
                patterns = self.language_patterns[language]

                # Extract imports
                import_matches = re.findall(patterns['import_pattern'], content, re.MULTILINE)
                analysis['imports'] = import_matches

                # Extract functions
                func_matches = re.findall(patterns['function_def'], content, re.MULTILINE)
                analysis['functions'] = [match[-1] if isinstance(match, tuple) else match for match in func_matches]

                # Extract classes
                class_matches = re.findall(patterns['class_def'], content, re.MULTILINE)
                analysis['classes'] = [match[-1] if isinstance(match, tuple) else match for match in class_matches]

                # Check for deprecated patterns
                for pattern in patterns['deprecated_patterns']:
                    if re.search(pattern, content, re.IGNORECASE):
                        analysis['deprecated_usage'] = True

            # Syntax validation
            if language == 'python':
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    analysis['syntax_valid'] = False
                    analysis['errors'].append({
                        'type': 'syntax_error',
                        'message': str(e),
                        'line': e.lineno
                    })

            return analysis

        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e)
            }

    def _analyze_references(self, refs_dir: Path) -> Dict:
        """Analyze reference materials"""
        analysis = {
            'files': [],
            'apis': [],
            'schemas': []
        }

        for file_path in refs_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                ref_analysis = self._analyze_reference_file(file_path)
                if ref_analysis:
                    analysis['files'].append(ref_analysis)

        return analysis

    def _analyze_reference_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a reference file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            analysis = {
                'file': file_path.name,
                'type': 'unknown',
                'size': len(content)
            }

            # Determine type based on content
            if 'api' in content.lower() or 'endpoint' in content.lower():
                analysis['type'] = 'api_reference'
            elif 'schema' in content.lower() or 'model' in content.lower():
                analysis['type'] = 'schema'
            elif 'guide' in content.lower() or 'tutorial' in content.lower():
                analysis['type'] = 'guide'
            else:
                analysis['type'] = 'documentation'

            return analysis

        except Exception as e:
            return {
                'file': file_path.name,
                'error': str(e)
            }

    def _cross_analyze_docs_code(self, analysis: Dict) -> List[Dict]:
        """Cross-analyze documentation and code for conflicts"""
        conflicts = []

        doc_analysis = analysis.get('doc_analysis', {})
        code_analysis = analysis.get('code_analysis', {})

        # Check if documented functions exist in code
        doc_functions = set(doc_analysis.get('function_references', []))
        code_functions = set(code_analysis.get('functions', []))

        missing_functions = doc_functions - code_functions
        for func in missing_functions:
            conflicts.append({
                'type': 'missing_implementation',
                'severity': 'high',
                'message': f"Function '{func}' referenced in documentation but not found in implementation",
                'suggestion': f"Add implementation for {func} or remove from documentation"
            })

        # Check if code functions are documented
        undocumented_functions = code_functions - doc_functions
        for func in undocumented_functions:
            conflicts.append({
                'type': 'undocumented_function',
                'severity': 'medium',
                'message': f"Function '{func}' implemented but not documented",
                'suggestion': f"Add documentation for {func}"
            })

        # Check for syntax errors in documented code blocks
        for code_block in doc_analysis.get('code_blocks', []):
            if code_block['language'] == 'python':
                try:
                    ast.parse(code_block['code'])
                except SyntaxError as e:
                    conflicts.append({
                        'type': 'syntax_error',
                        'severity': 'high',
                        'message': f"Syntax error in documented code block: {str(e)}",
                        'code_block_hash': code_block['hash'],
                        'suggestion': "Fix syntax error in code example"
                    })

        # Check version compatibility
        doc_versions = doc_analysis.get('version_info', [])
        if doc_versions:
            # Simple version check - could be enhanced
            for version_tuple in doc_versions:
                version = version_tuple[0] if isinstance(version_tuple, tuple) else version_tuple
                if version and version.startswith('1.'):
                    conflicts.append({
                        'type': 'version_mismatch',
                        'severity': 'medium',
                        'message': f"Documentation references old version {version}",
                        'suggestion': "Update documentation to current version"
                    })

        # Check import consistency
        doc_imports = self._extract_imports_from_doc_blocks(doc_analysis.get('code_blocks', []))
        code_imports = set(code_analysis.get('imports', []))

        missing_imports = doc_imports - code_imports
        for imp in missing_imports:
            conflicts.append({
                'type': 'missing_import',
                'severity': 'medium',
                'message': f"Import '{imp}' used in documentation but not found in implementation",
                'suggestion': f"Add import statement for {imp}"
            })

        return conflicts

    def _extract_imports_from_doc_blocks(self, code_blocks: List[Dict]) -> set:
        """Extract import statements from documented code blocks"""
        imports = set()
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import',
            r'require\([\'"]([^\'"]+)[\'"]'
        ]

        for block in code_blocks:
            if block['language'] in ['python', 'javascript', 'typescript']:
                code = block['code']
                for pattern in import_patterns:
                    matches = re.findall(pattern, code)
                    imports.update(matches)

        return imports

    def _generate_statistics(self, analysis: Dict) -> Dict:
        """Generate analysis statistics"""
        stats = {
            'total_conflicts': len(analysis.get('conflicts', [])),
            'conflicts_by_type': {},
            'conflicts_by_severity': {},
            'documentation_metrics': {},
            'code_metrics': {}
        }

        # Count conflicts by type and severity
        for conflict in analysis.get('conflicts', []):
            conflict_type = conflict.get('type', 'unknown')
            severity = conflict.get('severity', 'unknown')

            stats['conflicts_by_type'][conflict_type] = stats['conflicts_by_type'].get(conflict_type, 0) + 1
            stats['conflicts_by_severity'][severity] = stats['conflicts_by_severity'].get(severity, 0) + 1

        # Documentation metrics
        doc_analysis = analysis.get('doc_analysis', {})
        stats['documentation_metrics'] = {
            'code_blocks': len(doc_analysis.get('code_blocks', [])),
            'function_references': len(doc_analysis.get('function_references', [])),
            'api_references': len(doc_analysis.get('api_references', [])),
            'version_info': len(doc_analysis.get('version_info', []))
        }

        # Code metrics
        code_analysis = analysis.get('code_analysis', {})
        stats['code_metrics'] = {
            'files_analyzed': len(code_analysis.get('files', [])),
            'total_functions': len(code_analysis.get('functions', [])),
            'total_classes': len(code_analysis.get('classes', [])),
            'total_imports': len(code_analysis.get('imports', []))
        }

        return stats

    def generate_conflict_report(self, analysis: Dict, output_path: Path):
        """Generate a detailed conflict report"""
        report = {
            'skill_name': analysis['skill_name'],
            'analysis_date': analysis['analysis_date'],
            'summary': self._generate_summary(analysis),
            'conflicts': analysis.get('conflicts', []),
            'warnings': analysis.get('warnings', []),
            'statistics': analysis.get('statistics', {}),
            'recommendations': self._generate_recommendations(analysis)
        }

        # Write report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

    def _generate_summary(self, analysis: Dict) -> str:
        """Generate analysis summary"""
        total_conflicts = len(analysis.get('conflicts', []))
        severity_counts = analysis.get('statistics', {}).get('conflicts_by_severity', {})

        summary_parts = [
            f"Found {total_conflicts} conflicts",
            f"High severity: {severity_counts.get('high', 0)}",
            f"Medium severity: {severity_counts.get('medium', 0)}",
            f"Low severity: {severity_counts.get('low', 0)}"
        ]

        return ". ".join(summary_parts)

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        stats = analysis.get('statistics', {})

        # High severity conflicts
        if stats.get('conflicts_by_severity', {}).get('high', 0) > 0:
            recommendations.append("Address high severity conflicts immediately as they may break functionality")

        # Missing implementations
        conflict_types = stats.get('conflicts_by_type', {})
        if conflict_types.get('missing_implementation', 0) > 0:
            recommendations.append("Implement missing functions or remove them from documentation")

        # Syntax errors
        if conflict_types.get('syntax_error', 0) > 0:
            recommendations.append("Fix syntax errors in code examples")

        # Missing imports
        if conflict_types.get('missing_import', 0) > 0:
            recommendations.append("Add missing import statements")

        # Undocumented functions
        if conflict_types.get('undocumented_function', 0) > 0:
            recommendations.append("Document all implemented functions")

        # No conflicts
        if len(analysis.get('conflicts', [])) == 0:
            recommendations.append("No conflicts detected - skill is well-maintained")

        return recommendations


def main():
    if len(sys.argv) != 3:
        print("Usage: python conflict_detector.py <skill-directory> <output-report.json>")
        print("Example: python conflict_detector.py ./my-skill ./conflict-report.json")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    detector = ConflictDetector()

    try:
        # Analyze skill
        analysis = detector.analyze_skill(skill_path)

        # Generate report
        detector.generate_conflict_report(analysis, output_path)

        # Print summary
        total_conflicts = len(analysis.get('conflicts', []))
        if total_conflicts > 0:
            print(f"⚠️  Found {total_conflicts} conflicts in skill '{skill_path.name}'")
            print(f"   Report saved to: {output_path}")
        else:
            print(f"✅ No conflicts found in skill '{skill_path.name}'")

        # Print top conflicts
        conflicts = analysis.get('conflicts', [])
        if conflicts:
            print("\nTop conflicts:")
            for conflict in conflicts[:5]:
                print(f"   [{conflict.get('severity', 'unknown').upper()}] {conflict.get('message', '')}")

    except Exception as e:
        print(f"❌ Error analyzing skill: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()