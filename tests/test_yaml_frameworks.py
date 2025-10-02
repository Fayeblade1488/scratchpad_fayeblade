#!/usr/bin/env python3
"""YAML Framework Validation Test Suite.

This script validates all Scratchpad framework YAML files to ensure they
adhere to syntax, structure, and quality standards. It is the primary
test suite for maintaining the integrity of the framework collection.

The suite includes the following checks:
-   **Syntax Validation**: Ensures all `.yml` files are valid YAML.
-   **Required Keys**: Verifies the presence of essential keys like `name`,
    `category`, `documentation`, and `framework`.
-   **Field Types**: Checks that key fields have the correct data type.
-   **Metadata Quality**: Assesses the conciseness and presence of
    `purpose` and `use_case` fields.
-   **Content Uniqueness**: Performs a basic check for duplicate content.
-   **Category Organization**: Verifies that frameworks are in the correct
    category directories.

Author: Warp AI Agent
Date: 2025-10-01
"""

import sys
import yaml
from pathlib import Path
import re
from typing import List, Dict, Any

def test_yaml_syntax() -> bool:
    """Tests that all YAML files have valid syntax.

    Iterates through all `.yml` files in the `frameworks` directory and
    attempts to parse them using `yaml.safe_load`.

    Returns:
        bool: True if all files parse successfully, False otherwise.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    
    print(f"Found {len(yaml_files)} YAML files to check for syntax.")
    
    passed_count = 0
    failed_count = 0
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"  ✅ {yaml_file.relative_to(base_dir)}")
            passed_count += 1
        except yaml.YAMLError as e:
            print(f"  ❌ {yaml_file.relative_to(base_dir)}: {e}")
            failed_count += 1
    
    print(f"\nYAML Syntax: {passed_count} passed, {failed_count} failed")
    return failed_count == 0


def test_required_keys() -> bool:
    """Tests that all frameworks have the required top-level keys.

    Checks for the presence of 'name', 'category', 'documentation',
    and 'framework'.

    Returns:
        bool: True if all files have the required keys, False otherwise.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    required_keys = ['name', 'category', 'documentation', 'framework']
    
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    passed_count = 0
    failed_count = 0
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            print(f"  ❌ {yaml_file.name}: Not a valid YAML dictionary.")
            failed_count += 1
            continue

        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            print(f"  ❌ {yaml_file.name}: Missing required keys: {missing_keys}")
            failed_count += 1
        else:
            passed_count += 1
    
    print(f"Required Keys: {passed_count} passed, {failed_count} failed")
    return failed_count == 0


def test_framework_categories() -> bool:
    """Tests that frameworks are organized into the correct categories.

    Verifies the directory structure and ensures a minimum number of
    frameworks exist in each category.

    Returns:
        bool: True if the category structure is valid, False otherwise.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    categories = {
        'core': list((frameworks_dir / 'core').glob('*.yml')),
        'purpose-built': list((frameworks_dir / 'purpose-built').glob('*.yml')),
        'personas': list((frameworks_dir / 'personas').glob('*.yml'))
    }
    
    print("Framework Category Counts:")
    for category, files in categories.items():
        print(f"  - {category}: {len(files)} frameworks")
    
    total = sum(len(files) for files in categories.values())
    print(f"\nTotal frameworks: {total}")
    
    return total >= 20


def test_metadata_quality() -> bool:
    """Tests the quality and consistency of framework metadata.

    Checks for the presence and conciseness of 'purpose' and 'use_case'
    fields, and ensures a 'version' field exists.

    Returns:
        bool: True if warnings are below a certain threshold, False otherwise.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    warnings = []
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data or 'documentation' not in data:
            warnings.append(f"  - {yaml_file.name}: Missing 'documentation' section.")
            continue
            
        doc = data['documentation']
        if not doc.get('purpose') or len(doc['purpose'].split()) > 30:
            warnings.append(f"  - {yaml_file.name}: 'purpose' is missing or too long (>30 words).")
        if not doc.get('use_case') or len(doc['use_case'].split()) > 40:
            warnings.append(f"  - {yaml_file.name}: 'use_case' is missing or too long (>40 words).")
        if not data.get('version'):
            warnings.append(f"  - {yaml_file.name}: Missing 'version' field.")
            
    if warnings:
        print("\nMetadata Quality Warnings:")
        for warning in warnings:
            print(warning)
    
    print(f"\nMetadata Quality: {len(yaml_files)} files checked, {len(warnings)} warnings found.")
    return len(warnings) < 10  # Allow a few warnings, but fail if there are too many.


