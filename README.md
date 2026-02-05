# MeDF

**Mutable Expression Description Format** - A format to fix document states, not to judge correctness or authority.

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

---

## Citation Format

```
MEDF: paper-2026-example#methodology
```

- `paper-2026-example` - Document ID
- `#methodology` - Block ID

---

## Philosophy

**Core Principles** (see [思想.md](思想.md) for full philosophy):

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

---

## Use Cases

- **Academic papers**: Section-level reference (`MEDF: paper-2026-xyz#methodology`)
- **Public documents**: Revision history tracking
- **Impersonation prevention**: Proving "same person" through key continuity
- **Signing**: Claim of "I fixed this" (not trust)

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

- **Philosophy**: [PHILOSOPHY.md](PHILOSOPHY.md) (English) / [思想.md](思想.md) (日本語)
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
