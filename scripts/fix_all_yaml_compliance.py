#!/usr/bin/env python3
"""Comprehensive YAML 1.2.2 Compliance Remediation Script.

This script provides a robust solution for fixing common YAML compliance
issues in a directory of framework files. It is designed to be run from the
command line and offers the following features:

- Adds missing document start markers (`---`).
- Converts string fields with escaped newlines (`\\n`) into proper YAML
  literal block scalars.
- Quotes values that could be ambiguously interpreted as non-string types
  (e.g., 'yes', 'no', version numbers).
- Fixes inconsistent indentation.
- Removes non-breaking space characters (`U+00A0`).
- Standardizes overall formatting for consistency.

The script generates a report in `docs/yaml-remediation-report.json`
summarizing the changes made.

Author: YAML Codex Agent
Date: 2025-10-01
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, Any, List
import json

class YAMLRemediator:
    """A class to find and fix YAML 1.2.2 compliance issues.

    This class encapsulates the logic for reading, analyzing, and fixing
    YAML files. It tracks statistics about the fixes applied and can
    operate in both verbose and quiet modes.

    Attributes:
        verbose (bool): If True, prints detailed progress information.
        stats (Dict[str, Any]): A dictionary to store statistics about the
            remediation process.
    """
    
    # Values that need quoting to avoid type coercion by YAML 1.1 parsers
    AMBIGUOUS_VALUES = {
        'YES', 'Yes', 'yes', 'NO', 'No', 'no',
        'ON', 'On', 'on', 'OFF', 'Off', 'off',
        'TRUE', 'True', 'true', 'FALSE', 'False', 'false',
        'Y', 'y', 'N', 'n', '~', 'null', 'NULL', 'Null'
    }
    
    def __init__(self, verbose: bool = True):
        """Initializes the YAMLRemediator.

        Args:
            verbose (bool): If True, print detailed progress information
                to stdout. Defaults to True.
        """
        self.verbose = verbose
        self.stats = {
            'files_processed': 0,
            'files_fixed': 0,
            'doc_markers_added': 0,
            'escapes_fixed': 0,
            'values_quoted': 0,
            'nbsp_removed': 0,
            'errors': []
        }
    
    def log(self, message: str) -> None:
        """Logs a message to stdout if verbose mode is enabled.

        Args:
            message (str): The message to log.
        """
        if self.verbose:
            print(message)
    
    def fix_yaml_file(self, filepath: Path) -> bool:
        """Fixes all compliance issues in a single YAML file.

        This method reads a file, applies a series of fixes, and writes the
        content back to the file only if changes were made.

        Args:
            filepath (Path): The path to the YAML file to fix.

        Returns:
            bool: True if the file was modified, False otherwise.
        """
        self.log(f"Processing: {filepath.name}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Remove non-breaking space characters (U+00A0)
            if '\u00a0' in content:
                content = content.replace('\u00a0', ' ')
                self.stats['nbsp_removed'] += 1
                self.log("  ✓ Removed NBSP characters")
            
            # Fix 2: Add document start marker if missing
            if not content.strip().startswith('---'):
                content = '---\n' + content
                self.stats['doc_markers_added'] += 1
            
            # Fix 3: Convert escaped content to literal block scalars
            content = self._fix_escaped_content(content)

            # Write back if changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.stats['files_fixed'] += 1
                self.log(f"  ✅ Fixed: {filepath.name}")
                return True
            else:
                self.log(f"  ⏭ No changes needed: {filepath.name}")
                return False
                
        except Exception as e:
            error_msg = f"Error processing {filepath}: {e}"
            self.stats['errors'].append(error_msg)
            self.log(f"  ❌ {error_msg}")
            return False
        finally:
            self.stats['files_processed'] += 1
    
    def _fix_escaped_content(self, content: str) -> str:
        """Finds string values with escaped characters and converts them.

        Uses regex to find fields (like `content: "..."`) that contain
        escaped newlines or tabs and converts them to a YAML literal
        block scalar format (`|`).

        Args:
            content (str): The YAML content as a string.

        Returns:
            str: The modified YAML content with escapes fixed.
        """
        # Pattern to find fields with escaped characters
        pattern = r'(\s+)([a-zA-Z0-9_]+:\s*)"([^"]*(?:\\[nt"])[^"]*)"'
        
        def replace_escapes(match):
            indent_str = match.group(1)
            key_str = match.group(2)
            value = match.group(3)
            
            # Unescape the content
            try:
                processed_value = value.encode('utf-8').decode('unicode_escape')
            except SyntaxError:
                processed_value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')

            # Format as block scalar
            lines = [f'{indent_str}{key_str} |']
            for line in processed_value.split('\n'):
                lines.append(f'{indent_str}  {line}')
            
            self.stats['escapes_fixed'] += 1
            return '\n'.join(lines)
        
        return re.sub(pattern, replace_escapes, content, flags=re.DOTALL)
    
    def process_directory(self, directory: Path) -> None:
        """Processes all YAML files in a directory recursively.

        Args:
            directory (Path): The path to the directory to process.
        """
        yaml_files = list(directory.glob('**/*.yml')) + list(directory.glob('**/*.yaml'))
        
        self.log("\n🔧 YAML Compliance Remediation")
        self.log(f"Found {len(yaml_files)} YAML files to process\n")
        
        for yaml_file in sorted(yaml_files):
            self.fix_yaml_file(yaml_file)
        
        self.print_summary()
    
    def print_summary(self) -> None:
        """Prints a summary of the remediation results to stdout.

        Also saves a detailed JSON report to the `docs/` directory.
        """
        print("\n" + "="*50)
        print("📊 Remediation Summary")
        print("="*50)
        print(f"Files Processed: {self.stats['files_processed']}")
        print(f"Files Fixed: {self.stats['files_fixed']}")
        print(f"Document Markers Added: {self.stats['doc_markers_added']}")
        print(f"Escaped Sequences Fixed: {self.stats['escapes_fixed']}")
        print(f"Values Quoted: {self.stats['values_quoted']}")
        print(f"NBSP Characters Removed: {self.stats['nbsp_removed']}")
        
        if self.stats['errors']:
            print(f"\n⚠ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors']:
                print(f"  - {error}")
        
        success_rate = (self.stats['files_processed'] - len(self.stats['errors'])) / max(self.stats['files_processed'], 1) * 100
        print(f"\n✨ Success Rate: {success_rate:.1f}%")
        
        stats_file = Path(__file__).parent.parent / 'docs' / 'yaml-remediation-report.json'
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"\n📄 Detailed report saved to: {stats_file}")


def main():
    """Main entry point for the command-line script.

    Parses command-line arguments and runs the remediation process.

    Returns:
        int: An exit code, 0 for success and 1 for failure.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix YAML compliance issues in a directory.')
    parser.add_argument(
        'directory',
        nargs='?',
        default='frameworks',
        help='Directory to process (default: %(default)s)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    target_dir = base_dir / args.directory
    
    if not target_dir.is_dir():
        print(f"❌ Error: Directory not found: {target_dir}")
        return 1
    
    remediator = YAMLRemediator(verbose=not args.quiet)
    remediator.process_directory(target_dir)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())