# medf.py Improvements: Setup Simplification & IPFS Integration

This document outlines specific, actionable improvements to `medf.py` to simplify setup and add IPFS CID generation capabilities.

## Current State Analysis

**Strengths**:
- ✅ Minimal dependencies (no external packages required for core functionality)
- ✅ Clear command structure (init, import, pack, verify, sign, diff, explain)
- ✅ Good help text with examples
- ✅ RFC 8785 compliant hashing

**Gaps**:
- ❌ No IPFS CID generation (manual calculation required)
- ❌ Help text could be more discoverable (per-command help)
- ❌ No progress indicators for large files
- ❌ No batch processing support
- ❌ No interactive mode for beginners
- ❌ Missing examples for common workflows

---

## Improvement 1: Per-Command Help

### Current Behavior
```bash
$ medf pack --help
# No output (--help not recognized per-command)
```

### Proposed Behavior
```bash
$ medf pack --help
medf pack — Generate hashes for all blocks and the document

USAGE:
  medf pack <document.medf.json> [options]

DESCRIPTION:
  This command creates a verifiable snapshot of your document.
  It calculates SHA-256 hashes for each block and the entire document
  using RFC 8785 (JSON Canonicalization Scheme).

  The document is NOT frozen. You can always create a new version
  by editing and running pack again.

OPTIONS:
  --verbose    Show detailed progress
  --json       Output results as JSON

EXAMPLES:
  medf pack my-document.medf.json
  medf pack my-document.medf.json --verbose
  medf pack my-document.medf.json --json

WHAT IT DOES:
  1. Reads your MEDF document
  2. Calculates block_hash for each block
  3. Calculates doc_hash for entire document
  4. Updates the file with hashes
  5. Displays summary

WHAT IT DOESN'T DO:
  ✗ Freeze or lock the document
  ✗ Upload to any server
  ✗ Require internet connection
  ✗ Modify your original content

NEXT STEPS:
  • medf verify my-document.medf.json (verify integrity)
  • medf sign my-document.medf.json --key private.key (sign)
  • ipfs add my-document.medf.json (publish to IPFS)

For more information: https://github.com/maskin/medf
```

### Implementation
```python
def cmd_pack_help():
    """Show detailed help for pack command"""
    print("""medf pack — Generate hashes for all blocks and the document
...
""")

def main():
    # ... existing code ...
    if cmd == "pack":
        if "--help" in sys.argv or "-h" in sys.argv:
            cmd_pack_help()
            return
        # ... rest of pack logic ...
```

### Commands to Update
- `medf init --help`
- `medf import --help`
- `medf pack --help`
- `medf verify --help`
- `medf sign --help`
- `medf diff --help`
- `medf explain --help`

---

## Improvement 2: Automatic IPFS CID Generation

### Current Behavior
```bash
$ medf pack document.medf.json
[OK] Hashes generated: document.medf.json
  Blocks: 3
  Document hash: sha256:abc123...

# User must manually:
# 1. Calculate IPFS CID from document hash
# 2. Use external tools or manual calculation
```

### Proposed Behavior
```bash
$ medf pack document.medf.json --ipfs
[OK] Hashes generated: document.medf.json
  Blocks: 3
  Document hash: sha256:abc123...
  IPFS CID (v0):  QmXxxx...
  IPFS CID (v1):  bafyxxx...
  IPFS Gateway:   https://ipfs.io/ipfs/QmXxxx...
  Pinata Gateway: https://gateway.pinata.cloud/ipfs/QmXxxx...

Next steps:
  ipfs add document.medf.json
  # or
  curl -X POST https://api.pinata.cloud/pinning/pinFileToIPFS ...
```

### Implementation

**Step 1: Add IPFS CID calculation function**