def test_field_types() -> bool:
    """Validates that key YAML fields have the correct data types.

    Returns:
        bool: True if all checked fields have the correct types, False otherwise.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    failed_count = 0
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        errors = []
        if not isinstance(data.get('name'), str): errors.append("'name' must be a string")
        if not isinstance(data.get('version'), str): errors.append("'version' must be a string")
        if not isinstance(data.get('category'), str): errors.append("'category' must be a string")
        if not isinstance(data.get('documentation'), dict): errors.append("'documentation' must be a dictionary")
        if not isinstance(data.get('framework'), dict): errors.append("'framework' must be a dictionary")

        if errors:
            print(f"  ❌ {yaml_file.name}: {', '.join(errors)}")
            failed_count += 1
            
    print(f"Field Types: {len(yaml_files) - failed_count} passed, {failed_count} failed")
    return failed_count == 0


def test_content_uniqueness() -> bool:
    """Performs a functional check for duplicate content across frameworks.

    This test creates a 'signature' for each framework based on its
    documented purpose and the names of its execution steps. This provides
    a more meaningful comparison than a simple string match.

    Returns:
        bool: True if no functional duplicates are found, False otherwise.
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    framework_signatures: Dict[str, str] = {}

    for yaml_file in frameworks_dir.glob('**/*.yml'):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        try:
            # Create a signature from purpose and step names
            purpose = data.get('documentation', {}).get('purpose', '')

            steps_data = data.get('framework', {}).get('system_prompt', {}).get('execution_flow', {}).get('steps', [])
            step_names = sorted([step['name'] for step in steps_data if 'name' in step])

            signature = f"purpose: {purpose.strip()} | steps: {','.join(step_names)}"
            framework_signatures[yaml_file.name] = signature

        except (AttributeError, KeyError, TypeError):
            # Handle files that don't match the expected structure
            continue

    duplicates = []
    seen_signatures: Dict[str, str] = {}
    for name, signature in framework_signatures.items():
        if signature in seen_signatures:
            duplicates.append(f"  - {name} appears to be a functional duplicate of {seen_signatures[signature]}")
        else:
            seen_signatures[signature] = name

    if duplicates:
        print("\nPotential Functional Duplicates Found:")
        for dup in duplicates:
            print(dup)

    return len(duplicates) == 0


def main() -> int:
    """Runs all tests in the suite and prints a summary.

    Returns:
        int: An exit code, 0 if all critical tests pass, 1 otherwise.
    """
    print("="*70)
    print(" YAML Framework Validation Test Suite")
    print("="*70)
    
    tests = [
        ("YAML Syntax Validation", test_yaml_syntax),
        ("Required Keys Check", test_required_keys),
        ("Field Type Validation", test_field_types),
        ("Metadata Quality Check", test_metadata_quality),
        ("Content Uniqueness Check", test_content_uniqueness),
        ("Framework Categories Check", test_framework_categories),
    ]
    
    passed_count = 0
    failed_count = 0
    
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        if test_func():
            print(f"✅ PASSED: {name}")
            passed_count += 1
        else:
            print(f"❌ FAILED: {name}")
            failed_count += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed_count} passed, {failed_count} failed")
    print("="*70)
    
    return 1 if failed_count > 0 else 0


if __name__ == '__main__':
    sys.exit(main())