# Block ID Guidelines

Block IDs are identifiers used for reference, citation,
and version continuity.

MEDF does not require block IDs to be persistent,
but strongly recommends explicit and stable IDs
for long-lived or versioned documents.

---

## What is a Block ID?

A block ID uniquely identifies a semantic unit within a MEDF document:

```json
{
  "block_id": "introduction",
  "role": "body",
  "format": "markdown",
  "text": "This is the introduction..."
}
```

Block IDs enable:
- **Precise citation**: `MEDF: paper-2026-xyz#introduction`
- **Version continuity**: Track blocks across document versions
- **Referential integrity**: Link to specific content without ambiguity

---

## Best Practices

### 1. Use Descriptive IDs

✅ **Good**:
```json
"block_id": "methodology"
"block_id": "results-discussion"
"block_id": "appendix-statistics"
```

❌ **Avoid**:
```json
"block_id": "block-1"
"block_id": "abc123"
"block_id": "7d8f3a2b"
```

### 2. Be Stable Across Versions

When updating a document:
- ✅ **Keep** the same `block_id` for semantically identical content
- ❌ **Don't change** `block_id` just because text was edited

Example:

**Version 1**:
```json
{
  "block_id": "introduction",
  "text": "This paper introduces..."
}
```

**Version 2** (text edited):
```json
{
  "block_id": "introduction",
  "text": "This paper presents an introduction to..."  // Edited
}
```

### 3. Use Hierarchical Naming for Complex Documents

For large documents with nested sections:

```json
{
  "block_id": "sec-1-intro",
  "role": "body",
  "text": "..."
}

{
  "block_id": "sec-1-1-background",
  "role": "body",
  "text": "..."
}

{
  "block_id": "sec-1-1-1-motivation",
  "role": "body",
  "text": "..."
}
```

### 4. Consider Citation Format

Block IDs will appear in citations like:

```
MEDF: document-id#block-id
```

Choose IDs that:
- Are readable in plain text
- Work well in URLs
- Are memorable for humans

---

## When to Use Block IDs

### Recommended For:
- ✅ Academic papers (sections, figures, tables)
- ✅ Technical specifications (requirements, clauses)
- ✅ Legal documents (articles, provisions)
- ✅ Versioned documents (tracking across revisions)
- ✅ Long-form content (chapters, sections)

### Optional For:
- 🔹 Short documents (< 5 blocks)
- 🔹 Temporary or ephemeral content
- 🔹 Internal drafts (before publication)

### Not Required For:
- ❌ Simple sequential content
- ❌ Single-block documents

---

## Technical Notes

### Uniqueness Scope

Block IDs MUST be unique **within a document**.
The same block ID MAY be reused across different documents.

Example:
- `doc-A.json` has `block_id: "introduction"`
- `doc-B.json` also has `block_id: "introduction"`
- ✅ This is allowed

### Character Set

Block IDs are strings. Recommended characters:
- Lowercase letters (a-z)
- Numbers (0-9)
- Hyphens (-)
- Underscores (_)

Avoid spaces and special characters.

### Length

No strict limit, but recommended:
- **Minimum**: 3 characters
- **Typical**: 5-20 characters
- **Maximum**: 64 characters (practical usability)

---

## CLI Usage Note

When using the MEDF CLI, stable block IDs are recommended for versioned documents:

```bash
# Verify document with stable block IDs
python3 medf.py verify document.medf.json

# Sign document (block IDs included in hash)
python3 medf.py sign document.medf.json --key private.key
```
