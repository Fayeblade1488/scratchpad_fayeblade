#!/usr/bin/env python3
"""Simple YAML Document Marker Addition Script.

This script ensures that all YAML framework files in the `frameworks/`
directory begin with the `---` document start marker, which is required
for YAML 1.2.2 compliance.

It iterates through all `.yml` and `.yaml` files, reads their content,
and prepends the marker if it is not already present. The script is
idempotent and can be run safely multiple times.

Author: YAML Codex Agent
Date: 2025-10-01
"""

import sys
from pathlib import Path

def add_doc_marker(filepath: Path) -> bool:
    """Adds a '---' document start marker to a YAML file if missing.

    This function reads a file and checks if the content starts with the
    YAML document marker. If not, it prepends the marker to the file's
    content.

    Args:
        filepath (Path): The path to the YAML file to process.

    Returns:
        bool: True if the file was modified, False otherwise.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.strip().startswith('---'):
            return False
        
        new_content = '---\n' + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except IOError as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main() -> int:
    """Main entry point for the script.

    Finds all YAML files in the `frameworks/` directory and processes
    them to add missing document start markers. It prints a summary
    of the actions taken.

    Returns:
        int: An exit code, 0 for success.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    if not frameworks_dir.is_dir():
        print(f"Error: 'frameworks' directory not found at {frameworks_dir}", file=sys.stderr)
        return 1

    yaml_files = list(frameworks_dir.glob('**/*.yml')) + list(frameworks_dir.glob('**/*.yaml'))
    
    modified_count = 0
    skipped_count = 0
    
    print(f"Scanning {len(yaml_files)} YAML files for missing document markers...")
    
    for yaml_file in sorted(yaml_files):
        if add_doc_marker(yaml_file):
            print(f"✅ Added marker to: {yaml_file.name}")
            modified_count += 1
        else:
            skipped_count += 1
    
    print(f"\n✨ Complete! Modified {modified_count} files, skipped {skipped_count}.")
    return 0

if __name__ == '__main__':
    sys.exit(main())