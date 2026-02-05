# Trust Anchor Examples

This document describes example trust anchors for MEDF documents.

These are not part of the core specification,
but practical references for experimentation and deployment.

---

## GitHub-based Trust Anchor

A MEDF document MAY be signed with a key
whose public part is published in a GitHub repository.

Trust is anchored in:
- GitHub account ownership
- Repository access control
- Commit history transparency

### Example Usage

1. **Publish Public Key** in a GitHub repository

```json
{
  "public_key": "BASE64_ENCODED_PUBLIC_KEY",
  "owner": "github-username",
  "repository": "repository-name",
  "published_at": "2026-02-05T10:00:00Z"
}
```

2. **Sign Document** with corresponding private key

```bash
python3 medf.py sign document.medf.json --key private.key
```

3. **Verify Trust** by checking:
   - Public key exists in referenced GitHub repository
   - Repository owner is trusted entity
   - Key has not been revoked

### Advantages

- ✅ Transparent and auditable
- ✅ Leverages existing GitHub infrastructure
- ✅ Suitable for open-source projects and public documents
- ✅ No additional infrastructure required

### Limitations

- ⚠️ Requires GitHub account security
- ⚠️ Not suitable for air-gapped environments
- ⚠️ Trust depends on GitHub's reliability

---

## Future Examples

Additional trust anchor examples may be added:
- Organizational PKI
- Platform-based identity (e.g., ORCID, institutional accounts)
- Social proofs (e.g., Web of Trust, key signing parties)
- Hardware security modules (HSMs)

Contributions welcome.
