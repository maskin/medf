# MeDF Position on AI-Generated Documents

## 1. Background: Why AI-Generated Documents Are Problematic

The proliferation of generative AI has brought several challenges to light:

* **Unclear authorship, timing, and creation methods**
* Undetectable content modifications after the fact
* No distinction between human-written and AI-generated documents
* Difficult to use in contexts requiring accountability: government, academic papers, contracts

The essential point: **The problem is not "AI wrote this,"**
but rather **"provenance and responsibility cannot be verified."**

MeDF (Mutable Expression Description Format) provides **a format-level answer**
to this structural problem.

---

## 2. MeDF's Basic Principle: Does Not Prohibit AI

MeDF does **not** take a position to prohibit, detect, or exclude AI-generated documents.

Instead, we adopt these principles:

* AI may write
* Humans may edit
* **But must be fixed in a verifiable form**

In MeDF, what matters is **not the creation method,
but verifiability after fixing.**

---

## 3. What Does "Fixing" a Document Mean?

MeDF handles documents as follows:

1. Decompose document into semantic units (blocks)
2. Assign hash values to each block and the entire document
3. Sign those hashes

This ensures:

* Any single-character change is detectable
* Block-level citation and verification
* Offline tamper detection

Whether AI-generated or human-generated,
**"document content at that point in time"** is guaranteed to remain as evidence.

---

## 4. Where Is AI Usage Recorded?

In MeDF, AI usage is treated as **optional metadata**.

Example:

```json
"provenance": {
  "created_by": "human",
  "assisted_by": [
    {
      "type": "ai",
      "model": "gpt-4",
      "role": "drafting"
    }
  ]
}
```

Important points:

* This information **can be recorded for transparency**
* But is **not required for verification**
* Presence or absence does not affect document validity

MeDF is not an "AI confession format."

---

## 5. Why Not Rely on Watermarks or AI Detection?

AI detection and watermarking technologies have structural limitations:

* Detection breaks with model updates
* Lost through translation or summarization
* Does not work offline
* Vendor-dependent

MeDF avoids these issues,
establishing trust through **document structure and cryptographic verification.**

---

## 6. Use Cases

### Government and Official Documents

* AI drafts → Human review → MeDF fixes
* Later verification of "official document at that point in time"

### Academic and Technical Papers

* AI assistance acceptable
* Peer review and citation at fixed block level

### Archives for the AI Era

* Prevents proliferation of "PDFs of unknown origin"
* Leaves records that future generations can verify

---

## 7. MeDF's Answer

> **AI-generated documents are not dangerous.**
> **Dangerous documents are those that cannot be verified.**

MeDF implements **accountability, provenance, and verifiability**
for documents in the AI era at the format level.

---

## 8. One-Line Summary

**MeDF is not a mechanism to stop AI —**
**it is a mechanism that keeps documents trustworthy even in the AI era.**
