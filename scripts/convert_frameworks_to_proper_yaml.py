#!/usr/bin/env python3
"""Convert framework files from XML-in-strings to proper YAML nesting.

This script is designed to refactor legacy framework files that embed
an XML-like structure within a single 'content' string. It parses this
string and converts it into a native, nested YAML structure under a new
'structure' key.

The original XML-like content is preserved in a 'legacy_content' field
for reference, and the old 'content' key is removed. The script is
idempotent and will skip any files that it determines have already been
converted.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, List


def clean_text(text: str) -> str:
    """Cleans and normalizes a block of text.

    This function performs two main cleaning operations:
    1.  Reduces multiple consecutive newlines into a maximum of two.
    2.  Removes leading and trailing whitespace from each line.

    Args:
        text (str): The input string to clean.

    Returns:
        str: The cleaned and normalized string.
    """
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # Remove trailing/leading whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    return '\n'.join(lines).strip()


def parse_scratchpad_sections(content: str) -> List[str]:
    """Extracts scratchpad section names from a bracketed format.

    For example, from "[AttentionFocus: ...]", it extracts "AttentionFocus".

    Args:
        content (str): The string content containing bracketed sections.

    Returns:
        List[str]: A list of the extracted section names.
    """
    pattern = r'\[([^:]+):.*?\]'
    sections = re.findall(pattern, content)
    return [s.strip() for s in sections]


def parse_xml_to_yaml(content: str) -> Dict[str, Any]:
    """Recursively parses an XML-like string into a YAML structure.

    This function identifies XML-like tags (e.g., <role>...</role>) and
    converts them into key-value pairs in a dictionary. It handles
    nested tags, simple text content, and a special format for
    bracketed scratchpad sections.

    Args:
        content (str): The XML-like string to parse.

    Returns:
        Dict[str, Any]: A dictionary representing the structured data.
    """
    result = {}

    # Pattern to match XML-like tags (including tags with spaces)
    tag_pattern = r'<([^/>]+)>(.*?)</\1>'

    matches = re.findall(tag_pattern, content, re.DOTALL | re.IGNORECASE)

    if not matches:
        # No XML tags found, check for bracketed sections
        if '[' in content and ']' in content:
            sections = parse_scratchpad_sections(content)
            if sections:
                return {"sections": sections, "raw_format": clean_text(content)}
        return {"content": clean_text(content)}

    for tag_name, tag_content in matches:
        clean_tag = tag_name.strip().lower().replace(' ', '_')
        tag_content = tag_content.strip()

        # Check if content has nested tags for recursion
        if re.search(r'<[^/>]+>.*?</[^>]+>', tag_content, re.DOTALL):
            result[clean_tag] = parse_xml_to_yaml(tag_content)
        # Check for the special bracketed scratchpad format
        elif '[' in tag_content and ']:' in tag_content:
            sections = parse_scratchpad_sections(tag_content)
            instructions_match = re.search(r'^(.+?)```', tag_content, re.DOTALL)
            instructions = clean_text(instructions_match.group(1)) if instructions_match else None

            result[clean_tag] = {"format": "bracketed_sections", "sections": sections}
            if instructions:
                result[clean_tag]["usage"] = instructions
            result[clean_tag]["template"] = clean_text(tag_content)
        else:
            result[clean_tag] = clean_text(tag_content)

    # Handle any text content outside of the main tags
    remaining = re.sub(tag_pattern, '', content, flags=re.DOTALL).strip()
    remaining = re.sub(r'-{3,}', '', remaining).strip()
    remaining = clean_text(remaining)

    if remaining:
        result["instructions"] = remaining

    return result


def convert_framework(yaml_file: Path) -> bool:
    """Converts a single framework file to a structured YAML format.

    This function reads a framework file, checks if it needs conversion,
    parses the legacy 'content' field, and writes a new structured
    format back to the file.

    Args:
        yaml_file (Path): The path to the framework file to convert.

    Returns:
        bool: True if the file was converted, False if it was skipped.
    """
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or 'framework' not in data or 'content' not in data['framework']:
        return False

    if 'structure' in data['framework']:
        return False

    content = data['framework']['content']
    has_xml = re.search(r'<[^/>]+>.*?</[^>]+>', content, re.DOTALL)
    has_brackets = '[' in content and ']:' in content

    if not (has_xml or has_brackets):
        return False

    print(f"Converting: {yaml_file.name}")

    parsed_structure = parse_xml_to_yaml(content)

    data['framework']['structure'] = parsed_structure
    data['framework']['legacy_content'] = content
    del data['framework']['content']

    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120, indent=2)

    return True


def main() -> int:
    """Main entry point for the conversion script.

    Iterates through all YAML files in the `frameworks` directory,
    converts them if necessary, and prints a summary of the results.

    Returns:
        int: An exit code, 0 for success, 1 for failure.
    """
    frameworks_dir = Path(__file__).parent.parent / 'frameworks'

    if not frameworks_dir.is_dir():
        print(f"Error: Directory '{frameworks_dir}' not found.")
        return 1

    converted_count = 0
    skipped_count = 0

    for yaml_file in sorted(frameworks_dir.glob('**/*.yml')):
        try:
            if convert_framework(yaml_file):
                converted_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"Error converting {yaml_file.name}: {e}")

    print("\nConversion complete:")
    print(f"  Converted: {converted_count} files")
    print(f"  Skipped: {skipped_count} files")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())