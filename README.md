# The Scratchpad Framework
<img width="1536" height="1024" alt="483854870-514bd1e1-6ef5-4403-8d0a-441881c5217e" src="https://github.com/user-attachments/assets/d1032a2e-d001-4be8-b57f-803e82218dea" />

![Tests](https://img.shields.io/badge/tests-15/15_passing-brightgreen)
![Bugs](https://img.shields.io/badge/bugs-0_known-brightgreen)
![YAML](https://img.shields.io/badge/YAML-1.2.2_compliant-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

**Advanced AI Reasoning Templates for Comet Browser**

---

## Overview

The Scratchpad Framework is a curated collection of **AI reasoning templates** designed to transform how AI assistants think and respond. All frameworks are in clean YAML format, optimized for Comet Browser's character limits.

## Repository Structure

```
scratchpad/
├── frameworks/
│   ├── core/              # 10 general-purpose reasoning templates
│   ├── purpose-built/     # 18 task-specific frameworks
│   └── personas/          # 2 AI assistant personalities
├── docs/                  # Documentation and guides
├── scripts/               # Utility scripts
├── assets/showcase/       # Screenshots and demos
├── tests/                 # Validation test suite
├── README.md             # This file
└── license.txt           # MIT License
```

## Quick Start
1. **Choose a framework** from the `frameworks/` directory.
2. **Understand the structure**: Each file contains a structured YAML prompt with defined steps and rules.
3. **Integrate with your tools**: Parse the YAML and use the structured data to guide your AI's reasoning process.
4. **Enjoy structured, transparent AI reasoning!**

## Framework Categories

### Core Frameworks (10)
- `scratchpad-lite.yml` - Lightweight, 3-step reasoning
- `scratchpad-2.6.yml` - Comprehensive 11-step analysis
- `scratchpad-2.7.yml` - Deep, multi-faceted reasoning
- `scratchpad-concise.yml` - Short, to-the-point answers
- `scratchpad-think.yml` - Metacognitive verbalization
- Plus 5 more variants...

### Purpose-Built Frameworks (18)
- `deep-researcher.yml` - Research and investigation
- `game-design-gabg.yml` - Game design planning
- `emotional-intelligence.yml` - Emotion-aware responses
- `podsynth-clean.yml` - Podcast script generation
- Plus 14 more specialized frameworks...

### Persona Frameworks (8)
- `gilfoyle-bot.yml` - Systems architecture expertise (cynical tone)
- `anton-bot.yml` - Browser automation specialist
- `debug-detective.yml` - Systematic problem-solver
- `gemini-2.5.yaml` - Advanced, multi-modal AI persona
- Plus 4 more...

## Technical Details
- **Format:** 100% structured YAML. No more XML-in-YAML.
- **Schema**: All frameworks conform to a strict JSON Schema (`schemas/prompt_framework.schema.json`).
- **Parsing**: Easily parsable with any standard YAML library.
- **Validation:** 100% YAML syntax passing and schema validation.
- **Testing:** Comprehensive test suite included.

## Testing
```bash
python3 tests/test_yaml_frameworks.py
```

## License
MIT License - Free for commercial and personal use.

## Project Overview
- **30 frameworks** persona and framework rework
- **70% file reduction** (240 → 73 files)
- **19% size reduction** (149MB → 121MB)
- **100% YAML validation** passing

---

## Credits and Mentions 
- Orignal repo and author: https://github.com/para-droid-ai/scratchpad
- Discord with information: https://discord.gg/mmbQG63U
- OP of scratch-Pad: https://github.com/para-droid-ai
- Fayeblade Repo Author: https://github.com/Fayeblade1488

**Version 3.0 (October 2025)** - Major refactoring and YAML conversion complete.
