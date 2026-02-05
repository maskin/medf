#!/usr/bin/env python3
"""
medf — A CLI tool to package, hash, sign, and verify documents
       in Mutable Expression Description Format (MEDF).

MEDF helps you make documents verifiable.
It does not decide what is correct, official, or authoritative.
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

# Version
VERSION = "0.2.1"


def canonical_json(obj) -> bytes:
    """
    Convert object to canonical JSON bytes following RFC 8785 (JCS).

    NORMATIVE: MeDF canonicalization MUST follow RFC 8785.
    See: https://www.rfc-editor.org/rfc/rfc8785.html

    Implementation:
    - UTF-8 encoding
    - Sorted keys (lexical order)
    - No whitespace (separators=(",", ":"))
    - Unicode characters preserved (ensure_ascii=False)
    """
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
    """
    Initialize a MEDF document skeleton.
    No existing content is modified.
    """
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


def cmd_pack(path: Path):
    """
    Generate hashes for all blocks and the document.

    This command creates a verifiable snapshot.
    It does NOT freeze your workflow.
    You can always create a new version by repacking.
    """
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

    print(f"[OK] Hashes generated: {path}")
    print(f"  Blocks: {len(doc['blocks'])}")
    print(f"  Document hash: {doc['doc_hash']['value'][:16]}...")


def cmd_verify(path: Path, explain: bool = False, json_output: bool = False):
    """
    Verify block hashes, document hash, and signature.

    Verification checks integrity and consistency.
    Trust decisions are not evaluated.
    """
    doc = json.loads(path.read_text(encoding="utf-8"))

    # Verify blocks
    failed_block = None
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
            failed_block = {
                "block_id": block["block_id"],
                "expected": expected,
                "actual": actual
            }
            break

    if failed_block:
        result = {
            "result": "error",
            "error": "block_hash_mismatch",
            "block_id": failed_block["block_id"],
            "expected": f"sha256:{failed_block['expected'][:16]}...",
            "actual": f"sha256:{failed_block['actual'][:16]}..."
        }
        if json_output:
            print(json.dumps(result, indent=2))
        else:
            print("✖ Block hash mismatch")
            print()
            print("Details:")
            print(f"  block_id: {failed_block['block_id']}")
            print(f"  expected: sha256:{failed_block['expected'][:16]}...")
            print(f"  actual:   sha256:{failed_block['actual'][:16]}...")
            print()
            print("The text content of this block has been altered.")
        return

    # Verify document hash
    if "doc_hash" not in doc:
        if json_output:
            print(json.dumps({"result": "error", "error": "no_document_hash"}, indent=2))
        else:
            print("✖ No document hash found")
        return

    expected = doc["doc_hash"]["value"]
    doc_src = {
        k: v for k, v in doc.items()
        if k not in ("doc_hash", "signature", "index")
    }
    actual = sha256_hex(canonical_json(doc_src))
    if expected != actual:
        if json_output:
            print(json.dumps({"result": "error", "error": "document_hash_mismatch"}, indent=2))
        else:
            print("✖ Document hash mismatch")
            print()
            print("The document structure has been altered.")
        return

    # Verify signature (if present)
    has_signature = "signature" in doc
    signature_valid = None

    if has_signature:
        if not HAS_NACL:
            signature_valid = "skipped"
        else:
            try:
                sig = doc["signature"]
                public_key = VerifyKey(sig["public_key"].encode("utf-8"))
                hash_value = doc["doc_hash"]["value"].encode("utf-8")
                public_key.verify(hash_value, sig["value"].encode("utf-8"))
                signature_valid = True
            except Exception:
                if json_output:
                    print(json.dumps({"result": "error", "error": "signature_verification_failed"}, indent=2))
                else:
                    print("✖ Signature verification failed")
                    print()
                    print("The signature does not match the document hash.")
                return

    # Success output
    if json_output:
        result = {
            "result": "ok",
            "integrity": "verified",
            "checked": {
                "document_hash": True,
                "block_hashes": True
            }
        }

        if has_signature and signature_valid is True:
            result["reproducibility"] = "verified"
            result["signature"] = {
                "present": True,
                "valid": True
            }
            result["trust_decision"] = "not_evaluated"
        elif has_signature and signature_valid == "skipped":
            result["signature"] = {
                "present": True,
                "valid": None
            }
            result["trust_decision"] = "not_evaluated"
        else:
            result["signature"] = {
                "present": False
            }
            result["trust_decision"] = "not_applicable"

        print(json.dumps(result, indent=2))
    else:
        print("✔ Document hash matches")
        print("✔ All block hashes match")

        if has_signature and signature_valid is True:
            print("✔ Signature is cryptographically valid")
            print()
            print("Summary:")
            print("  Integrity: verified")
            print("  Reproducibility: verified")
            print("  Trust decision: not evaluated")
        elif has_signature and signature_valid == "skipped":
            print("⚠ Signature present (PyNaCl not installed)")
            print()
            print("Summary:")
            print("  Integrity: verified")
            print("  Signature: present (not verified)")
            print("  Trust decision: not evaluated")
        else:
            print()
            print("Summary:")
            print("  Integrity: verified")
            print("  Signature: not present")
            print("  Trust decision: not applicable")

        if explain:
        print()
        print("="*60)
        if has_signature and signature_valid is True:
            print("This MEDF document is verifiable because:")
            print("- Each content block matches its recorded hash")
            print("- The document hash matches the signed value")
            print("- The signature matches the embedded public key")
        else:
            print("This MEDF document is verifiable because:")
            print("- Each content block matches its recorded hash")
            print("- The document hash is computable and reproducible")

        print()
        print("This verification does NOT evaluate:")
        print("- Who owns the signing key" if has_signature else "- Key ownership or authority")
        print("- Whether the signer is authoritative" if has_signature else "- Content authorship")
        print("- Whether the content is correct")
        print("="*60)



def cmd_sign(path: Path, key_path: Path):
    """
    Attach a cryptographic signature to the document hash.

    A signature proves integrity, not authority.
    """
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
        print("Run 'medf pack' first")
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

    print(f"[OK] Signature attached: {path}")
    print(f"  Algorithm: ed25519")
    print(f"  Signer: {doc['signature']['public_key'][:40]}...")


def cmd_explain():
    """
    Explain what MEDF verification guarantees.

    MEDF verification means:
    - The text content has not been altered
    - The document structure matches the signed hash
    - The signature is cryptographically valid

    MEDF verification does NOT mean:
    - The signer is authoritative
    - The content is correct
    - The document should be trusted
    """
    print("="*60)
    print("What MEDF Verification Means")
    print("="*60)
    print()
    print("MEDF verification means:")
    print("✓ The text content has not been altered")
    print("✓ The document structure matches the signed hash")
    print("✓ The signature is cryptographically valid (if present)")
    print()
    print("MEDF verification does NOT mean:")
    print("✗ The signer is authoritative")
    print("✗ The content is correct")
    print("✗ The document should be trusted")
    print()
    print("Key principles:")
    print("• Text content is immutable once published")
    print("• Presentation (rendering, indexing) is mutable")
    print("• All hashing uses RFC 8785 (JSON Canonicalization Scheme)")
    print("• MEDF does not define trust authorities or key ownership")
    print()
    print("For more information:")
    print("• Philosophy: see PHILOSOPHY.md")
    print("• Trust anchors: see docs/trust.md")
    print("="*60)


def print_usage():
    """Print usage information"""
    print("medf — A CLI tool to package, hash, sign, and verify documents")
    print("       in Mutable Expression Description Format (MEDF).")
    print()
    print("MEDF helps you make documents verifiable.")
    print("It does not decide what is correct, official, or authoritative.")
    print()
    print("USAGE:")
    print("  medf <command> [options]")
    print()
    print("COMMANDS:")
    print("  init        Initialize a MEDF document skeleton")
    print("  pack        Generate hashes for blocks and the document")
    print("  sign        Attach a cryptographic signature to the document hash")
    print("  verify      Verify hashes and signatures")
    print("  explain     Explain what MEDF verification means")
    print()
    print("GLOBAL OPTIONS:")
    print("  --help      Show this help message")
    print("  --version   Show version information")
    print()
    print("VERIFICATION OPTIONS:")
    print("  --explain    Explain verification results in plain language")
    print("  --json      Output verification results as JSON")
    print()
    print("NOTES:")
    print("  • Text content in MEDF blocks is immutable once published.")
    print("  • Presentation (rendering, indexing, layout) is mutable.")
    print("  • All hashing and signing uses RFC 8785 (JSON Canonicalization Scheme).")
    print("  • MEDF does not define trust authorities or key ownership.")
    print()
    print("EXAMPLES:")
    print("  medf init > document.medf.json")
    print("  medf pack document.medf.json")
    print("  medf verify document.medf.json")
    print("  medf verify document.medf.json --explain")
    print("  medf verify document.medf.json --json")
    print("  medf sign document.medf.json --key private.key")
    print("  medf explain")
    print()
    print("For more information:")
    print("  https://github.com/maskin/medf")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    # Handle --version and --help
    if sys.argv[1] in ["--version", "-v"]:
        print(f"medf {VERSION}")
        print()
        print("MEDF adopts RFC 8785 (JSON Canonicalization Scheme) for all hashing.")
        print("See: https://www.rfc-editor.org/rfc/rfc8785.html")
        return

    if sys.argv[1] in ["--help", "-h"]:
        print_usage()
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "pack":
        if len(sys.argv) < 3:
            print("usage: medf pack <document.medf>")
            return
        path = Path(sys.argv[2])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return
        cmd_pack(path)
    elif cmd == "hash":
        # Legacy support for old 'hash' command
        if len(sys.argv) < 3:
            print("Note: 'hash' command is deprecated. Use 'pack' instead.")
            print("usage: medf pack <document.medf>")
            return
        print("[Warning] 'hash' command is deprecated. Use 'pack' instead.")
        path = Path(sys.argv[2])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return
        cmd_pack(path)
    elif cmd == "verify":
        explain = "--explain" in sys.argv
        json_output = "--json" in sys.argv
        if len(sys.argv) < 3:
            print("usage: medf verify <document.medf> [--explain] [--json]")
            return
        path = Path(sys.argv[2])
        if not path.exists():
            print(f"[Error] File not found: {path}")
            return
        cmd_verify(path, explain=explain, json_output=json_output)
    elif cmd == "sign":
        if len(sys.argv) < 4:
            print("usage: medf sign <document.medf> --key <private-key>")
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
    elif cmd == "explain":
        cmd_explain()
    else:
        print(f"[Error] Unknown command: {cmd}")
        print()
        print("Run 'medf --help' for usage information.")


if __name__ == "__main__":
    main()
