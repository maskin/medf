# MeDF — Mutable Expression Description Format

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![medf_version](https://img.shields.io/badge/medf-0.2.1-blue)](spec/medf.schema.json)

**TL;DR**: Verifiable documents with immutable text and flexible presentation. For researchers, developers, and anyone who needs citable, tamper-evident content.

MEDF is a document format designed to make text verifiable
while allowing flexible presentation and reuse.

Text content is immutable.
Expression, layout, indexing, and interpretation are mutable.

MEDF focuses on integrity and referenceability —
not authority, correctness, or trust.

---

## Concept

MEDF separates immutable text from mutable presentation.

```
+---------------------------+
|        MEDF Document      |
+---------------------------+
|  Immutable Text Blocks    |  ← hashed & verifiable
|  ----------------------  |
|  block: executive_summary |
|  block: policy            |
|  block: appendix          |
+---------------------------+
|  Mutable Presentation     |  ← free to change
|  ----------------------  |
|  rendering (HTML/PDF)     |
|  indexing / TOC           |
|  layout / styling         |
+---------------------------+
```

Only the text blocks are part of the cryptographic identity.
Everything else can evolve without breaking verification.

---

## Overview

MeDF is not a system for preserving or distributing documents themselves. It is a format for **describing the state** that "a document existed at a certain point in time, with certain intent."

- ✅ **Records existence** - when, who, and intent
- ✅ **Fixes state** - immutability through hashing
- ✅ **Offline-first** - no central servers required
- ❌ **Does not prove correctness** - no truth judgment

**Works fully offline and does not require trust, servers, or blockchains.**

---

## Design Principles

- **Block-based immutable text**
- **RFC 8785 JSON Canonicalization**
- **Hash-first, signature-optional**
- **Offline verification by design**
- **Trust and authority are out of scope**

---

## Quick Start

```bash
# Initialize document
python3 medf.py init > document.medf.json

# Generate hashes
python3 medf.py pack document.medf.json

# Verify integrity
python3 medf.py verify document.medf.json

# Sign (optional)
python3 medf.py sign document.medf.json --key private.key

# Explain verification
python3 medf.py explain
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

## Canonicalization

MEDF adopts RFC 8785 (JSON Canonicalization Scheme, JCS)
for all cryptographic operations such as hashing and signing.

MEDF does not define its own canonicalization rules.
This avoids ambiguity and ensures interoperability
with existing cryptographic tooling.

---

## Continuous Integration

MEDF documents in this repository are automatically verified by GitHub Actions:

```yaml
name: MEDF Verify
on:
  push:
    paths:
      - "**/*.medf.json"
```

This ensures that any MEDF document pushed to the repository is automatically verified for integrity.

---

## MEDF Diff

MEDF can diff documents at semantic block level, not just line-based text diffs.

```bash
medf diff v1.medf.json v2.medf.json
```

Output:
```
Block changed: policy
- Previous hash: sha256:ab12...
+ New hash:      sha256:ff98...

Block unchanged: executive_summary
Block added: appendix
```

JSON output for CI/automation:
```bash
medf diff v1.medf.json v2.medf.json --json
```

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

## What MEDF is NOT

MEDF is **NOT**:
- A blockchain
- A trust or identity system
- A certificate authority
- A content moderation tool
- A way to decide what is true or official

MEDF does **NOT**:
- Judge correctness of content
- Decide who should be trusted
- Prevent publishing false information

MEDF **ONLY**:
- Makes text content verifiable
- Detects unintended or malicious changes
- Enables precise, block-level references

---

## Trust and Key Management

MEDF defines how documents are structured and verified,
but does not define global trust authorities or key management systems.

How a public key is trusted (for example, organizational PKI,
platform-based identity, or social proofs)
is intentionally left outside the core specification.

Reference implementations may demonstrate practical trust anchors.

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
# Initialize document
python3 medf.py init > document.medf.json

# Generate hashes
python3 medf.py pack document.medf.json

# Verify document integrity
python3 medf.py verify document.medf.json

# Explain verification
python3 medf.py verify document.medf.json --explain
python3 medf.py explain

# Sign document (optional)
python3 medf.py sign document.medf.json --key private.key
```

---

## Reference Tracking (Draft)

**Proposal v0.2.2**: Blocks can cite other MEDF documents and blocks.

**Citation format in text:**
```
MEDF: paper-2026-example#methodology
```

**Structured references (optional):**
```json
{
  "block_id": "discussion",
  "references": [
    {
      "document_id": "paper-2026-example",
      "block_id": "methodology",
      "uri": "./paper-2026-example.medf.json"
    }
  ]
}
```

**Proposed command:**
```bash
# Resolve references (offline-first)
medf resolve document.medf.json --block discussion

# Fetch remote references (explicit online)
medf resolve document.medf.json --block discussion --fetch
```

**Key principles:**
- ✅ **Offline-first**: Reference resolution works without network
- ✅ **Optional online**: Fetch only with explicit `--fetch` flag
- ✅ **Local caching**: Fetched documents cached for offline use
- ✅ **Not validation**: References are metadata, not requirements

📖 **Full specification**: [docs/references.md](docs/references.md)

**Status**: Draft proposal. Feedback welcome!

---

## MEDF Viewer (Draft)

**Proposal**: Flexible, block-based document viewer — not fixed layout like PDF.

**Key features:**
- 📱 **Responsive**: Adapts to device, no fixed page boundaries
- 🔗 **Block-level linking**: `MEDF: doc#section` → direct navigation
- 📄 **Block embedding**: Embed individual sections in web pages
- 🎨 **Flexible styling**: Themes, fonts, layouts are mutable

**Examples:**

```html
<!-- Embed single block -->
<medf-block src="paper.medf.json" block-id="abstract"></medf-block>
```

```javascript
// Navigate to block
viewer.navigateToBlock('methodology');
```

**Live demos:** [examples/viewer/](examples/viewer/)
- `index.html` - Full viewer with TOC
- `embed.html` - Block embedding examples
- `web-component.html` - Web Component API proposal

**📖 Full specification:** [docs/viewer.md](docs/viewer.md)

**Status:** Reference implementation available. Web Components proposed.

---

## Specification

- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) (System design)
- **Viewer**: [docs/viewer.md](docs/viewer.md) (Reference implementation)
- **Reference Tracking**: [docs/references.md](docs/references.md) (Draft v0.2.2)
- **Philosophy**: [PHILOSOPHY.md](PHILOSOPHY.md) / [思想.md](思想.md)
- **AI-Generated Documents**: [docs/ai-generated-documents.md](docs/ai-generated-documents.en.md) / [docs/ai-generated-documents.md](docs/ai-generated-documents.md)
- **Trust Anchors**: [docs/trust.md](docs/trust.md) (Practical examples)
- **Block IDs**: [docs/block-id.md](docs/block-id.md) (Guidelines)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (Common issues)
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

