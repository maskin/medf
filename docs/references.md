# MEDF Reference Tracking Specification

**Status:** Draft (v0.2.2 proposal)
**Created:** 2026-02-05
**Authors:** MEDF Project

---

## Abstract

This document specifies the reference tracking mechanism for MEDF, enabling blocks to cite other MEDF documents and blocks while maintaining offline-first operation.

---

## Design Principles

1. **Offline-first**: Reference resolution works without network access
2. **Optional online fetching**: Network requests only with explicit `--fetch` flag
3. **Local caching**: Fetched documents are cached for offline use
4. **Minimal coupling**: References are metadata, not validation requirements

---

## Schema Changes

### Block Reference Field

Each block MAY include a `references` array:

```json
{
  "block_id": "discussion",
  "role": "body",
  "format": "markdown",
  "text": "See MEDF: paper-2026-example#methodology for details",
  "references": [
    {
      "document_id": "paper-2026-example",
      "block_id": "methodology",
      "uri": "https://github.com/user/repo/blob/main/paper-2026-example.medf.json"
    }
  ]
}
```

**Reference object fields:**
- `document_id` (required): Document identifier
- `block_id` (required): Block identifier within document
- `uri` (optional): HTTPS URL or local file path

---

## Reference Resolution

### Resolution Order (Offline)

When resolving references without `--fetch`:

1. **Same directory** as referring document
2. **MEDF_PATH** environment variable (colon-separated paths)
3. **Local cache** (`~/.medf/cache/`)
4. **User-specified paths** (`--path` flag)

### Online Fetching (Optional)

With `--fetch` flag:
1. Attempt HTTPS GET request to `uri`
2. Fetch successful → Save to `~/.medf/cache/{document_id}.medf.json`
3. Cache hit → Use cached version (no network request)

---

## CLI Commands

### Resolve References

```bash
# Resolve all references in document
medf resolve document.medf.json

# Resolve references for specific block
medf resolve document.medf.json --block discussion

# Fetch remote references (explicit online)
medf resolve document.medf.json --block discussion --fetch

# List all references without resolving
medf resolve document.medf.json --list-all

# Specify custom search paths
medf resolve document.medf.json --path /path/to/medf/documents
```

### Output Format

**Human-readable (default):**
```
References for block: discussion

1. MEDF: paper-2026-example#methodology
   Status: ✓ Found (local)
   Path: ./paper-2026-example.medf.json
   Block hash: sha256:abc123...
```

**JSON (`--json` flag):**
```json
{
  "block_id": "discussion",
  "references": [
    {
      "document_id": "paper-2026-example",
      "block_id": "methodology",
      "status": "found",
      "location": "./paper-2026-example.medf.json",
      "block_hash": "sha256:abc123..."
    }
  ]
}
```

---

## Citation Format in Text

When citing MEDF documents in block text, use the following format:

```
MEDF: {document_id}#{block_id}
```

**Examples:**
- `MEDF: paper-2026-example#methodology`
- `MEDF: admin-guideline-2024#scope`
- `MEDF: philosophy#2-does-not-determine-correctness`

**Note:** Citation text is human-readable. Structured reference data in `references` array is for machine processing.

---

## Security Considerations

### Online Fetching

- **HTTPS required**: All URIs MUST use HTTPS
- **Certificate validation**: Standard TLS verification
- **No automatic fetching**: Requires explicit `--fetch` flag
- **Cache inspection**: Users can inspect cached files

### Reference Validation

- **References are metadata**: Document validity does NOT depend on reference resolution
- **No circular dependency checks**: Clients MAY detect cycles but MUST NOT fail
- **Trust boundaries**: Referenced documents have separate trust chains

---

## Implementation Notes

### Cache Structure

```
~/.medf/
├── cache/
│   ├── paper-2026-example.medf.json
│   ├── admin-guideline-2024.medf.json
│   └── ...
└── config.json (optional, for custom paths)
```

### Environment Variables

```bash
# Set search paths for reference resolution
export MEDF_PATH="/path/to/docs:/another/path"

# Set custom cache directory
export MEDF_CACHE="/custom/cache/path"
```

---

## Examples

### Example 1: Local References

**Document A (`paper-a.medf.json`):**
```json
{
  "medf_version": "0.2.2",
  "id": "paper-a",
  "blocks": [
    {
      "block_id": "conclusion",
      "text": "See MEDF: paper-b#results",
      "references": [
        {
          "document_id": "paper-b",
          "block_id": "results",
          "uri": "./paper-b.medf.json"
        }
      ]
    }
  ]
}
```

**Resolution:**
```bash
$ medf resolve paper-a.medf.json --block conclusion
References for block: conclusion

1. MEDF: paper-b#results
   Status: ✓ Found (local)
   Path: ./paper-b.medf.json
   Block hash: sha256:def456...
```

### Example 2: Remote References with Fetch

**Document with remote reference:**
```json
{
  "references": [
    {
      "document_id": "external-spec",
      "block_id": "requirements",
      "uri": "https://github.com/org/specs/blob/main/external-spec.medf.json"
    }
  ]
}
```

**Resolution with fetch:**
```bash
$ medf resolve document.medf.json --fetch --block analysis
Fetching: https://github.com/org/specs/blob/main/external-spec.medf.json
Cached to: ~/.medf/cache/external-spec.medf.json

References for block: analysis

1. MEDF: external-spec#requirements
   Status: ✓ Found (fetched)
   Cached: ~/.medf/cache/external-spec.medf.json
   Block hash: sha256:789abc...
```

---

## Open Questions

1. **Version-specific references**: Should references specify `medf_version`?
   - Proposal: Optional, for compatibility checks

2. **Reference types**: Should we distinguish between "cites", "extends", "replaces"?
   - Proposal: Keep simple for v0.2.2, add `reference_type` in future

3. **Batch resolution**: Should we support resolving multiple documents at once?
   - Proposal: Not needed for MVP, shell scripting can handle it

4. **Reference integrity**: Should pack/verify check reference existence?
   - Proposal: NO. References are metadata, not validation requirements

---

## Future Enhancements

- **Reference graphs**: Visualize document dependency networks
- **Transitive closure**: Resolve all indirect references
- **Reference updates**: Update reference URIs in bulk
- **Reference signing**: Sign reference assertions separately

---

## Changelog

### v0.2.2 (Draft)
- Initial reference tracking specification
- Offline-first resolution with optional online fetching
- `medf resolve` command proposal
