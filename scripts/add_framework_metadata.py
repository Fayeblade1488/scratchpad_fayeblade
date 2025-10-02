#!/usr/bin/env python3
"""Framework Metadata Generator.

This script intelligently generates and adds missing metadata to framework
YAML files. It uses a template-based approach for known frameworks and
generates generic metadata for unknown ones. The script can be run
repeatedly and will only modify files that are missing required
metadata fields (`purpose`, `use_case`, `version`).

Author: Warp AI Agent
Date: 2025-10-01
"""

import yaml
from pathlib import Path

# Metadata templates based on framework patterns
METADATA_TEMPLATES = {
    # Core frameworks
    'scratchpad-2.5': {
        'purpose': 'Structured AI reasoning framework with comprehensive cognitive operations',
        'use_case': 'Complex reasoning tasks requiring detailed analysis, synthesis, and metacognition',
        'version': '2.5'
    },
    'scratchpad-2.6': {
        'purpose': 'Enhanced reasoning framework with improved attention management and pathway clarity',
        'use_case': 'Advanced problem-solving, strategic planning, research analysis',
        'version': '2.6'
    },
    'scratchpad-2.7': {
        'purpose': 'Latest comprehensive scratchpad framework with optimized cognitive workflow',
        'use_case': 'High-complexity tasks requiring systematic reasoning, quality validation, and exploration',
        'version': '2.7'
    },
    'scratchpad-lite': {
        'purpose': 'Lightweight reasoning framework optimized for character-constrained environments',
        'use_case': 'Quick tasks in Comet Browser or similar character-limited platforms',
        'version': '1.0'
    },
    'scratchpad-concise': {
        'purpose': 'Minimal scratchpad framework focusing on essential reasoning steps only',
        'use_case': 'Simple queries requiring structured thinking without extensive metacognition',
        'version': '1.0'
    },
    'scratchpad-think': {
        'purpose': 'Thinking-focused framework emphasizing deliberate cognitive processes',
        'use_case': 'Deep analytical tasks requiring explicit thought articulation',
        'version': '1.0'
    },
    'pplx-profile': {
        'purpose': 'Scratchpad framework optimized for Perplexity AI platform constraints',
        'use_case': 'Research queries on Perplexity requiring structured reasoning within platform limits',
        'version': '1.0'
    },
    
    # Purpose-built frameworks
    'deep-researcher': {
        'purpose': 'Systematic research framework for thorough investigation and source analysis',
        'use_case': 'Academic research, literature reviews, comprehensive topic exploration',
        'version': '1.0'
    },
    'deeper-research': {
        'purpose': 'Advanced research framework with enhanced depth and source validation',
        'use_case': 'Complex research projects requiring rigorous methodology and citation tracking',
        'version': '1.0'
    },
    'emotional-intelligence': {
        'purpose': 'Framework emphasizing emotional awareness, empathy, and nuanced human interaction',
        'use_case': 'Counseling scenarios, interpersonal communication, emotional support contexts',
        'version': '1.0'
    },
    'planning-13': {
        'purpose': 'Structured planning framework with 13-step systematic approach',
        'use_case': 'Project planning, strategic initiatives, complex task decomposition',
        'version': '1.3'
    },
    'novelize-review': {
        'purpose': 'Literary analysis framework for narrative structure and storytelling evaluation',
        'use_case': 'Novel critique, creative writing feedback, narrative arc analysis',
        'version': '1.0'
    },
    'saganpad': {
        'purpose': 'Science communication framework inspired by Carl Sagan\'s accessible style',
        'use_case': 'Explaining complex scientific concepts to general audiences',
        'version': '1.0'
    },
    'unified-conscious': {
        'purpose': 'Holistic framework integrating multiple cognitive and awareness dimensions',
        'use_case': 'Philosophical inquiry, consciousness exploration, integrated thinking',
        'version': '1.0'
    },
    'sonnet-thinking': {
        'purpose': 'Reasoning framework optimized for Claude Sonnet model capabilities',
        'use_case': 'Complex reasoning tasks leveraging Sonnet\'s strengths in analysis and synthesis',
        'version': '1.0'
    },
    'gemini-cli': {
        'purpose': 'Command-line optimized framework for Gemini API interactions',
        'use_case': 'Terminal-based workflows, scripting, automated Gemini API calls',
        'version': '1.0'
    },
    'flow-gpt5': {
        'purpose': 'Framework designed for fluid, conversational reasoning with GPT-5 architecture',
        'use_case': 'Natural dialogue-based problem solving, iterative refinement conversations',
        'version': '5.0'
    },
    'game-design-gabg': {
        'purpose': 'Game design framework for mechanics, balance, and gameplay analysis',
        'use_case': 'Game development, mechanics design, player experience optimization',
        'version': '1.0'
    },
    'nlm-extended': {
        'purpose': 'Extended natural language modeling framework with enhanced linguistic analysis',
        'use_case': 'NLP tasks, linguistic research, language model evaluation',
        'version': '1.0'
    },
    'nlm-framework-500': {
        'purpose': 'Compact NLM framework optimized for 500-word constraint environments',
        'use_case': 'Brief linguistic analysis, summarization, constrained NLP tasks',
        'version': '1.0'
    },
    'human-condition-benchmark': {
        'purpose': 'Framework for evaluating AI understanding of human experiences and conditions',
        'use_case': 'Ethics evaluation, empathy testing, human-centered AI assessment',
        'version': '1.0'
    },
    'podsynth': {
        'purpose': 'Podcast synthesis framework for audio content analysis and summarization',
        'use_case': 'Podcast production, audio content strategy, episode planning',
        'version': '1.0'
    },
}

