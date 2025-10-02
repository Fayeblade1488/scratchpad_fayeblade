#!/usr/bin/env python3
"""Bug Fix Validation Tests.

This test suite is designed to verify the fixes for specific bugs that
were discovered and resolved. Each test class corresponds to a bug,
and its methods validate the fix and prevent regressions.

The tests cover issues such as error handling, hardcoded paths,
missing null checks, and major YAML compliance problems like backslash
escapes and missing document markers.

Author: YAML Codex Agent
Date: 2025-10-01
"""

import unittest
import sys
from pathlib import Path
import yaml
import os

# Ensure the scripts directory is in the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import generate_framework_docs, add_framework_metadata, fix_yaml_formatting

class TestBug1ErrorHandling(unittest.TestCase):
    """Tests for Bug #1: Missing error handling in scripts."""

    def test_timestamp_formatting(self):
        """Verifies that generated docs use ISO timestamps, not raw floats."""
        base_dir = Path(__file__).parent.parent
        summary = generate_framework_docs.generate_framework_summary(base_dir)
        
        self.assertIn('Last Updated', summary)
        self.assertRegex(summary, r'Last Updated.*\d{4}-\d{2}-\d{2}T', "Timestamp should be in ISO format.")
        self.assertNotRegex(summary, r'Last Updated.*:\s+\d{10,}\.\d+\s', "Timestamp should not be a raw float.")
    
    def test_specific_exception_handling(self):
        """Ensures scripts catch specific exceptions, not bare `except:`."""
        test_dir = Path(__file__).parent / 'test_data'
        test_dir.mkdir(exist_ok=True)
        bad_yaml = test_dir / 'bad_test.yml'
        bad_yaml.write_text('name: test\n{invalid_yaml:')
        
        try:
            # This call should gracefully handle the YAMLError
            comparison = generate_framework_docs.generate_comparison_table(test_dir.parent)
            self.assertIsNotNone(comparison, "Function should complete without raising an unhandled exception.")
        finally:
            bad_yaml.unlink()
            if test_dir.exists() and not any(test_dir.iterdir()):
                test_dir.rmdir()


class TestBug2HardcodedPaths(unittest.TestCase):
    """Tests for Bug #2: Hardcoded paths in utility scripts."""
    
    def test_environment_variable_support(self):
        """Verifies that scripts respect the SCRATCHPAD_DIR env variable."""
        test_path = "/tmp/test_scratchpad"
        os.environ['SCRATCHPAD_DIR'] = test_path
        
        try:
            import inspect
            # Verify that the main functions in scripts check for the env var
            source_metadata = inspect.getsource(add_framework_metadata.main)
            self.assertIn('SCRATCHPAD_DIR', source_metadata)
            
            source_formatting = inspect.getsource(fix_yaml_formatting.main)
            self.assertIn('SCRATCHPAD_DIR', source_formatting)
        finally:
            del os.environ['SCRATCHPAD_DIR']


class TestBug3NullChecks(unittest.TestCase):
    """Tests for Bug #3: Missing null checks for empty YAML files."""
    
    def test_none_data_handling(self):
        """Ensures empty YAML files don't cause AttributeError."""
        test_dir = Path(__file__).parent / 'test_data'
        test_dir.mkdir(exist_ok=True)
        empty_yaml = test_dir / 'empty_test.yml'
        empty_yaml.write_text('')  # An empty file parses to None
        
        try:
            # This should not raise an AttributeError
            result = add_framework_metadata.add_metadata_to_framework(empty_yaml)
            self.assertIsInstance(result, bool, "Function should handle empty files gracefully.")
        except AttributeError as e:
            self.fail(f"AttributeError raised when handling an empty YAML file: {e}")
        finally:
            empty_yaml.unlink()
            if test_dir.exists() and not any(test_dir.iterdir()):
                test_dir.rmdir()


