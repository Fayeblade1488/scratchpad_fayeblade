#!/usr/bin/env python3
"""Framework Documentation Generator.

This script automatically generates markdown documentation from the metadata
of all framework YAML files in the `frameworks/` directory. It creates two
key documents in the `docs/` directory:

1.  `FRAMEWORK_REFERENCE.md`: A detailed reference guide with the purpose,
    use case, and other metadata for each framework, organized by category.
2.  `FRAMEWORK_COMPARISON.md`: A summary table comparing all frameworks
    by name, category, version, and character count.

This script is intended to be run whenever frameworks are added or their
metadata is updated, ensuring documentation stays consistent.

Author: Warp AI Agent
Date: 2025-10-01
"""

import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List

def load_framework(yaml_path: Path) -> Dict[str, Any]:
    """Loads and parses a single YAML framework file.

    Args:
        yaml_path (Path): The path to the YAML framework file.

    Returns:
        Dict[str, Any]: The parsed YAML data as a dictionary.

    Raises:
        yaml.YAMLError: If the file contains malformed YAML.
        FileNotFoundError: If the specified file does not exist.
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_framework_summary(base_dir: Path) -> str:
    """Generates a detailed markdown summary of all frameworks.

    This function iterates through all frameworks, groups them by category,
    and generates a detailed description for each one, including its
    purpose, use case, and other metadata.

    Args:
        base_dir (Path): The base directory of the repository, containing
            the `frameworks` subdirectory.

    Returns:
        str: A string containing the full markdown documentation.
    """
    frameworks_dir = base_dir / 'frameworks'
    
    categories = defaultdict(list)
    
    for yaml_file in sorted(frameworks_dir.glob('**/*.yml')):
        try:
            data = load_framework(yaml_file)
            if not data:
                print(f"Warning: Skipping empty or invalid file {yaml_file}")
                continue

            category = yaml_file.parent.name
            
            framework_info = {
                'name': data.get('name', yaml_file.stem),
                'version': data.get('version', 'N/A'),
                'file': yaml_file.name,
                'purpose': data.get('documentation', {}).get('purpose', 'No description available.'),
                'use_case': data.get('documentation', {}).get('use_case', 'No use case specified.'),
                'character_count': data.get('documentation', {}).get('character_count', 'Unknown'),
            }
            
            categories[category].append(framework_info)
        except Exception as e:
            print(f"Warning: Could not process {yaml_file}: {e}")
    
    # Generate markdown content
    md_lines = [
        "# Framework Quick Reference\n",
        f"_This document was auto-generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC_\n",
        "---\n\n"
    ]
    
    md_lines.append("## Table of Contents\n")
    for category in sorted(categories.keys()):
        md_lines.append(f"- [{category.title()}](#{category.lower().replace(' ', '-')})\n")
    md_lines.append("\n---\n")
    
    for category in sorted(categories.keys()):
        md_lines.append(f"## {category.title()}\n\n")
        
        for fw in sorted(categories[category], key=lambda x: x['name']):
            md_lines.append(f"### {fw['name']}\n\n")
            md_lines.append(f"**File**: `{fw['file']}` | **Version**: `{fw['version']}` | **Size**: ~{fw['character_count']} chars\n\n")
            md_lines.append(f"**Purpose**: {fw['purpose']}\n\n")
            md_lines.append(f"**Use Cases**: {fw['use_case']}\n\n")
            md_lines.append("---\n")
    
    return ''.join(md_lines)

def generate_comparison_table(base_dir: Path) -> str:
    """Generates a markdown comparison table of all frameworks.

    Args:
        base_dir (Path): The base directory of the repository.

    Returns:
        str: A markdown-formatted string containing the comparison table.
    """
    frameworks_dir = base_dir / 'frameworks'
    
    frameworks = []
    for yaml_file in sorted(frameworks_dir.glob('**/*.yml')):
        try:
            data = load_framework(yaml_file)
            if not data:
                continue
            frameworks.append({
                'name': data.get('name', yaml_file.stem),
                'category': yaml_file.parent.name.title(),
                'version': data.get('version', 'N/A'),
                'chars': data.get('documentation', {}).get('character_count', '?'),
            })
        except (yaml.YAMLError, FileNotFoundError) as e:
            print(f"Warning: Could not process {yaml_file} for comparison table: {e}")
            continue
    
    frameworks.sort(key=lambda x: (x['category'], x['name']))
    
    md_lines = [
        "# Framework Comparison Table\n\n",
        "| Framework | Category | Version | Size (chars) |\n",
        "|:----------|:---------|:--------|:-------------|\n"
    ]
    
    for fw in frameworks:
        md_lines.append(f"| {fw['name']} | {fw['category']} | `{fw['version']}` | {fw['chars']} |\n")
    
    return ''.join(md_lines)

def main() -> int:
    """Main function to generate all documentation files.

    This function coordinates the generation of the framework reference
    and comparison table, and saves them to the `docs/` directory.

    Returns:
        int: An exit code, 0 for success.
    """
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    print("Generating framework documentation...")
    
    try:
        # Generate and save the framework reference
        summary = generate_framework_summary(base_dir)
        summary_path = output_dir / 'FRAMEWORK_REFERENCE.md'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"✅ Generated: {summary_path}")

        # Generate and save the comparison table
        comparison = generate_comparison_table(base_dir)
        comparison_path = output_dir / 'FRAMEWORK_COMPARISON.md'
        with open(comparison_path, 'w', encoding='utf-8') as f:
            f.write(comparison)
        print(f"✅ Generated: {comparison_path}")

        print("\n✨ Documentation generation complete!")
        return 0
    except Exception as e:
        print(f"\n❌ An error occurred during documentation generation: {e}")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())