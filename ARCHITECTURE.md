# MEDF Architecture

This document describes the architecture and structure of the MEDF project.

---

## Overview

MEDF (Mutable Expression Description Format) is a document format specification with reference implementations for document creation, verification, and viewing.

**Core Philosophy**: Separate immutable text content from mutable presentation.

---

## Repository Structure

```
mdf/
├── medf.py                          # CLI tool for MEDF operations
├── spec/
│   └── medf.schema.json             # Normative JSON schema
├── docs/                            # Documentation
│   ├── ai-generated-documents.md   # Position on AI-generated content
│   ├── ai-generated-documents.en.md # English version
│   ├── block-id.md                 # Block ID guidelines
│   ├── references.md               # Reference tracking spec (draft)
│   ├── trust.md                    # Trust anchor examples
│   └── viewer.md                   # Viewer specification
├── examples/                        # Example MEDF documents
│   ├── academic-paper.md           # Source Markdown
│   ├── academic-paper.medf.json    # Converted MEDF
│   ├── admin-guideline.md          # Japanese example
│   ├── admin-guideline.medf.json
│   ├── paper-a.medf.json          # Reference examples
│   ├── paper-b.medf.json
│   └── viewer/                     # Reference viewer implementation
│       ├── index.html              # Full viewer
│       ├── embed.html              # Block embedding
│       ├── web-component.html      # Web Component proposal
│       ├── medf-viewer.css         # Styles
│       └── medf-viewer.js          # JavaScript implementation
├── .github/
│   └── workflows/
│       └── medf-verify.yml         # CI for MEDF verification
├── README.md                        # Main documentation
├── PHILOSOPHY.md                    # Design philosophy (English)
├── 思想.md                          # 設計思想 (日本語)
├── TROUBLESHOOTING.md              # Common issues and solutions
├── ARCHITECTURE.md                  # This file
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # MIT License
└── draft-medf-format-00.md         # IETF Internet-Draft
```

---

## Component Responsibilities

### Core Components

#### 1. CLI Tool (`medf.py`)
**Purpose**: Command-line interface for MEDF document operations.

**Commands**:
- `init` - Create document skeleton
- `import` - Convert Markdown to MEDF (auto-packs by default)
- `pack` - Generate hashes for blocks and document
- `verify` - Verify document integrity
- `sign` - Attach cryptographic signature (optional)
- `diff` - Compare documents at block level
- `explain` - Explain verification philosophy

**Responsibilities**:
- Document creation and modification
- Hash generation (SHA-256)
- JSON Canonicalization (RFC 8785)
- Signature operations (ed25519, optional)
- Verification logic

**Not responsible for**:
- Trust evaluation
- Content correctness judgment
- Authority determination
- Network operations (offline-first)

#### 2. Schema (`spec/medf.schema.json`)
**Purpose**: Normative specification of MEDF document structure.

**Defines**:
- Required fields (`medf_version`, `id`, `snapshot`, `issuer`, `blocks`, `doc_hash`)
- Optional fields (`signature`, `document_type`, `language`, `references`)
- Block structure (`block_id`, `role`, `format`, `text`, `block_hash`)
- Reference structure (draft v0.2.2)

**Responsibilities**:
- Structure validation
- Type definitions
- Field constraints
- Normative behavior

#### 3. Viewer (`examples/viewer/`)
**Purpose**: Reference implementation for displaying MEDF documents.

**Components**:
- **HTML** - Document structure
- **CSS** - Responsive styling with themes
- **JavaScript** - MEDFViewer class

**Features**:
- Block-based rendering
- Table of contents generation
- Block-level navigation
- Citation copying
- Document verification display
- Theme switching (light/dark)

**Responsibilities**:
- Document display
- User interaction
- Responsive design
- Block-level linking

**Not responsible for**:
- Content modification
- Hash generation
- Verification logic (uses CLI tool)

### Supporting Components

