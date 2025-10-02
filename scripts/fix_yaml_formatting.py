#!/usr/bin/env python3
"""Fix YAML Framework Formatting.

This script ensures that all framework YAML files use a consistent format,
specifically by converting the 'content' field to use a literal block
scalar (`|`) instead of a standard string with escaped newlines.

This was primarily intended to improve the readability and maintainability
of legacy framework files. The script manually reconstructs the YAML file
to enforce the desired structure.

Author: Warp AI Agent
Date: 2025-10-01
"""

import yaml
from pathlib import Path
import sys
from typing import Dict, Any

def fix_yaml_file(yaml_path: Path) -> bool:
    """Fixes a single YAML file to use a literal block scalar for content.

    This function reads a YAML file, manually reconstructs its content
    line-by-line to enforce a specific format, and writes the result
    back to the file.

    Args:
        yaml_path (Path): The path object pointing to the YAML file.

    Returns:
        bool: True if the file was processed, False if the file was empty
              or could not be parsed.

    Raises:
        yaml.YAMLError: If the input file contains malformed YAML.
        IOError: If there is an error reading or writing the file.
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not data:
        return False

    # Manually construct the YAML to ensure literal block scalar formatting
    yaml_lines = []
    yaml_lines.append(f"name: {data.get('name', '')}")
    
    version = data.get('version', '')
    yaml_lines.append(f"version: \"{version}\"")
    
    yaml_lines.append(f"category: {data.get('category', '')}")
    
    doc = data.get('documentation', {})
    if doc:
        yaml_lines.append("documentation:")
        for key, value in doc.items():
            yaml_lines.append(f"  {key}: {value}")

    framework = data.get('framework', {})
    if framework:
        yaml_lines.append("framework:")
        content = framework.get('content', '')
        yaml_lines.append("  content: |")
        for line in content.split('\n'):
            yaml_lines.append(f"    {line}")

    # Write the properly formatted YAML back to the file
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(yaml_lines))
        f.write('\n')  # Ensure a final newline

    return True

def main() -> int:
    """Main function to process all YAML files in the frameworks directory.

    This function finds all YAML framework files, iterates through them,
    and applies the formatting fix. It prints a summary of the operation.

    Returns:
        int: An exit code, 0 for success, 1 for failure.
    """
    import os
    base_dir = Path(os.getenv('SCRATCHPAD_DIR', Path(__file__).parent.parent))
    frameworks_dir = base_dir / 'frameworks'

    if not frameworks_dir.is_dir():
        print(f"Error: Directory '{frameworks_dir}' not found.", file=sys.stderr)
        return 1

    fixed_count = 0
    error_count = 0
    
    print("Fixing YAML formatting to use literal block scalars...")
    print()
    
    yaml_files = sorted(frameworks_dir.glob('**/*.yml'))
    for yaml_file in yaml_files:
        try:
            if fix_yaml_file(yaml_file):
                print(f"✅ Fixed: {yaml_file.name}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error processing {yaml_file.name}: {e}", file=sys.stderr)
            error_count += 1
    
    print()
    print(f"✨ Complete! Fixed {fixed_count} files.")
    if error_count > 0:
        print(f" Encountered {error_count} errors.")

    return 0

if __name__ == '__main__':
    sys.exit(main())