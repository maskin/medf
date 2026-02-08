# MeDF Examples and Use Cases

This document shows practical examples of how to use MeDF for different scenarios.

## Table of Contents

1. [Academic Paper](#academic-paper)
2. [News Article](#news-article)
3. [Government Document](#government-document)
4. [Research Report](#research-report)
5. [Technical Specification](#technical-specification)
6. [Blog Post](#blog-post)
7. [Collaborative Document](#collaborative-document)

---

## Academic Paper

**Use case**: Publishing a peer-reviewed paper with verifiable authorship and block-level citations.

```json
{
  "medf_version": "0.2.1",
  "id": "paper-2026-quantum-entanglement",
  "snapshot": "2026-02-08T10:00:00Z",
  "issuer": "alice@university.edu",
  "blocks": [
    {
      "block_id": "title",
      "role": "body",
      "format": "markdown",
      "text": "# Quantum Entanglement in Distributed Systems\n\nAlice Smith, Bob Johnson, Carol Lee",
      "block_hash": ""
    },
    {
      "block_id": "abstract",
      "role": "body",
      "format": "markdown",
      "text": "## Abstract\n\nWe present a novel approach to quantum entanglement in distributed systems...",
      "block_hash": ""
    },
    {
      "block_id": "introduction",
      "role": "body",
      "format": "markdown",
      "text": "## Introduction\n\nQuantum computing has revolutionized...\n\nAs discussed in MEDF: paper-2025-quantum-basics#methodology, the foundation of our work...",
      "block_hash": ""
    },
    {
      "block_id": "methodology",
      "role": "body",
      "format": "markdown",
      "text": "## Methodology\n\nOur experimental setup consists of:\n\n1. Quantum processor (IBM Q)\n2. Classical control system\n3. Measurement apparatus",
      "block_hash": ""
    },
    {
      "block_id": "results",
      "role": "body",
      "format": "markdown",
      "text": "## Results\n\nOur experiments show a 40% improvement in entanglement fidelity...",
      "block_hash": ""
    },
    {
      "block_id": "discussion",
      "role": "body",
      "format": "markdown",
      "text": "## Discussion\n\nThese results align with theoretical predictions from MEDF: paper-2025-theory#predictions...",
      "block_hash": ""
    },
    {
      "block_id": "references",
      "role": "appendix",
      "format": "markdown",
      "text": "## References\n\n1. MEDF: paper-2025-quantum-basics#abstract\n2. MEDF: paper-2025-theory#predictions\n3. Smith et al. (2025) - Previous work\n4. Johnson (2024) - Related research",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  }
}
```

**Workflow**:
```bash
# Create and hash
python3 medf.py pack paper-2026-quantum-entanglement.medf.json

# Sign with author key
python3 medf.py sign paper-2026-quantum-entanglement.medf.json --key alice-key.pem

# Publish to IPFS
ipfs add paper-2026-quantum-entanglement.medf.json
# QmXxxx...

# Share citation
# MEDF: paper-2026-quantum-entanglement#methodology
```

---

## News Article

**Use case**: Publishing news with version tracking and correction history.

```json
{
  "medf_version": "0.2.1",
  "id": "news-2026-02-08-tech-breakthrough",
  "snapshot": "2026-02-08T15:30:00Z",
  "issuer": "newsroom@example.com",
  "blocks": [
    {
      "block_id": "headline",
      "role": "body",
      "format": "markdown",
      "text": "# Major Breakthrough in AI Safety Research\n\nFebruary 8, 2026",
      "block_hash": ""
    },
    {
      "block_id": "lede",
      "role": "body",
      "format": "markdown",
      "text": "## Summary\n\nResearchers at leading institutions announced a major breakthrough in AI safety...",
      "block_hash": ""
    },
    {
      "block_id": "body",
      "role": "body",
      "format": "markdown",
      "text": "## Full Story\n\nThe research, conducted over 18 months, demonstrates...",
      "block_hash": ""
    },
    {
      "block_id": "expert-quote",
      "role": "body",
      "format": "markdown",
      "text": "## Expert Commentary\n\n\"This is a game-changer,\" said Dr. Jane Smith, director of the AI Ethics Institute.",
      "block_hash": ""
    },
    {
      "block_id": "corrections",
      "role": "appendix",
      "format": "markdown",
      "text": "## Corrections\n\n**v1.0** (2026-02-08 15:30): Initial publication\n**v1.1** (2026-02-08 16:45): Corrected institution name from \"AI Institute\" to \"AI Ethics Institute\"\n**v1.2** (2026-02-08 17:00): Added expert quote",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  }
}
```

**Key features**:
- Each version gets a new IPFS hash
- Corrections are documented in the document itself
- Readers can verify the document hasn't been secretly modified
- Version history is transparent

---

## Government Document

**Use case**: Official regulation with cryptographic signature and offline verification.

```json
{
  "medf_version": "0.2.1",
  "id": "regulation-2026-data-privacy",
  "snapshot": "2026-02-08T09:00:00Z",
  "issuer": "government-ministry@country.gov",
  "blocks": [
    {
      "block_id": "title",
      "role": "body",
      "format": "markdown",
      "text": "# Data Privacy Regulation 2026\n\nOfficial Document\nEffective Date: March 1, 2026",
      "block_hash": ""
    },
    {
      "block_id": "section-1",
      "role": "body",
      "format": "markdown",
      "text": "## Section 1: Definitions\n\n**Personal Data**: Any information relating to an identified or identifiable person...",
      "block_hash": ""
    },
    {
      "block_id": "section-2",
      "role": "body",
      "format": "markdown",
      "text": "## Section 2: Rights and Obligations\n\nOrganizations must:\n1. Obtain explicit consent\n2. Provide data access upon request\n3. Implement security measures",
      "block_hash": ""
    },
    {
      "block_id": "penalties",
      "role": "body",
      "format": "markdown",
      "text": "## Penalties\n\nViolations result in fines up to €50,000 or 5% of annual revenue...",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  },
  "signature": {
    "algorithm": "rsa-sha256",
    "value": "...",
    "issuer_key": "government-ministry-public-key.pem"
  }
}
```

**Verification workflow**:
```bash
# Citizen downloads document
ipfs get QmXxxx > regulation.medf.json

# Verify without internet
python3 medf.py verify regulation.medf.json
# ✓ Document verified
# ✓ Signature valid

# Verify government signature
python3 medf.py verify regulation.medf.json --key government-public-key.pem
# ✓ Signed by government-ministry@country.gov
```

---

## Research Report

**Use case**: Internal research report with multiple sections and data references.

```json
{
  "medf_version": "0.2.1",
  "id": "report-2026-market-analysis",
  "snapshot": "2026-02-08T14:00:00Z",
  "issuer": "research-team@company.com",
  "blocks": [
    {
      "block_id": "executive-summary",
      "role": "body",
      "format": "markdown",
      "text": "## Executive Summary\n\nMarket analysis shows 15% growth in Q4 2025...",
      "block_hash": ""
    },
    {
      "block_id": "methodology",
      "role": "body",
      "format": "markdown",
      "text": "## Methodology\n\nWe analyzed 10,000 data points from...",
      "block_hash": ""
    },
    {
      "block_id": "findings",
      "role": "body",
      "format": "markdown",
      "text": "## Key Findings\n\n1. Customer retention improved by 20%\n2. Market share increased in APAC region\n3. New product adoption exceeded forecasts",
      "block_hash": ""
    },
    {
      "block_id": "appendix-data",
      "role": "appendix",
      "format": "markdown",
      "text": "## Appendix: Raw Data\n\nDetailed dataset available at: https://data.company.com/q4-2025\n\nData hash: sha256:abc123...\n(for verification)",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  }
}
```

---

## Technical Specification

**Use case**: API specification with versioning and change tracking.

```json
{
  "medf_version": "0.2.1",
  "id": "spec-api-v2",
  "snapshot": "2026-02-08T11:00:00Z",
  "issuer": "engineering@company.com",
  "blocks": [
    {
      "block_id": "overview",
      "role": "body",
      "format": "markdown",
      "text": "# API v2 Specification\n\n**Version**: 2.0\n**Status**: Stable\n**Release Date**: 2026-02-08",
      "block_hash": ""
    },
    {
      "block_id": "authentication",
      "role": "body",
      "format": "markdown",
      "text": "## Authentication\n\nAll requests must include Bearer token:\n\n```\nAuthorization: Bearer YOUR_TOKEN\n```",
      "block_hash": ""
    },
    {
      "block_id": "endpoints",
      "role": "body",
      "format": "markdown",
      "text": "## Endpoints\n\n### GET /api/v2/users/{id}\n\nRetrieve user by ID.\n\n**Parameters**:\n- `id` (string, required): User ID\n\n**Response**:\n```json\n{\n  \"id\": \"user-123\",\n  \"name\": \"John Doe\"\n}\n```",
      "block_hash": ""
    },
    {
      "block_id": "changelog",
      "role": "appendix",
      "format": "markdown",
      "text": "## Changelog\n\n**v2.0** (2026-02-08): Initial release\n- Added authentication\n- Added user endpoints\n- Added rate limiting\n\n**v1.5** (2025-12-15): Previous version\n- See MEDF: spec-api-v1.5#changelog",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  }
}
```

---

## Blog Post

**Use case**: Personal blog post with comments and discussion.

```json
{
  "medf_version": "0.2.1",
  "id": "blog-2026-future-web",
  "snapshot": "2026-02-08T12:00:00Z",
  "issuer": "alice@blog.example.com",
  "blocks": [
    {
      "block_id": "post",
      "role": "body",
      "format": "markdown",
      "text": "# The Future of the Web is Decentralized\n\nFebruary 8, 2026\n\nThe web is changing. Instead of centralized platforms...",
      "block_hash": ""
    },
    {
      "block_id": "discussion",
      "role": "body",
      "format": "markdown",
      "text": "## Discussion\n\n**Comment 1** (Bob): \"Great post! I agree that decentralization is important.\"\n\n**Comment 2** (Carol): \"But what about user experience? MEDF: blog-2026-future-web#post\"\n\n**Reply** (Alice): \"Good point! See MEDF: blog-2026-ux-challenges#usability for more on this.\"",
      "block_hash": ""
    }
  ],
  "doc_hash": {
    "algorithm": "sha-256",
    "value": ""
  }
}
```

---

## Collaborative Document

**Use case**: Document edited by multiple authors with version history.

```bash
# Author 1: Alice creates document
python3 medf.py init > collaborative-doc.medf.json

# Alice edits and hashes
python3 medf.py pack collaborative-doc.medf.json

# Alice signs
python3 medf.py sign collaborative-doc.medf.json --key alice-key.pem

# Alice publishes
ipfs add collaborative-doc.medf.json
# QmAAA...

# Author 2: Bob downloads and edits
ipfs get QmAAA > collaborative-doc-v2.medf.json

# Bob makes changes, hashes, and signs
python3 medf.py pack collaborative-doc-v2.medf.json
python3 medf.py sign collaborative-doc-v2.medf.json --key bob-key.pem

# Bob publishes new version
ipfs add collaborative-doc-v2.medf.json
# QmBBB...

# Version history:
# QmAAA... (Alice's version)
# QmBBB... (Bob's version)
# Both verifiable, both signed, both immutable
```

---

## Tips for Your Own Documents

1. **Choose meaningful block IDs**: Use `introduction`, `methodology`, not `block-1`
2. **Use semantic roles**: `body` for main content, `appendix` for supplementary
3. **Keep blocks focused**: One idea per block for better referenceability
4. **Document changes**: Use appendix to track versions and corrections
5. **Sign important documents**: Proves authorship and prevents tampering
6. **Publish to IPFS**: Share with confidence that content won't disappear

---

## Next Steps

- Try the [Getting Started](GETTING_STARTED.md) guide
- Explore [IPFS Integration](IPFS_INTEGRATION.md)
- Read [PHILOSOPHY.md](../PHILOSOPHY.md) for design principles
- Check out [examples/](../examples/) for complete working documents

---

Happy documenting! 🚀
