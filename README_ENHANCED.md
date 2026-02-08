# MeDF — Mutable Expression Description Format

**TL;DR**: MeDF is a document format that makes text verifiable while allowing flexible presentation. It separates immutable content (hashed blocks) from mutable presentation (styling, layout). Perfect for academic papers, news, regulations, and IPFS sharing.

---

## What is MeDF?

MeDF (Mutable Expression Description Format) is a JSON-based document format designed to:

- ✅ **Make text verifiable** - Cryptographic hashes prove content hasn't changed
- ✅ **Allow flexible presentation** - Styling, layout, and rendering can evolve
- ✅ **Work offline** - No servers, APIs, or blockchains required
- ✅ **Enable precise references** - Cite specific blocks: `MEDF: paper-2026-xyz#methodology`
- ✅ **Integrate with IPFS** - Content-addressed storage for decentralized sharing

```
MeDF Document = Immutable Text Blocks (hashed) + Mutable Presentation (free to change)
```

---

## Key Concept

MeDF separates **what was said** from **how it's presented**:

| Aspect | Status | Example |
|--------|--------|---------|
| **Text content** | ✅ Immutable | "The methodology is..." |
| **Block structure** | ✅ Immutable | Introduction, Methodology, Results |
| **Hashes** | ✅ Immutable | sha256:abc123... |
| **Styling** | 🔄 Mutable | Font, color, layout |
| **Rendering** | 🔄 Mutable | HTML, PDF, web component |
| **Indexing** | 🔄 Mutable | Table of contents, search |

**Result**: Documents can evolve without breaking verification.

---

## Quick Start (5 minutes)

### 1. Install

```bash
git clone https://github.com/maskin/medf.git
cd medf
# No dependencies! Just Python 3.7+
```

### 2. Create

```bash
python3 medf.py init > my-document.medf.json
```

### 3. Edit

Open `my-document.medf.json` and modify the text blocks.

### 4. Hash

```bash
python3 medf.py pack my-document.medf.json
```

### 5. Verify

```bash
python3 medf.py verify my-document.medf.json
# ✓ Document verified successfully
```

### 6. Share

```bash
# Via IPFS
ipfs add my-document.medf.json
# QmXxxx...

# Via email, GitHub, or anywhere
```