#### 4. Documentation (`docs/`)
- **PHILOSOPHY.md / 思想.md** - Design principles and philosophy
- **references.md** - Reference tracking specification (draft)
- **viewer.md** - Viewer specification
- **trust.md** - Trust anchor examples
- **block-id.md** - Block ID guidelines
- **ai-generated-documents.md** - Position on AI-generated content

#### 5. CI/CD (`.github/workflows/`)
- **medf-verify.yml** - Automatic MEDF verification on push/PR
  - Triggers on `*.medf.json` changes
  - Runs `medf verify` on all examples

#### 6. Examples (`examples/`)
- Academic paper example
- Administrative guideline example (Japanese)
- Reference tracking examples (paper-a, paper-b)
- Viewer implementation

---

## Data Flow

### Document Creation Flow

```
Markdown (.md)
    ↓
medf.py import
    ↓
Split by ## headers
    ↓
Create blocks with block_ids
    ↓
Generate JSON (.medf.json)
    ↓
medf.py pack
    ↓
Calculate block hashes
    ↓
Calculate document hash
    ↓
Verifiable MEDF document ✓
```

### Verification Flow

```
Load .medf.json
    ↓
Extract block_hash for each block
    ↓
Recalculate hash from block content
    ↓
Compare: expected == actual?
    ↓
Calculate document hash
    ↓
Compare: doc_hash matches?
    ↓
Verify signature (if present)
    ↓
Result: Integrity verified ✓
```

### Viewing Flow

```
Load .medf.json
    ↓
Verify hashes (optional)
    ↓
Generate table of contents
    ↓
Render blocks
    ↓
Apply theme/styling
    ↓
Enable navigation
    ↓
Display in browser ✓
```

---

## Design Principles

### 1. Separation of Concerns

| Layer | Responsibility | Mutable |
|-------|---------------|----------|
| **Content** | Text in blocks | ✅ Immutable |
| **Structure** | Block organization | ✅ Immutable |
| **Presentation** | Rendering, layout | ✅ Mutable |
| **Indexing** | Table of contents | ✅ Mutable |
| **References** | Citation metadata | ✅ Mutable |

### 2. Offline-First

- **No network required** for creation or verification
- **No central servers** for document validity
- **No external APIs** for core operations
- **Optional online features** (future: reference fetching)

### 3. Cryptographic Foundations

**Canonicalization**: RFC 8785 (JCS)
- UTF-8 encoding
- Sorted keys
- No whitespace separators

**Hashing**: SHA-256
- Per-block hashes
- Document hash
- Content-based addressing

**Signing**: ed25519 (optional)
- Signs document hash value
- Public key embedded in document
- Does NOT imply trust or authority

### 4. Extensibility

**Optional fields**:
- `document_type` - Document classification
- `language` - Language code
- `references` - Block-level citations (draft)
- `signature` - Cryptographic signature

**Future extensions**:
- Additional block roles
- New hash algorithms
- Alternative signature schemes

---

## Technology Choices

### Why Python for CLI?

**Pros**:
- ✅ Readable and maintainable
- ✅ Excellent JSON support
- ✅ Cross-platform
- ✅ Easy to distribute (single file)
- ✅ No build step required

**Cons**:
- ❌ Slower than compiled languages
- ❌ GIL limits concurrency

**Decision**: Python is sufficient for MEDF's needs. Performance is not a bottleneck for document processing.

### Why JSON for Format?

**Pros**:
- ✅ Human-readable
- ✅ Machine-parseable
- ✅ Git-friendly (diff tracking)
- ✅ Widely supported
- ✅ CLI-generatable

**Cons**:
- ❌ Verbose compared to binary
- ❌ No built-in hash reference

**Decision**: Readability and tool support outweigh verbosity. JSON is a compromise, not an ideal (see PHILOSOPHY.md).

### Why HTML/CSS/JS for Viewer?

**Pros**:
- ✅ Universal browser support
- ✅ No installation required
- ✅ Responsive design
- ✅ Embeddable

**Cons**:
- ❌ Requires browser for viewing
- ❌ JavaScript dependency

