Internet-Draft                                           MEDF Project
Intended status: Informational                          June 2026
Expires: December 2026

         Mutable Expression Description Format (MEDF)

Abstract

   This document describes the Mutable Expression Description Format
   (MEDF), a document format designed to make textual content verifiable
   while allowing presentation and indexing layers to remain mutable.

   MEDF provides a mechanism for documenting the state of text content at
   specific points in time, enabling detection of unintended or malicious
   changes without specifying correctness, authority, or trust status.

Status of This Memo

   This Internet-Draft is submitted in full conformance with the provisions
   of Section 3 of RFC 7841.

   This document is a product of the IETF MEDF Project and represents the
   consensus of the MEDF community.  It is published for informational
   purposes only.

Copyright Notice

   Copyright (c) 2026 IETF Trust and the persons identified as authors of the
   code.  All rights reserved.

Table of Contents

   1.  Introduction
   2.  Design Goals
   3.  Data Model
   4.  Canonicalization
  5.  Hashing and Signatures
   6.  Verification Model
   7.  What MEDF Does Not Define
   8.  Security Considerations
   9.  IANA Considerations
   10. References

1.  Introduction

   Digital documents are easily altered, whether accidentally or
   maliciously.  While version control systems track changes over time,
   they do not provide cryptographic verification of document state.

   MEDF addresses this by providing a format for documenting the state
   of text content in a verifiable manner.  It focuses on recording when
   content existed and who fixed it, without making claims about
   correctness, authority, or trustworthiness.

   Key characteristics:
   * Text content is immutable once published
   * Presentation, indexing, and interpretation layers are mutable
   * Verification is offline and requires no central infrastructure
   * Hashing uses RFC 8785 (JSON Canonicalization Scheme)
   * Signatures are optional and indicate integrity, not authority

2.  Design Goals

   MEDF was designed with the following goals in mind:

   * Make text content verifiable without requiring online services
   * Separate immutable text from mutable presentation
   * Enable precise, block-level references and citations
   * Remain compatible with existing tools and formats
   * Avoid defining trust authorities or key management systems
   * Support offline operation and long-term archival

3.  Data Model

   A MEDF document is a JSON object with the following structure:

   * medf_version: Format version identifier
   * id: Document identifier
   * snapshot: Timestamp of document creation
   * issuer: Entity that created the document
   * blocks: Array of semantic text blocks
   * doc_hash: Hash of document content
   * signature (optional): Cryptographic signature

   Each block contains:
   * block_id: Unique identifier
   * role: Block role (e.g., abstract, policy, scope)
   * format: Content format (e.g., markdown)
   * text: Textual content
   * block_hash: Hash of block content

4.  Canonicalization

   MEDF adopts RFC 8785 (JSON Canonicalization Scheme, JCS) as its
   normative canonicalization standard [RFC8785].

   All cryptographic hashes and signatures MUST be computed over RFC 8785-
   canonicalized JSON bytes.  MEDF does not define its own canonicalization
   rules.

5.  Hashing and Signatures

   MEDF uses SHA-256 for hashing block and document content.

   Signatures use ed25519 and are computed over the document hash value.
   Signatures are optional and indicate cryptographic integrity, not
   authority or correctness.

6.  Verification Model

   Verification checks:
   * Block hashes match recorded values
   * Document hash matches content
   * Signature is cryptographically valid (if present)

   Verification does NOT evaluate:
   * Who owns the signing key
   * Whether the signer is authoritative
   * Whether the content is correct
   * Whether the document should be trusted

7.  What MEDF Does Not Define

   MEDF intentionally does not define:

   * Trust authorities or identity verification
   * Key management or revocation mechanisms
   * Content correctness or authenticity
   * Legal or regulatory validity

   These concerns are considered application-layer responsibilities and are
   left outside the scope of the format specification.

8.  Security Considerations

   MEDF provides integrity verification but does not guarantee content
   correctness or authority.  Users must evaluate trust based on external
   factors such as key ownership, signer identity, and content validation.

   The cryptographic strength of MEDF depends on:
   * SHA-256 collision resistance
   * ed25519 signature security
   * Proper key management practices

9.  IANA Considerations

   This document has no IANA actions.

10. References

   [RFC8785]  Andersen, P., "JSON Canonicalization Scheme (JCS)",
              RFC 8785, June 2020.

Authors' Addresses

   MEDF Project
   Email: medf@example.com

   GitHub: https://github.com/maskin/medf