```python
import base58
import hashlib

def calculate_ipfs_cid_v0(data: bytes) -> str:
    """
    Calculate IPFS v0 CID (base58-encoded multihash).
    
    IPFS v0 CID format:
    - Multihash prefix: 0x12 (sha256) + 0x20 (32 bytes)
    - Hash: SHA-256 of the data
    - Encoding: Base58
    """
    # SHA-256 hash
    hash_bytes = hashlib.sha256(data).digest()
    
    # Multihash: 0x12 (sha256) + 0x20 (32 bytes) + hash
    multihash = bytes([0x12, 0x20]) + hash_bytes
    
    # Base58 encode
    cid_v0 = base58.b58encode(multihash).decode('ascii')
    return cid_v0

def calculate_ipfs_cid_v1(data: bytes) -> str:
    """
    Calculate IPFS v1 CID (base32-encoded).
    
    IPFS v1 CID format:
    - Prefix: 0x01 (CIDv1) + 0x55 (raw) + 0x12 (sha256) + 0x20 (32 bytes)
    - Hash: SHA-256 of the data
    - Encoding: Base32
    """
    # SHA-256 hash
    hash_bytes = hashlib.sha256(data).digest()
    
    # Multihash: 0x12 (sha256) + 0x20 (32 bytes) + hash
    multihash = bytes([0x12, 0x20]) + hash_bytes
    
    # CIDv1 prefix: 0x01 (version) + 0x55 (dag-json codec)
    cid_v1_bytes = bytes([0x01, 0x55]) + multihash
    
    # Base32 encode (RFC 4648, no padding)
    import base64
    cid_v1 = base64.b32encode(cid_v1_bytes).decode('ascii').lower().rstrip('=')
    return f"bafy{cid_v1}"

def get_ipfs_gateways(cid_v0: str) -> dict:
    """Return common IPFS gateway URLs"""
    return {
        "ipfs.io": f"https://ipfs.io/ipfs/{cid_v0}",
        "pinata": f"https://gateway.pinata.cloud/ipfs/{cid_v0}",
        "dweb.link": f"https://dweb.link/ipfs/{cid_v0}",
        "cf-ipfs": f"https://cf-ipfs.com/ipfs/{cid_v0}",
        "local": f"ipfs://{cid_v0}"
    }
```

**Step 2: Update pack command**

```python
def cmd_pack(path: Path, ipfs: bool = False, verbose: bool = False):
    """
    Generate hashes for all blocks and the document.
    Optionally calculate IPFS CIDs.
    """
    doc = json.loads(path.read_text(encoding="utf-8"))

    # ... existing hash generation code ...

    print(f"[OK] Hashes generated: {path}")
    print(f"  Blocks: {len(doc['blocks'])}")
    print(f"  Document hash: {doc['doc_hash']['value'][:16]}...")
    
    if ipfs:
        # Calculate IPFS CIDs
        doc_json = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        cid_v0 = calculate_ipfs_cid_v0(doc_json)
        cid_v1 = calculate_ipfs_cid_v1(doc_json)
        
        print()
        print("IPFS Information:")
        print(f"  CID v0: {cid_v0}")
        print(f"  CID v1: {cid_v1}")
        print()
        print("Gateway URLs:")
        gateways = get_ipfs_gateways(cid_v0)
        for name, url in gateways.items():
            print(f"  {name:12} {url}")
        
        if verbose:
            print()
            print("Next steps:")
            print(f"  1. ipfs add {path}")
            print(f"  2. Share: {gateways['local']}")
            print(f"  3. Or use gateway: {gateways['ipfs.io']}")
```

**Step 3: Update CLI argument parsing**

```python
elif cmd == "pack":
    if len(sys.argv) < 3:
        print("usage: medf pack <document.medf> [--ipfs] [--verbose]")
        return
    path = Path(sys.argv[2])
    if not path.exists():
        print(f"[Error] File not found: {path}")
        return
    ipfs = "--ipfs" in sys.argv
    verbose = "--verbose" in sys.argv
    cmd_pack(path, ipfs=ipfs, verbose=verbose)
```

---

## Improvement 3: Interactive Mode for Beginners

### Proposed Behavior
```bash
$ medf --interactive
Welcome to MeDF! 🚀

What would you like to do?
1. Create a new document
2. Import from Markdown
3. Verify an existing document
4. Sign a document
5. Publish to IPFS
6. Exit

Choose (1-6): 1

Document ID (e.g., my-first-doc): my-paper-2026
Issuer (your name/email): alice@example.com

Creating document...
✓ Created: my-paper-2026.medf.json

Next steps:
1. Edit the document in your editor
2. Run: medf pack my-paper-2026.medf.json
3. Run: medf verify my-paper-2026.medf.json

Ready to continue? (y/n):
```