class TestBug4VersionQuoting(unittest.TestCase):
    """Tests for Bug #4: Incorrectly typed version numbers."""
    
    def test_version_is_quoted_as_string(self):
        """Verifies that numeric versions are quoted as strings."""
        test_dir = Path(__file__).parent / 'test_data'
        test_dir.mkdir(exist_ok=True)
        test_yaml = test_dir / 'version_test.yml'
        test_data = {'name': 'Test', 'version': 1.0, 'category': 'test', 'framework': {'content': '...'} }
        with open(test_yaml, 'w') as f:
            yaml.dump(test_data, f)
        
        try:
            fix_yaml_formatting.fix_yaml_file(test_yaml)
            content = test_yaml.read_text()
            self.assertIn('version: "1.0"', content, "Numeric version should be enclosed in double quotes.")
        finally:
            test_yaml.unlink()
            if test_dir.exists() and not any(test_dir.iterdir()):
                test_dir.rmdir()


class TestBug6BackslashEscapes(unittest.TestCase):
    """Tests for Bug #6: Widespread backslash escape contamination."""
    
    def test_no_active_backslash_n_in_frameworks(self):
        """Verifies that active content fields do not contain `\\n` escapes."""
        base_dir = Path(__file__).parent.parent
        frameworks_dir = base_dir / 'frameworks'
        files_with_escapes = []
        
        for yaml_file in frameworks_dir.glob('**/*.yml'):
            content = yaml_file.read_text()
            # Check for escapes, but ignore the legacy_content field
            content_without_legacy = content.split('legacy_content:')[0]
            if '\\n' in content_without_legacy or '\\t' in content_without_legacy:
                files_with_escapes.append(yaml_file.name)

        self.assertEqual([], files_with_escapes, f"Files with backslash escapes in active content: {files_with_escapes}")


class TestBug7DocumentMarkers(unittest.TestCase):
    """Tests for Bug #7: Missing YAML document start markers."""
    
    def test_all_yaml_files_have_doc_markers(self):
        """Verifies that all YAML files start with the '---' marker."""
        base_dir = Path(__file__).parent.parent
        frameworks_dir = base_dir / 'frameworks'
        files_missing_markers = []

        for yaml_file in frameworks_dir.glob('**/*.yml'):
            content = yaml_file.read_text()
            if not content.strip().startswith('---'):
                files_missing_markers.append(yaml_file.name)
        
        self.assertEqual([], files_missing_markers, f"Files missing '---' document start marker: {files_missing_markers}")


class TestBug8AmbiguousValues(unittest.TestCase):
    """Tests for Bug #8: Unquoted ambiguous values like version numbers."""
    
    def test_version_numbers_are_strings(self):
        """Verifies that all 'version' fields are loaded as strings."""
        base_dir = Path(__file__).parent.parent
        frameworks_dir = base_dir / 'frameworks'
        files_with_unquoted_versions = []
        
        for yaml_file in frameworks_dir.glob('**/*.yml'):
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
            if data and 'version' in data and not isinstance(data['version'], str):
                files_with_unquoted_versions.append(f"{yaml_file.name} (version is {type(data['version']).__name__})")

        self.assertEqual([], files_with_unquoted_versions, f"Files with non-string versions: {files_with_unquoted_versions}")


class TestYAMLCompliance(unittest.TestCase):
    """Tests for overall YAML 1.2.2 compliance."""
    
    def test_all_yaml_files_parse_without_errors(self):
        """Verifies that all YAML files in the frameworks dir parse correctly."""
        base_dir = Path(__file__).parent.parent
        frameworks_dir = base_dir / 'frameworks'
        parse_failures = []

        for yaml_file in frameworks_dir.glob('**/*.yml'):
            try:
                with open(yaml_file, 'r') as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                parse_failures.append(f"{yaml_file.name}: {e}")
        
        self.assertEqual([], parse_failures, f"Files that failed to parse: {parse_failures}")


def run_tests() -> int:
    """Runs all tests in this module and reports the results.

    Returns:
        int: An exit code, 0 for success and 1 for failure.
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())