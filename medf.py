#!/usr/bin/env python3
"""
MeDF MVP Implementation
python3.10+

Usage:
    python3 medf.py init
    python3 medf.py hash file.medf.json
    python3 medf.py verify file.medf.json
    python3 medf.py sign file.medf.json --key private.key
"""

import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone

try:
    from nacl.signing import SigningKey, VerifyKey
    from nacl.exceptions import BadSignatureError
    HAS_NACL = True
except ImportError:
    HAS_NACL = False


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
    if "doc_hash" not in doc:
        print("[NG] No doc_hash found")
        return

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


def cmd_sign(path: Path, key_path: Path):
    """Sign document with private key"""
    if not HAS_NACL:
        print("[Error] PyNaCl is required for signing")
        print("Install: pip install pynacl")
        sys.exit(1)

    doc = json.loads(path.read_text(encoding="utf-8"))

    # Read private key
    try:
        key = SigningKey.load(key_path.read_bytes())
    except Exception as e:
        print(f"[Error] Failed to load private key: {e}")
        sys.exit(1)

    # Sign doc_hash.value
    if "doc_hash" not in doc:
        print("[Error] No doc_hash found to sign")
        print("Run 'medf hash' first")
        sys.exit(1)

    hash_value = doc["doc_hash"]["value"]
    message = hash_value.encode("utf-8")

    # Sign
    signature_bytes = key.sign(message)
    signature_value = signature_bytes.decode("utf-8")

    # Get public key
    public_key = key.verify_key

    doc["signature"] = {
        "algorithm": "ed25519",
        "value": signature_value,
        "public_key": public_key.encode().decode("utf-8"),
        "signed_at": datetime.now(timezone.utc).isoformat()
    }

    # Write updated document
    path.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"[OK] signed: {path}")
    print(f"  Algorithm: ed25519")
    print(f"  Signer: {doc['signature']['public_key'][:40]}...")


def main():
    if len(sys.argv) < 2:
        print("usage: medf init|hash|verify|sign [file] [options]")
        print("")
        print("Commands:")
        print("  init                    Show template document")
        print("  hash <file>             Calculate hashes")
        print("  verify <file>           Verify document integrity")
        print("  sign <file> --key <key>  Sign document")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "hash":
        if len(sys.argv) < 3:
            print("usage: medf hash <file>")
            return
        path = Path(sys.argv[2])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return
        cmd_hash(path)
    elif cmd == "verify":
        if len(sys.argv) < 3:
            print("usage: medf verify <file>")
            return
        path = Path(sys.argv[2])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return
        cmd_verify(path)
    elif cmd == "sign":
        if len(sys.argv) < 4:
            print("usage: medf sign <file> --key <private_key>")
            return
        path = Path(sys.argv[2])
        key_path = Path(sys.argv[4])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return
        if not key_path.exists():
            print(f"[Error] Key file not found: {key_path}")
            return
        cmd_sign(path, key_path)
    else:
        print(f"[Error] Unknown command: {cmd}")


if __name__ == "__main__":
    main()