def add_metadata_to_framework(yaml_path):
    """Adds or updates metadata for a single framework YAML file.

    This function reads a YAML file, checks for the presence of `purpose`,
    `use_case`, and `version` metadata, and adds them if they are missing.
    It uses a predefined template if the filename matches, otherwise it
    generates generic metadata.

    Args:
        yaml_path (Path): The path object pointing to the YAML framework file.

    Returns:
        bool: True if the file was modified, False otherwise.

    Raises:
        yaml.YAMLError: If the YAML file is malformed and cannot be parsed.
        IOError: If there is an error reading or writing the file.
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Guard against empty or invalid YAML files
    if not data:
        data = {}
    
    filename = yaml_path.stem
    
    # Find a matching template or create a generic one
    template = None
    for key, meta in METADATA_TEMPLATES.items():
        if key in filename:
            template = meta
            break
    
    if not template:
        category = yaml_path.parent.name
        template = {
            'purpose': f'{filename.replace("-", " ").title()} framework for specialized AI reasoning',
            'use_case': f'{category.replace("-", " ").title()} tasks requiring structured cognitive approach',
            'version': '1.0'
        }
    
    changed = False
    doc = data.get('documentation', {})
    
    if not doc.get('purpose'):
        doc['purpose'] = template['purpose']
        changed = True
    
    if not doc.get('use_case'):
        doc['use_case'] = template['use_case']
        changed = True
    
    if not data.get('version') or not str(data.get('version')).strip():
        data['version'] = template['version']
        changed = True
    
    if changed:
        data['documentation'] = doc
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return True
    
    return False

def main():
    """Main function to process all framework files in the repository.

    This function locates the 'frameworks' directory, iterates through all
    '.yml' files, and calls `add_metadata_to_framework` for each one.
    It prints a summary of the number of files updated and skipped.

    Returns:
        int: An exit code, 0 for success.
    """
    import os
    base_dir = Path(os.getenv('SCRATCHPAD_DIR', Path(__file__).parent.parent))
    frameworks_dir = base_dir / 'frameworks'
    
    updated_count = 0
    skipped_count = 0
    
    print("Adding metadata to frameworks...")
    print()
    
    for yaml_file in sorted(frameworks_dir.glob('**/*.yml')):
        try:
            if add_metadata_to_framework(yaml_file):
                print(f"✅ Updated: {yaml_file.name}")
                updated_count += 1
            else:
                print(f"⏭️  Skipped: {yaml_file.name} (already complete)")
                skipped_count += 1
        except (IOError, yaml.YAMLError) as e:
            print(f"❌ Error processing {yaml_file.name}: {e}")

    print()
    print(f"✨ Complete! Updated {updated_count} files, skipped {skipped_count}")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
