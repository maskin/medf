# MeDF

**Mutable Expression Description Format**

MeDF stands for **Mutable Expression Description Format**.

A document format where canonical meaning is fixed,
while expressions remain mutable.

> "Records *when, who, and with what intent* a document existed"

---

## Overview

MeDF is not a system for preserving or distributing documents themselves. It is a format for **describing the state** that "a document existed at a certain point in time, with certain intent."

- ✅ **Records existence** - when, who, and intent
- ✅ **Fixes state** - immutability through hashing
- ✅ **Offline-first** - no central servers required
- ❌ **Does not prove correctness** - no truth judgment

**Works fully offline and does not require trust, servers, or blockchains.**

---

## Immutable vs Mutable Layers

**Core Principle**: MeDF guarantees immutability of text and meaning, while allowing mutable presentation and interpretation layers on top of a verifiable core.

### Immutable Layer (Verifiable)

The following are **immutable once signed and verified**:

- ✅ **Text** - Semantic content in `blocks[].text` (Markdown)
- ✅ **Structure** - Block order, IDs, and relationships
- ✅ **Meaning** - The canonical semantic information

### Mutable Layer (Non-verifiable)

The following are **mutable and not part of hash verification**:

- ✅ **Presentation** - Visual styling, layout, rendering
- ✅ **Indexing** - Table of contents, navigation, metadata
- ✅ **Views** - Different interpretations, formats, or UIs
- ✅ **Extensions** - Custom fields for application-specific use

**Key Distinction**: The term "Mutable Expression" refers not to the text itself, but to its presentation, rendering, indexing, and interpretation layers, which may change without affecting document integrity.

> "In MEDF, text is immutable, structure is immutable, meaning is immutable. Expression is mutable, presentation is mutable, views are mutable."

---

## Quick Start

```bash
# Show template
python3 medf.py init

# Calculate hashes
python3 medf.py hash document.medf.json

# Verify integrity
python3 medf.py verify document.medf.json

# Sign (optional)
python3 medf.py sign document.medf.json --key private.key
```

---

## Structure

```json
{
  "medf_version": "0.2.1",
  "id": "document-id",
  "snapshot": "2026-02-05T10:00:00Z",
  "issuer": "issuer-code",
  "blocks": [
    {
      "block_id": "introduction",
      "role": "body",
      "format": "markdown",
      "text": "...",
      "block_hash": "sha256:..."
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": "..."
  }
}
```

- **blocks** - Minimal semantic units
- **block_hash** - Hash for each block
- **doc_hash** - Hash for entire document

**Note on Markdown**: `blocks[].text` uses Markdown as a semantic markup language. It is treated as part of the immutable, verifiable content. Visual styling, layout, and rendering decisions are explicitly out of scope for MeDF and are considered mutable presentation layers.

---

## Canonicalization (RFC 8785)

MeDF adopts **RFC 8785 (JSON Canonicalization Scheme - JCS)** as its normative canonicalization standard.

**Key Points**:
- ✅ No custom canonicalization rules defined
- ✅ All hashes computed over RFC 8785–canonicalized JSON
- ✅ Ensures interoperable and implementation-independent verification
- ✅ Works offline without external dependencies

> "MeDF does not define its own canonicalization rules. It normatively adopts RFC 8785 to ensure interoperable and implementation-independent verification."

---

## Citation Format

```
MEDF: paper-2026-example#methodology
```

- `paper-2026-example` - Document ID
- `#methodology` - Block ID

---

## Philosophy

**Core Principles** (see [PHILOSOPHY.md](PHILOSOPHY.md) / [思想.md](思想.md)):

1. **Does not judge correctness** - MeDF does not determine truth, evaluate content, grant authority, or decide superiority
2. **Records "when/who/intent existed"** - Not "is this correct?" but "when/who/with what intent did this exist?"
3. **Hash as responsibility boundary** - Hash proves "unchanged from this state," not trust or legitimacy
4. **History as chains** - Each state linked by `previous`, branching allowed, no "official" history
5. **Offline-first** - No network, central servers, or external APIs required
6. **JSON as compromise** - Human-readable, machine-processable, CLI-generatable, future-convertible
7. **No forced trust** - Records "who fixed this," not "this is trustworthy"

### Q&A (Philosophy Defense)

**Q: Is this blockchain?**
A: No. No consensus or distribution required. MeDF is a state description format; distributed consensus is optional.

**Q: Can't I trust this?**
A: We operate on a no-trust premise. Trustworthiness is an external concern. MeDF records "what existed."

**Q: Weak authentication?**
A: We don't authenticate. We only fix state. Signatures show "who fixed," not content correctness.

**Q: Wouldn't central management be more convenient?**
A: We prioritize resilience over convenience. Central servers are single points of failure. Offline operation is essential for long-term document preservation.

### AI-Generated Documents

**Position**: MeDF provides verifiable document state regardless of creation method (AI or human).

> "The problem is not 'AI wrote this' — the essence is 'provenance and responsibility cannot be verified'"

See [docs/ai-generated-documents.md](docs/ai-generated-documents.en.md) for complete position statement on AI-generated documents.

---

## Use Cases

- **Academic papers**: Section-level reference (`MEDF: paper-2026-xyz#methodology`)
- **Public documents**: Revision history tracking
- **Impersonation prevention**: Proving "same person" through key continuity
- **Signing**: Claim of "I fixed this" (not trust)
- **AI-generated documents**: Verifiable AI-assisted writing - see [docs/ai-generated-documents.md](docs/ai-generated-documents.en.md)

---

## CLI Reference

```bash
# Show template
python3 medf.py init

# Calculate hashes
python3 medf.py hash document.medf.json

# Verify document integrity
python3 medf.py verify document.medf.json

# Sign document (optional)
python3 medf.py sign document.medf.json --key private.key
```

---

## Specification

- **Philosophy**: [PHILOSOPHY.md](PHILOSOPHY.md) / [思想.md](思想.md)
- **AI-Generated Documents**: [docs/ai-generated-documents.md](docs/ai-generated-documents.en.md) / [docs/ai-generated-documents.md](docs/ai-generated-documents.md)
- **Schema**: [spec/medf.schema.json](spec/medf.schema.json)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **License**: [LICENSE](LICENSE)

---

## License

MIT License - [LICENSE](LICENSE)

**"No forced trust | No central control | No fork fear"** - Fully aligned with MeDF philosophy

---

## Related

- **v0.2**: Public document specification (JSON-embedded)
- **v0.1**: Minimal structure (external reference)

---

## Links

- GitHub: https://github.com/maskin/medf
- Schema: [spec/medf.schema.json](spec/medf.schema.json)