### Implementation
```python
def interactive_mode():
    """Interactive mode for beginners"""
    print("Welcome to MeDF! 🚀")
    print()
    print("What would you like to do?")
    print("1. Create a new document")
    print("2. Import from Markdown")
    print("3. Verify an existing document")
    print("4. Sign a document")
    print("5. Publish to IPFS")
    print("6. Exit")
    print()
    
    choice = input("Choose (1-6): ").strip()
    
    if choice == "1":
        doc_id = input("Document ID (e.g., my-first-doc): ").strip()
        issuer = input("Issuer (your name/email): ").strip()
        # Create document...
    elif choice == "2":
        md_path = input("Markdown file path: ").strip()
        # Import...
    # ... etc ...
```

---

## Improvement 4: Batch Processing

### Proposed Behavior
```bash
$ medf pack *.medf.json --batch
[OK] Processing 5 documents...

✓ document-1.medf.json (3 blocks)
✓ document-2.medf.json (5 blocks)
✓ document-3.medf.json (2 blocks)
✓ document-4.medf.json (8 blocks)
✓ document-5.medf.json (4 blocks)

Summary:
  Processed: 5 documents
  Total blocks: 22
  Time: 0.23s
```

### Implementation
```python
def cmd_pack_batch(pattern: str):
    """Process multiple documents matching pattern"""
    from pathlib import Path
    import glob
    
    files = glob.glob(pattern)
    if not files:
        print(f"[Error] No files matching: {pattern}")
        return
    
    print(f"[OK] Processing {len(files)} documents...")
    print()
    
    total_blocks = 0
    for file_path in sorted(files):
        path = Path(file_path)
        cmd_pack(path)
        doc = json.loads(path.read_text(encoding="utf-8"))
        total_blocks += len(doc['blocks'])
        print()
    
    print(f"Summary:")
    print(f"  Processed: {len(files)} documents")
    print(f"  Total blocks: {total_blocks}")
```

---

## Improvement 5: Progress Indicators for Large Files

### Proposed Behavior
```bash
$ medf pack large-document.medf.json --progress
[OK] Processing large-document.medf.json

Calculating block hashes:
  [████████████████████░░░░░░░░░░░░░░░░░░░░] 50% (25/50 blocks)

Calculating document hash:
  [██████████████████████████████████████████] 100%

✓ Hashes generated: large-document.medf.json
  Blocks: 50
  Document hash: sha256:abc123...
  Time: 1.23s
```

### Implementation
```python
def cmd_pack(path: Path, ipfs: bool = False, progress: bool = False):
    """Generate hashes with optional progress indicator"""
    doc = json.loads(path.read_text(encoding="utf-8"))
    
    if progress:
        total_blocks = len(doc.get("blocks", []))
        print(f"Calculating block hashes:")
    
    # Calculate block_hash
    for i, block in enumerate(doc.get("blocks", [])):
        if progress:
            # Show progress bar
            percent = (i + 1) / total_blocks * 100
            bar_length = 40
            filled = int(bar_length * (i + 1) / total_blocks)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  [{bar}] {percent:.0f}% ({i+1}/{total_blocks} blocks)", end='\r')
        
        block_src = {
            "block_id": block["block_id"],
            "role": block["role"],
            "format": block["format"],
            "text": block["text"],
        }
        block["block_hash"] = sha256_hex(canonical_json(block_src))
    
    if progress:
        print()  # New line after progress
    
    # ... rest of pack logic ...
```

---

## Improvement 6: Configuration File Support

### Proposed Behavior
```bash
# Create .medf.config.json in project root
{
  "default_issuer": "alice@example.com",
  "default_doc_type": "research",
  "auto_ipfs": true,
  "ipfs_gateway": "https://gateway.pinata.cloud",
  "signing_key": "~/.medf/private.key"
}

# Now commands use config defaults
$ medf pack document.medf.json
[OK] Hashes generated: document.medf.json
  Blocks: 3
  Document hash: sha256:abc123...
  IPFS CID (v0): QmXxxx... (from config: auto_ipfs=true)
```

### Implementation
```python
def load_config() -> dict:
    """Load .medf.config.json if it exists"""
    config_path = Path(".medf.config.json")
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {}

def main():
    config = load_config()
    # Use config values as defaults...
```

---

