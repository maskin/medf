# Getting Started with MeDF

Welcome to MeDF (Mutable Expression Description Format)! This guide will help you create, verify, and share your first MeDF document in 5 minutes.

## Prerequisites

- Python 3.7+
- Git (optional, for cloning the repository)

## Installation

```bash
# Clone the repository
git clone https://github.com/maskin/medf.git
cd medf

# No additional dependencies required!
# MeDF works completely offline with just Python
```

## 5-Minute Quick Start

### Step 1: Create a Document

```bash
python3 medf.py init > my-document.medf.json
```

This creates a basic MeDF document with:
- A unique document ID
- A timestamp (snapshot)
- An issuer identifier
- One example block

### Step 2: Edit Your Content

Open `my-document.medf.json` in your editor and modify the block text:

```json
{
  "medf_version": "0.2.1",
  "id": "my-first-document",
  "snapshot": "2026-02-08T10:00:00Z",
  "issuer": "your-name",
  "blocks": [
    {
      "block_id": "introduction",
      "role": "body",
      "format": "markdown",
      "text": "# My First MeDF Document\n\nThis is my first document in MeDF format.",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  }
}
```

### Step 3: Generate Hashes

```bash
python3 medf.py pack my-document.medf.json
```

This command:
- Calculates the hash for each block
- Calculates the document hash
- Updates your file with the hashes

### Step 4: Verify Integrity

```bash
python3 medf.py verify my-document.medf.json
```

Output:
```
✓ Document verified successfully
  Blocks: 1
  Document hash: sha256:abc123...
```

### Step 5: Share Your Document

Your document is now ready to share! You can:
- Email it as JSON
- Upload to GitHub
- Share via IPFS (see [IPFS Integration](#ipfs-integration))
- Embed in a website

## Understanding the Structure

```
MeDF Document
├── Metadata
│   ├── medf_version: "0.2.1"
│   ├── id: unique identifier
│   ├── snapshot: creation timestamp
│   └── issuer: who created it
├── Blocks (immutable content)
│   ├── block_id: semantic identifier
│   ├── role: body, appendix, etc.
│   ├── format: markdown
│   ├── text: actual content
│   └── block_hash: SHA-256 hash
└── Document Hash (overall integrity)
    ├── algorithm: sha-256
    └── value: hash of all blocks
```

## Common Tasks

### Add a New Block

```json
{
  "block_id": "methodology",
  "role": "body",
  "format": "markdown",
  "text": "## Methodology\n\nOur approach...",
  "block_hash": ""
}
```

Then run `pack` again to generate hashes.

### Reference Another Document

Use the citation format:

```markdown
As discussed in MEDF: paper-2026-xyz#methodology, ...
```

See [docs/references.md](references.md) for full details.

### Sign Your Document

```bash
python3 medf.py sign my-document.medf.json --key my-private-key.pem
```

This proves "you" created this version (optional).

## IPFS Integration

MeDF documents are perfect for IPFS sharing because:

1. **Content-addressed**: Each document has a unique hash
2. **Offline-verifiable**: No servers needed to verify integrity
3. **Immutable blocks**: Text content never changes
4. **Flexible presentation**: Styling and layout can evolve

See [IPFS_INTEGRATION.md](IPFS_INTEGRATION.md) for detailed instructions.

## Troubleshooting

### "Command not found: python3"

Try `python` instead, or install Python 3 from [python.org](https://www.python.org).

### "Hashes don't match"

This means the document was modified after hashing. This is expected! Run `pack` again to update hashes.

### "Verify failed"

The document's hashes don't match the content. This could mean:
- The JSON was edited manually
- The file was corrupted
- A block was modified

Check the error message for details.

## Next Steps

- **Read examples**: Check [examples/](../examples/) for real-world documents
- **Learn philosophy**: See [PHILOSOPHY.md](../PHILOSOPHY.md) for design principles
- **Explore features**: Try `python3 medf.py --help` for all commands
- **Join community**: Open an issue on GitHub to discuss ideas

## FAQ

**Q: Do I need a server?**
A: No! MeDF works completely offline.

**Q: Can I edit a document after hashing?**
A: Yes, but the hash will change. This is intentional—it shows the document evolved.

**Q: Is this blockchain?**
A: No. It's a document format. Distribution and consensus are optional.

**Q: Can I use this for sensitive documents?**
A: Yes, but add encryption separately. MeDF handles integrity, not confidentiality.

## Getting Help

- **Issues**: Open a GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for ideas
- **Documentation**: See [docs/](../) for detailed specifications

---

Happy documenting! 🚀
