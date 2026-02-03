# MeDF (Meaning-anchored Document Format)

A document format for stable, meaning-based citation and reuse of documents.

## Overview

MeDF provides a way to reference documents by their **meaning and state** rather than their URL location. This enables:

- **Long-term reference stability**: Documents can be referenced even if the original URL changes
- **Content integrity**: Hash-based verification ensures documents haven't been tampered with
- **Snapshot reference**: Reference a specific point-in-time version of a document
- **AI-friendly format**: Structured JSON + Markdown for easy machine processing

## Key Concepts

### ID@timestamp Format

v0.2 introduces the `ID@timestamp` format for document identifiers:

```
JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z
```

- **ID**: Semantic identity (`JP-MLIT-2026-GUIDE-001`)
- **@timestamp**: Snapshot point (`2026-02-04T10:00:00Z`)

### Citation Example

> 国土交通省『持続可能な観光推進ガイドライン』
> MeDF: JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z

This citation works regardless of where the file is stored (URL, local, mirror).

## Project Structure

```
mdf/
├── cli/
│   ├── __init__.py
│   └── medf.py              # CLI tool
├── schema/
│   ├── medf-v0.1.schema.json
│   └── medf-v0.2-public.schema.json
├── examples/
│   ├── tourism-policy-2024-03.medf
│   └── JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z.medf
└── README.md
```

## Installation

### Requirements

```bash
pip install markdown jsonschema
```

## CLI Usage

### Convert Markdown to MeDF

```bash
python cli/medf.py convert input.md output.medf \
  --id "JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z" \
  --authority "国土交通省" \
  --type guideline \
  --version 0.2
```

#### Options

- `--id`: Document ID (required, use ID@timestamp format for v0.2)
- `--authority`: Authority name or JSON object with name, code, department
- `--type`: Document type (public_notice, guideline, press_release, report, white_paper, official_statement)
- `--version`: MeDF version (0.1 or 0.2, default: 0.2)
- `--snapshot`: Snapshot timestamp (ISO 8601, auto-generated if not provided)
- `--reference`: Reference URI (can be used multiple times)

### Validate MeDF File

```bash
python cli/medf.py validate file.medf --version 0.2
```

### Convert MeDF to HTML

```bash
python cli/medf.py to-html input.medf output.html
```

### Calculate Hash

```bash
python cli/medf.py hash file.medf
```

### Verify Hash

```bash
python cli/medf.py verify file.medf --version 0.2
```

## MeDF File Format

### v0.2 Structure

```json
{
  "medf_version": "0.2",
  "document_type": "guideline",
  "id": "JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z",
  "snapshot": "2026-02-04T10:00:00Z",
  "hash": {
    "algorithm": "sha-256",
    "value": "..."
  },
  "authority": {
    "name": "国土交通省",
    "code": "JP-MLIT",
    "department": "観光庁"
  },
  "content": "# Markdown content here...",
  "index": {
    "title": "...",
    "summary": {
      "short": "...",
      "medium": "...",
      "full": "..."
    },
    "sections": [...],
    "tags": [...],
    "keywords": [...]
  },
  "references": [...],
  "extensions": {}
}
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `medf_version` | Yes | MeDF format version (e.g., "0.2") |
| `document_type` | Yes (v0.2) | Type of public document |
| `id` | Yes | Document identifier (ID@timestamp for v0.2) |
| `snapshot` | Yes | Snapshot timestamp in ISO 8601 format |
| `hash` | Yes | Hash object with algorithm and value |
| `authority` | Yes | Authority object with name, code, department |
| `content` | Yes | Main content in Markdown format |
| `index` | No | Index with title, summary, sections, tags, keywords |
| `references` | No | Array of reference objects |
| `signature` | No | JWS signature object (for official documents) |
| `extensions` | No | Custom extension fields |

## Markdown Extensions

### Section Blocks

```markdown
```medf-section
id: executive-summary
role: executive_summary
```

# Section Title

Content...
```
```

### Reference Blocks

```markdown
:::reference{uri="https://example.com/doc"}
Reference description...
:::
```

### Note Blocks

```markdown
:::note{type=background}
Note content...
:::
```

## Hash Calculation

The hash is calculated from the following fields (in canonical JSON form):

- `id`
- `snapshot`
- `authority` (as JSON string)
- `content`
- `index` (as JSON string, if present)
- `references` (as JSON string, if present)

**Excluded from hash:**
- `medf_version` (version information)
- `hash` field itself
- `signature` field
- `extensions` field

## Document Types (v0.2)

- `public_notice`: Official announcements
- `guideline`: Guidelines and manuals
- `press_release`: Press releases
- `report`: Reports and studies
- `white_paper`: White papers
- `official_statement`: Official statements

## Schema Validation

JSON Schemas are provided for validation:

- `schema/medf-v0.1.schema.json`: v0.1 schema
- `schema/medf-v0.2-public.schema.json`: v0.2 public document schema

## License

MIT License

## Contributing

Contributions are welcome! Please submit issues and pull requests.