## Improvement 7: Enhanced Error Messages

### Current Behavior
```bash
$ medf pack nonexistent.medf.json
[Error] File not found: nonexistent.medf.json
```

### Proposed Behavior
```bash
$ medf pack nonexistent.medf.json
[Error] File not found: nonexistent.medf.json

Did you mean one of these?
  • document.medf.json
  • paper.medf.json
  • research.medf.json

Or create a new document:
  medf init > nonexistent.medf.json

For help:
  medf pack --help
```

### Implementation
```python
def suggest_similar_files(filename: str) -> list:
    """Suggest similar filenames in current directory"""
    from difflib import get_close_matches
    medf_files = list(Path(".").glob("*.medf.json"))
    filenames = [f.name for f in medf_files]
    return get_close_matches(filename, filenames, n=3, cutoff=0.6)
```

---

## Improvement 8: Verbose Output Mode

### Proposed Behavior
```bash
$ medf pack document.medf.json --verbose
[DEBUG] Loading document: document.medf.json
[DEBUG] Document ID: my-paper-2026
[DEBUG] Found 3 blocks: introduction, methodology, results
[DEBUG] Calculating block hashes...
[DEBUG]   ✓ introduction: sha256:abc123...
[DEBUG]   ✓ methodology: sha256:def456...
[DEBUG]   ✓ results: sha256:ghi789...
[DEBUG] Calculating document hash...
[DEBUG]   ✓ doc_hash: sha256:xyz789...
[DEBUG] Writing updated document...
[OK] Hashes generated: document.medf.json
  Blocks: 3
  Document hash: sha256:xyz789...
```

### Implementation
```python
def cmd_pack(path: Path, ipfs: bool = False, verbose: bool = False):
    """Generate hashes with optional verbose output"""
    if verbose:
        print(f"[DEBUG] Loading document: {path}")
    
    doc = json.loads(path.read_text(encoding="utf-8"))
    
    if verbose:
        print(f"[DEBUG] Document ID: {doc.get('id')}")
        block_ids = [b.get('block_id') for b in doc.get('blocks', [])]
        print(f"[DEBUG] Found {len(block_ids)} blocks: {', '.join(block_ids)}")
        print(f"[DEBUG] Calculating block hashes...")
    
    # ... rest of logic ...
```

---

## Implementation Roadmap

### Phase 1: Quick Wins (1-2 weeks)
- ✅ Per-command help (`--help` for each command)
- ✅ Enhanced error messages with suggestions
- ✅ Verbose output mode (`--verbose`)

### Phase 2: IPFS Integration (1-2 weeks)
- ✅ IPFS CID calculation (v0 and v1)
- ✅ Gateway URL generation
- ✅ `--ipfs` flag for pack command

### Phase 3: User Experience (2-3 weeks)
- ✅ Interactive mode for beginners
- ✅ Progress indicators for large files
- ✅ Configuration file support

### Phase 4: Advanced Features (2-3 weeks)
- ✅ Batch processing
- ✅ Workflow templates
- ✅ Integration with common tools

---

## Testing Strategy

```bash
# Test per-command help
python3 medf.py pack --help
python3 medf.py verify --help

# Test IPFS CID generation
python3 medf.py pack document.medf.json --ipfs
python3 medf.py pack document.medf.json --ipfs --verbose

# Test interactive mode
python3 medf.py --interactive

# Test batch processing
python3 medf.py pack *.medf.json --batch

# Test error handling
python3 medf.py pack nonexistent.medf.json
```

---

## Backward Compatibility

All improvements are **100% backward compatible**:
- Existing commands work unchanged
- New flags are optional
- Default behavior unchanged
- No breaking changes to output format

---

## Dependencies

**No new external dependencies required**:
- `base58` - Already used in IPFS ecosystem, but can use pure Python implementation
- `hashlib` - Built-in
- `json` - Built-in
- `pathlib` - Built-in

---

## Next Steps

1. **Review & Feedback** - Get community feedback on proposed improvements
2. **Implementation** - Start with Phase 1 (quick wins)
3. **Testing** - Comprehensive test suite
4. **Documentation** - Update docs with new features
5. **Release** - Version 0.3.0 with all improvements

---

**Goal**: Make medf.py the easiest way to create, verify, and share verifiable documents.
