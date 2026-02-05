# MeDF Position on AI-Generated Documents

**MeDF (Mutable Expression Description Format)**

MeDF stands for **Mutable Expression Description Format**.

---

> **The problem with AI documents is not "AI wrote this"**
> **The essence is "provenance and responsibility cannot be verified"**
> **MeDF fixes "when, who, and with what intent"**

---

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

## 4. Why Not Rely on Watermarks or AI Detection?

AI detection and watermarking technologies have structural limitations:

* Detection breaks with model updates
* Lost through translation or summarization
* Does not work offline
* Vendor-dependent

MeDF avoids these issues,
establishing trust through **document structure and cryptographic verification.**

---

## 5. Use Cases

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

## 6. MeDF's Answer

> **AI-generated documents are not dangerous.**
> **Dangerous documents are those that cannot be verified.**

MeDF implements **accountability, provenance, and verifiability**
for documents in the AI era at the format level.

---

## 7. One-Line Summary

**MeDF is not a mechanism to stop AI —**
**it is a mechanism that keeps documents trustworthy even in the AI era.**

---

## Appendix: provenance (Optional Extension)

AI usage recording is optional but can be documented for transparency.

**Important**: This is **optional metadata** only and does not affect document validity or verification results.

### Example

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

### Positioning

* ✅ **Can be recorded for transparency**
* ✅ **Useful as reference for provenance tracking**
* ❌ **Not required for verification**
* ❌ **Presence or absence does not affect validity**

MeDF is not an "AI confession format" — it is, first and foremost, **a format for fixing document state**.