**Full guide**: [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

---

## IPFS Integration

MeDF is perfect for IPFS because:

1. **Content-addressed** - Document hash is its address
2. **Offline-verifiable** - No server needed to verify integrity
3. **Immutable blocks** - Text content never changes
4. **Semantic references** - Block-level citations work with IPFS

```bash
# Create and hash
python3 medf.py pack paper.medf.json

# Publish to IPFS
ipfs add paper.medf.json
# QmXxxx...

# Share: ipfs://QmXxxx or https://ipfs.io/ipfs/QmXxxx
# Anyone can verify offline!
```

**Full guide**: [docs/IPFS_INTEGRATION.md](docs/IPFS_INTEGRATION.md)

---

## Document Structure

```json
{
  "medf_version": "0.2.1",
  "id": "document-id",
  "snapshot": "2026-02-08T10:00:00Z",
  "issuer": "author@example.com",
  "blocks": [
    {
      "block_id": "introduction",
      "role": "body",
      "format": "markdown",
      "text": "# Introduction\n\nThis is the introduction...",
      "block_hash": "sha256:abc123..."
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": "sha256:xyz789..."
  }
}
```

**Key fields**:
- `blocks` - Immutable content units
- `block_hash` - Hash of each block
- `doc_hash` - Hash of entire document
- `signature` - Optional cryptographic signature (proves authorship)

---

## Design Principles

1. **Block-based immutable text** - Content is organized into semantic units
2. **RFC 8785 JSON Canonicalization** - Standard hashing for interoperability
3. **Hash-first, signature-optional** - Integrity is essential, signatures are optional
4. **Offline verification by design** - No servers or APIs required
5. **Trust and authority are out of scope** - MeDF records "what existed," not "what's true"

---

## Use Cases

| Use Case | Why MeDF? | Example |
|----------|-----------|---------|
| **Academic papers** | Block-level citations, version tracking | `MEDF: paper-2026-xyz#methodology` |
| **News articles** | Correction history, immutable original | Version 1, 2, 3 with corrections |
| **Government documents** | Cryptographic signatures, offline verification | Regulations, policies |
| **Technical specs** | API documentation with change tracking | API v1, v2, v3 |
| **Blog posts** | Discussion with verifiable references | Comments with citations |
| **IPFS sharing** | Content-addressed, decentralized | `ipfs://QmXxxx...` |

**See examples**: [docs/EXAMPLES.md](docs/EXAMPLES.md)

---

## CLI Reference

```bash
# Initialize document
python3 medf.py init > document.medf.json

# Generate hashes for all blocks
python3 medf.py pack document.medf.json

# Verify document integrity
python3 medf.py verify document.medf.json

# Verify with explanation
python3 medf.py verify document.medf.json --explain

# Sign document (optional, requires private key)
python3 medf.py sign document.medf.json --key private.key

# Diff two versions
python3 medf.py diff v1.medf.json v2.medf.json

# Get help
python3 medf.py --help
```

---

## Citation Format

Reference specific blocks in other documents:

```
MEDF: document-id#block-id
```

**Example**:
```markdown
As discussed in MEDF: paper-2026-quantum#methodology, we used...
```

**Resolving references**:
```bash
python3 medf.py resolve document.medf.json --block discussion
```

**Full spec**: [docs/references.md](docs/references.md)

---

## Philosophy

MeDF is built on these core principles:

1. **Does not judge correctness** - MeDF records "what existed," not "what's true"
2. **Records "when/who/intent existed"** - Not "is this correct?" but "when/who/with what intent?"
3. **Hash as responsibility boundary** - Hash proves "unchanged from this state," not trust
4. **History as chains** - Each state linked by `previous`, branching allowed
5. **Offline-first** - No network, servers, or external APIs required
6. **JSON as compromise** - Human-readable, machine-processable, CLI-generatable
7. **No forced trust** - Records "who fixed this," not "this is trustworthy"

**Full philosophy**: [PHILOSOPHY.md](PHILOSOPHY.md) / [思想.md](思想.md)

---

## What MeDF is NOT

❌ **Not a blockchain** - No consensus or distribution required  
❌ **Not a trust system** - Doesn't determine who to trust  
❌ **Not a certificate authority** - Doesn't authenticate identity  
❌ **Not a content moderation tool** - Doesn't filter or judge content  
❌ **Not a way to decide what's true** - Doesn't determine correctness  

**MeDF ONLY**:
- ✅ Makes text content verifiable
- ✅ Detects unintended or malicious changes
- ✅ Enables precise, block-level references

---

## Continuous Integration

MeDF documents in this repository are automatically verified by GitHub Actions:

```yaml
name: MEDF Verify
on:
  push:
    paths:
      - "**/*.medf.json"
```

This ensures any pushed MeDF document is automatically verified for integrity.

---

## AI-Generated Documents

**Position**: MeDF provides verifiable document state regardless of creation method (AI or human).

> "The problem is not 'AI wrote this' — the essence is 'provenance and responsibility cannot be verified'"

**Full statement**: [docs/ai-generated-documents.md](docs/ai-generated-documents.en.md)

---

## Documentation

| Document | Purpose |
|----------|---------|
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | 5-minute tutorial |
| [IPFS_INTEGRATION.md](docs/IPFS_INTEGRATION.md) | IPFS compatibility guide |
| [EXAMPLES.md](docs/EXAMPLES.md) | Real-world use cases |
| [PHILOSOPHY.md](PHILOSOPHY.md) | Design principles |
| [docs/references.md](docs/references.md) | Reference tracking spec |
| [docs/viewer.md](docs/viewer.md) | Viewer implementation |
| [docs/trust.md](docs/trust.md) | Trust anchors |
| [docs/ai-generated-documents.md](docs/ai-generated-documents.en.md) | AI content position |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## Specification

- **Format**: [spec/medf.schema.json](spec/medf.schema.json)
- **Version**: 0.2.1
- **License**: MIT

---

## Community

- **Issues**: [GitHub Issues](https://github.com/maskin/medf/issues)
- **Discussions**: [GitHub Discussions](https://github.com/maskin/medf/discussions)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## License

MIT License - See [LICENSE](LICENSE) for details

**"No forced trust | No central control | No fork fear"** - Fully aligned with MeDF philosophy

---

## Related Projects

- **[MeDF Hub](https://github.com/maskin/medf-hub)** - Web platform for creating, sharing, and discussing MeDF documents
- **[Awesome IPFS](https://github.com/ipfs/awesome-ipfs)** - Collection of IPFS projects
- **[Ceramic Protocol](https://ceramic.network/)** - Decentralized document store

---

## Getting Help

- **Quick questions**: Open a [GitHub Issue](https://github.com/maskin/medf/issues)
- **Ideas & feedback**: Use [GitHub Discussions](https://github.com/maskin/medf/discussions)
- **Documentation**: Check [docs/](docs/) for detailed guides
- **Examples**: See [examples/](examples/) for working documents

---

## Next Steps

1. **Try it**: Follow [GETTING_STARTED.md](docs/GETTING_STARTED.md)
2. **Learn more**: Read [PHILOSOPHY.md](PHILOSOPHY.md)
3. **Share documents**: Use [IPFS_INTEGRATION.md](docs/IPFS_INTEGRATION.md)
4. **Build applications**: Check [MeDF Hub](https://github.com/maskin/medf-hub)
5. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**MeDF: Making documents verifiable, flexible, and decentralized** 🚀
