#!/usr/bin/env python3
"""
MeDF MVP Implementation
python3.10+

Usage:
    python3 medf.py init
    python3 medf.py hash file.medf.json
    python3 medf.py verify file.medf.json
"""

import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone


def canonical_json(obj) -> bytes:
    """Convert object to canonical JSON bytes"""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    """Calculate SHA-256 hash and return as hex string"""
    return hashlib.sha256(data).hexdigest()


def cmd_init():
    """Initialize a new MeDF document template"""
    doc = {
        "medf_version": "0.2.1",
        "id": "example-doc",
        "snapshot": datetime.now(timezone.utc).isoformat(),
        "issuer": "example",
        "blocks": [
            {
                "block_id": "example",
                "role": "body",
                "format": "markdown",
                "text": "Hello MEDF"
            }
        ]
    }
    print(json.dumps(doc, indent=2, ensure_ascii=False))


def cmd_hash(path: Path):
    """Calculate hashes for blocks and document"""
    doc = json.loads(path.read_text(encoding="utf-8"))

    # Calculate block_hash
    for block in doc.get("blocks", []):
        block_src = {
            "block_id": block["block_id"],
            "role": block["role"],
            "format": block["format"],
            "text": block["text"],
        }
        block["block_hash"] = sha256_hex(canonical_json(block_src))

    # Calculate doc_hash (excluding index/signature)
    doc_src = {
        k: v for k, v in doc.items()
        if k not in ("doc_hash", "signature", "index")
    }
    doc["doc_hash"] = {
        "algorithm": "sha-256",
        "value": sha256_hex(canonical_json(doc_src))
    }

    # Write updated document
    path.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def cmd_verify(path: Path):
    """Verify document integrity"""
    doc = json.loads(path.read_text(encoding="utf-8"))

    # Verify blocks
    for block in doc.get("blocks", []):
        expected = block.get("block_hash")
        if not expected:
            continue

        block_src = {
            "block_id": block["block_id"],
            "role": block["role"],
            "format": block["format"],
            "text": block["text"],
        }
        actual = sha256_hex(canonical_json(block_src))
        if expected != actual:
            print(f"[NG] block {block['block_id']}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
            return

    # Verify document hash
    expected = doc["doc_hash"]["value"]
    doc_src = {
        k: v for k, v in doc.items()
        if k not in ("doc_hash", "signature", "index")
    }
    actual = sha256_hex(canonical_json(doc_src))
    if expected != actual:
        print("[NG] document hash")
        print(f"  Expected: {expected}")
        print(f"  Actual: {actual}")
        return

    print("[OK] verified")


def main():
    if len(sys.argv) < 2:
        print("usage: medf init|hash|verify [file]")
        print("")
        print("Commands:")
        print("  init           Show template document")
        print("  hash <file>    Calculate hashes")
        print("  verify <file>  Verify document integrity")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd in ("hash", "verify"):
        if len(sys.argv) < 3:
            print(f"usage: medf {cmd} <file>")
            return

        path = Path(sys.argv[2])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return

        if cmd == "hash":
            cmd_hash(path)
        else:
            cmd_verify(path)
    else:
        print(f"[Error] Unknown command: {cmd}")


if __name__ == "__main__":
    main()