## IPFS Compatibility

MEDF documents work well with IPFS (InterPlanetary File System) for content-addressed storage and distribution.

**Key compatibility features:**
- ✅ **Content addressing**: `doc_hash` serves as content identifier
- ✅ **Immutable storage**: Content-addressed via CID (Content Identifier)
- ✅ **Optional pinning**: Pin to IPFS for persistent availability
- ✅ **Offline-first**: No IPFS required for verification

**Example workflow:**

```bash
# 1. Create MEDF document
python3 medf.py import document.md

# 2. Add to IPFS
ipfs add document.medf.json
# Output: added QmABC123... document.medf.json

# 3. Pin for persistence (optional)
ipfs pin add QmABC123...

# 4. Share via IPFS
ipfs get QmABC123... -o downloaded.medf.json
python3 medf.py verify downloaded.medf.json
```

**Benefits of IPFS + MEDF:**
- **Decentralized**: No central server required
- **Verifiable**: Hash-based content addressing
- **Persistent**: Content remains available as long as pinned
- **Citable**: Stable CID for referencing

**Note**: IPFS is **optional**. MEDF works fully offline without IPFS. IPFS integration is for users who want decentralized storage and distribution.

**Learn more**:
- [IPFS Documentation](https://docs.ipfs.tech/)
- [Content Addressing](https://docs.ipfs.tech/concepts/content-addressing/)

---

## Links

- GitHub: https://github.com/maskin/medf
- Schema: [spec/medf.schema.json](spec/medf.schema.json)
