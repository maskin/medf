# IPFS Integration with MeDF

MeDF documents are naturally suited for IPFS (InterPlanetary File System) sharing. This guide explains why and how.

## Why IPFS + MeDF?

### Content Addressing

IPFS uses **content-based addressing** (hashing) instead of location-based URLs:

```
Traditional URL:  https://example.com/papers/2026-01-15.pdf
                  ↓ (server goes down, link breaks)

IPFS Hash:        QmXxxx...
                  ↓ (content is the address, always works)
```

MeDF documents are perfect for this because:

1. **Immutable blocks** - Text content never changes
2. **Built-in hashes** - Each block and document has SHA-256 hashes
3. **Offline verification** - No server needed to verify integrity
4. **Semantic references** - Block-level citations (`MEDF: doc#section`)

### Distribution Model

```
Traditional CMS:
  Author → Central Server → Readers
           (single point of failure)

IPFS + MeDF:
  Author → IPFS Network → Any Reader
           (distributed, resilient)
```

## How It Works

### 1. Create and Hash Your Document

```bash
# Create document
python3 medf.py init > paper.medf.json

# Add content and generate hashes
python3 medf.py pack paper.medf.json

# Verify integrity
python3 medf.py verify paper.medf.json
```

### 2. Add to IPFS

**Option A: Using IPFS Desktop or CLI**

```bash
# Install IPFS (https://docs.ipfs.tech/install/)
ipfs add paper.medf.json

# Output:
# added QmXxxx paper.medf.json
```

**Option B: Using Pinata (Pinned IPFS)**

```bash
# Sign up at https://www.pinata.cloud/
# Upload via web interface or API

curl -X POST https://api.pinata.cloud/pinning/pinFileToIPFS \
  -H "pinata_api_key: YOUR_KEY" \
  -H "pinata_secret_api_key: YOUR_SECRET" \
  -F "file=@paper.medf.json"
```

**Option C: Using Web3.Storage**

```bash
# Sign up at https://web3.storage/
# Upload via CLI or web interface

npx web3 put paper.medf.json
```

### 3. Share the IPFS Hash

Once added, you get a content hash (CID):

```
QmXxxx... (IPFS v0)
bafyxxx... (IPFS v1)
```

Share this hash with others:

```
"Check out my paper: ipfs://QmXxxx..."
"Or via gateway: https://ipfs.io/ipfs/QmXxxx..."
```

### 4. Verify Anywhere

Anyone can verify the document without a server:

```bash
# Download from IPFS
ipfs get QmXxxx > paper.medf.json

# Verify integrity
python3 medf.py verify paper.medf.json

# ✓ Document verified successfully
```

## Practical Examples

### Academic Paper

```json
{
  "medf_version": "0.2.1",
  "id": "paper-2026-quantum",
  "snapshot": "2026-02-08T10:00:00Z",
  "issuer": "alice@university.edu",
  "blocks": [
    {
      "block_id": "abstract",
      "role": "body",
      "format": "markdown",
      "text": "## Abstract\n\nQuantum computing breakthrough...",
      "block_hash": "sha256:abc123..."
    },
    {
      "block_id": "methodology",
      "role": "body",
      "format": "markdown",
      "text": "## Methodology\n\nWe used...",
      "block_hash": "sha256:def456..."
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": "sha256:xyz789..."
  }
}
```

**Share as:**
```
IPFS: QmXxxx...
Citation: MEDF: paper-2026-quantum#methodology
```

### News Article with Versioning

```bash
# Version 1
python3 medf.py pack article-v1.medf.json
ipfs add article-v1.medf.json
# QmAAA...

# Version 2 (corrections)
python3 medf.py pack article-v2.medf.json
ipfs add article-v2.medf.json
# QmBBB...

# Both versions available, both verifiable
```

### Government Document

```bash
# Create official document
python3 medf.py init > regulation-2026.medf.json

# Sign with government key
python3 medf.py sign regulation-2026.medf.json --key gov-key.pem

# Publish to IPFS
ipfs add regulation-2026.medf.json
# QmCCC...

# Citizens can verify:
# 1. Document hasn't changed (hash verification)
# 2. Government signed it (signature verification)
# 3. No server dependency (offline verification)
```

## IPFS Gateways

If users don't have IPFS installed, they can access documents via gateways:

```
IPFS Hash:     QmXxxx...

Gateway URLs:
- https://ipfs.io/ipfs/QmXxxx...
- https://gateway.pinata.cloud/ipfs/QmXxxx...
- https://dweb.link/ipfs/QmXxxx...
- https://cf-ipfs.com/ipfs/QmXxxx...
```

## Integration with MeDF Hub

The [MeDF Hub](https://github.com/maskin/medf-hub) platform provides:

- **Web UI** for creating and editing MeDF documents
- **Automatic IPFS publishing** via Pinata API
- **Gateway access** for easy sharing
- **Block-level discussion** on IPFS-published documents

## Best Practices

### 1. Version Management

```bash
# Keep versions in a directory
ls -la versions/
  paper-v1.medf.json  (QmAAA...)
  paper-v2.medf.json  (QmBBB...)
  paper-v3.medf.json  (QmCCC...)

# Link them via "previous" field (future spec)
```

### 2. Pinning Strategy

```
Temporary (1 month):
  - Draft documents
  - Experimental content

Permanent (forever):
  - Published papers
  - Official documents
  - Important references
```

### 3. Citation Format

```markdown
# References

- [Quantum Computing Breakthrough](ipfs://QmXxxx...)
  Citation: MEDF: paper-2026-quantum#abstract

- [Related Work](ipfs://QmYyyy...)
  Citation: MEDF: paper-2026-related#methodology
```

### 4. Offline Verification

```bash
# Download document
ipfs get QmXxxx > paper.medf.json

# Verify without internet
python3 medf.py verify paper.medf.json

# ✓ Works completely offline!
```

## Comparison: Storage Options

| Feature | IPFS | Arweave | Blockchain | Traditional |
|---------|------|---------|-----------|-------------|
| **Cost** | Free (self-host) or $5-20/mo (pinning) | ~$0.50/GB | Expensive | Varies |
| **Permanence** | Pinning required | Permanent | Permanent | Depends on provider |
| **Offline verification** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Decentralized** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Complexity** | Low | Medium | High | Low |
| **Best for** | **Documents, files** | **Permanent archive** | **Blockchain apps** | **Convenience** |

**Recommendation**: IPFS + Pinata for MeDF documents (balance of cost, decentralization, and ease).

## Troubleshooting

### "IPFS node not running"

```bash
# Start IPFS daemon
ipfs daemon

# In another terminal
ipfs add paper.medf.json
```

### "Document not found on IPFS"

The document may have been unpinned. Options:
1. Re-upload to IPFS
2. Use a pinning service (Pinata, Web3.Storage)
3. Ask the author to re-pin

### "How do I update a document on IPFS?"

IPFS content is immutable. To update:
1. Create a new version
2. Upload to IPFS (new hash)
3. Update references to point to new hash
4. Keep old versions for history

## Next Steps

- **Try it**: Follow the [Getting Started](GETTING_STARTED.md) guide
- **Use MeDF Hub**: Web platform with built-in IPFS integration
- **Learn more**: See [PHILOSOPHY.md](../PHILOSOPHY.md) for design principles
- **Join community**: Open an issue on GitHub

---

**MeDF + IPFS = Verifiable, decentralized, offline-first documents** 🚀
