---
name: skill-seekers
description: Automatically convert documentation websites, GitHub repositories, and PDF files into Claude AI skills with conflict detection. Use this skill when users want to create skills from existing documentation, scrape technical docs, convert repos to skills, or process PDFs into structured knowledge.
---

# Skill Seekers

**Version:** v2.1.1 (Production Ready)  
**Source:** [GitHub Repository](https://github.com/yusufkaraaslan/Skill_Seekers)  
**PyPI:** `pip install skill-seekers`

## Overview

Skill Seekers is an automated tool that transforms documentation websites, GitHub repositories, and PDF files into production-ready Claude AI skills. Instead of manually reading and summarizing documentation, Skill Seekers:

1. **Scrapes multiple sources** (docs, GitHub repos, PDFs) automatically
2. **Analyzes code repositories** with deep AST parsing
3. **Detects conflicts** between documentation and code implementation
4. **Organizes content** into categorized reference files
5. **Enhances with AI** to extract best examples and key concepts
6. **Packages everything** into an uploadable .zip file for Claude

## When to Use This Skill

- Convert documentation websites into Claude skills
- Create skills from GitHub repositories
- Process PDF documentation into structured knowledge
- Combine multiple sources (docs + code + PDFs) into unified skills
- Detect discrepancies between documentation and implementation

**Trigger Keywords:**
```
scrape documentation, convert repo to skill, create skill from docs,
PDF to skill, skill seekers, unified scraping, conflict detection,
documentation scraper, 文档转 skill, 创建技能
```

## Quick Start

### Installation

```bash
# Option 1: Install from PyPI (Recommended)
pip install skill-seekers

# Option 2: Clone this repository (already done)
cd skills/skill-seekers
pip install -e .
```

### Basic Usage

```bash
# Single-source scraping (documentation only)
skill-seekers scrape --config configs/react.json
skill-seekers scrape --config configs/godot.json

# Unified multi-source scraping (docs + GitHub + PDF)
skill-seekers unified --config configs/react_unified.json

# Package the skill
skill-seekers package output/react/
```

## Core Capabilities

### 1. Documentation Scraping

```bash
# Estimate pages before scraping
skill-seekers estimate configs/react.json

# Scrape with local AI enhancement
skill-seekers scrape --config configs/react.json --enhance-local

# Async mode (2-3x faster)
skill-seekers scrape --config configs/react.json --async --workers 8
```

### 2. GitHub Repository Analysis

```bash
# Scrape a GitHub repository
skill-seekers github --repo facebook/react

# Analyze local repository
skill-seekers github --local-repo /path/to/project
```

### 3. PDF Processing

```bash
# Convert PDF to skill
skill-seekers pdf --file docs/manual.pdf --name my-manual
```

### 4. Unified Multi-Source (NEW v2.0.0)

```bash
# Combine docs + GitHub + PDF with conflict detection
skill-seekers unified --config configs/react_unified.json

# Output shows conflicts between documentation and implementation
```

**What makes unified special:**
- ✅ Detects discrepancies between documentation and code
- ✅ Shows both versions side-by-side with ⚠️ warnings
- ✅ Identifies outdated docs and undocumented features
- ✅ Single source of truth showing intent (docs) AND reality (code)

## Available Preset Configs (24 Total)

### Web Frameworks
- `react.json` - React
- `vue.json` - Vue.js
- `django.json` - Django
- `fastapi.json` - FastAPI
- `laravel.json` - Laravel
- `astro.json` - Astro
- `hono.json` - Hono

### Game Engines
- `godot.json` - Godot Engine
- `godot-large-example.json` - Godot (large docs)

### DevOps
- `kubernetes.json` - Kubernetes
- `ansible-core.json` - Ansible Core

### CSS Frameworks
- `tailwind.json` - Tailwind CSS

### Unified Configs (Multi-Source)
- `react_unified.json` - React (docs + GitHub)
- `django_unified.json` - Django (docs + GitHub)
- `fastapi_unified.json` - FastAPI (docs + GitHub)
- `godot_unified.json` - Godot (docs + GitHub)

## Creating Custom Configs

### Interactive Mode

```bash
skill-seekers scrape --interactive
```

### Manual Configuration

Create a JSON config file:

```json
{
  "name": "myframework",
  "description": "When to use this skill",
  "base_url": "https://docs.myframework.org/",
  "selectors": {
    "main_content": "article",
    "title": "title",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": [],
    "exclude": ["/search", "/_static/"]
  },
  "categories": {
    "getting_started": ["introduction", "quickstart"],
    "api": ["api", "reference"]
  },
  "rate_limit": 0.5,
  "max_pages": 500
}
```

## Performance

| Task | Time | Notes |
|------|------|-------|
| Scraping | 15-45 min | First time only |
| Building | 1-3 min | Fast! |
| Re-building | <1 min | With --skip-scrape |
| Enhancement (LOCAL) | 30-60 sec | Uses Claude Code Max |
| Packaging | 5-10 sec | Final zip |

**Async Mode Performance:**
- Sync: ~18 pages/sec, 120 MB memory
- Async: ~55 pages/sec, 40 MB memory (3x faster!)

## MCP Integration

This tool includes an MCP server with 9 tools:

- `list_configs` - List available preset configurations
- `generate_config` - Generate a new config file
- `validate_config` - Validate config structure
- `estimate_pages` - Estimate page count before scraping
- `scrape_docs` - Scrape and build a skill
- `package_skill` - Package skill into .zip file
- `upload_skill` - Upload .zip to Claude
- `split_config` - Split large documentation configs
- `generate_router` - Generate router/hub skills

**Setup:**
```bash
./setup_mcp.sh
```

## Directory Structure

```
skill-seekers/
├── src/skill_seekers/
│   ├── cli/                    # CLI tools
│   │   ├── doc_scraper.py      # Main scraper
│   │   ├── github_scraper.py   # GitHub scraper
│   │   ├── pdf_scraper.py      # PDF scraper
│   │   ├── unified_scraper.py  # Unified multi-source
│   │   ├── conflict_detector.py # Conflict detection
│   │   └── package_skill.py    # Packager
│   └── mcp/
│       └── server.py           # MCP server
├── configs/                    # 24 preset configs
├── docs/                       # Documentation
└── output/                     # Generated skills (git-ignored)
```

## Troubleshooting

### No Content Extracted
Check `main_content` selector in config. Common selectors:
- `article`
- `main`
- `div[role="main"]`
- `div.content`

### Poor Categorization
Edit `categories` section with better keywords:
```bash
cat output/myframework_data/summary.json | grep url | head -20
```

### Force Re-scrape
```bash
rm -rf output/myframework_data/
skill-seekers scrape --config configs/myframework.json
```

## Resources

- **Full Documentation:** See `CLAUDE.md`, `README.md` in this directory
- **Quick Start Guide:** `QUICKSTART.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`
- **Changelog:** `CHANGELOG.md`
- **MCP Setup:** `docs/MCP_SETUP.md`