**Decision**: Web is the most accessible platform. Alternative viewers can be built (CLI, desktop apps).

---

## Security Considerations

### Threat Model

**Protects against**:
- ✅ Tampering (modification detection)
- ✅ Impersonation (signatures, if used)

**Does NOT protect against**:
- ❌ Malicious content (intentional lies)
- ❌ Compromised keys (trust evaluation)
- ❌ Fake identities (authority verification)

### Hash Security

**Algorithm**: SHA-256
- Collision resistance: Currently secure
- Preimage resistance: Currently secure
- **Note**: Monitor cryptographic research; be prepared to migrate

### Signature Security

**Algorithm**: ed25519
- Fast signature generation
- Small signature size
- No known practical attacks

**Limitations**:
- Private key protection is user's responsibility
- Key revocation not specified (out of scope)
- Trust establishment is application-level

---

## Extension Points

### 1. Custom Block Roles

Current roles: `abstract`, `policy`, `body`, `results`, `scope`

Extendable: Yes
- Add custom roles in `blocks[].role`
- Viewer styling via `data-role` attribute

### 2. Reference Tracking (Draft v0.2.2)

Add to blocks:
```json
{
  "block_id": "discussion",
  "references": [
    {
      "document_id": "paper-2024",
      "block_id": "methodology",
      "uri": "./paper-2024.medf.json"
    }
  ]
}
```

### 3. Alternative Viewers

Possible implementations:
- **CLI viewer** (`medf cat document.medf.json`)
- **Desktop app** (Electron, Tauri)
- **Mobile app** (React Native, Flutter)
- **Server-side renderer** (Express, FastAPI)

### 4. Export Formats

Possible conversions:
- **PDF** (fixed layout)
- **EPUB** (e-book format)
- **Slides** (reveal.js, PowerPoint)
- **Markdown** (round-trip conversion)

---

## Performance Characteristics

### Memory Usage

- **Small documents** (<1MB): ~5-10MB RAM
- **Large documents** (10MB): ~50-100MB RAM
- **Viewer**: Similar, plus browser overhead

### Disk Usage

- **Markdown source**: ~10-100KB
- **MEDF JSON**: ~15-150KB (with hashes)
- **Ratio**: ~1.5x original size

### Processing Time

- **Import**: <1 second for typical documents
- **Pack**: <1 second
- **Verify**: <1 second
- **Sign**: <1 second (with PyNaCl)

---

## Dependencies

### Required

- **Python 3.6+**: Core language
- **Standard library**: `json`, `hashlib`, `pathlib`, `datetime`, `re`

### Optional

- **PyNaCl**: For signing operations
  ```bash
  pip install pynacl
  ```
- **Browser**: For viewing examples
- **Git**: For version control

---

## Compliance and Standards

### Standards Used

1. **RFC 8785**: JSON Canonicalization Scheme (JCS)
   - Normative for all cryptographic operations

2. **RFC 4648**: Base64 Encoding
   - Used for signature encoding

3. **ISO 8601**: Timestamps
   - Used for `snapshot` field

### IETF Draft

- **Internet-Draft**: `draft-medf-format-00.md`
  - Status: Informational
  - Purpose: Formal documentation of MEDF format

---

## Future Architecture Evolution

### Phase 1: Current (v0.2.1)
- ✅ Core CLI tool
- ✅ Reference viewer implementation
- ✅ GitHub Actions CI
- ✅ Schema specification

### Phase 2: Near Future (v0.2.2)
- ⏳ Reference tracking implementation
- ⏳ `medf resolve` command
- ⏳ Enhanced viewer with reference navigation

### Phase 3: Long Term
- 📋 Web Components (`<medf-viewer>`, `<medf-block>`)
- 📋 Alternative viewers (CLI, desktop)
- 📋 Export tools (PDF, EPUB)
- 📋 IPFS integration (optional)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Pull request process
- Issue reporting
- Feature proposals

---

## License

MIT License - See [LICENSE](LICENSE)

**"No forced trust | No central control | No fork fear"**
