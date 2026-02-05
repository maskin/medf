# MeDF Philosophy (v0.1)

## 1. What MeDF Is

MeDF (Mutable Expression Description Format) is **not** a system for preserving, distributing, or evaluating documents.

What MeDF handles is the **description of a state** — "that a document existed at a certain point in time, with certain intent."

---

## 2. Does Not Determine Correctness

MeDF does **not** do the following:

- Judge truth or falsehood
- Evaluate content
- Grant authority
- Determine superiority

MeDF does not ask "Is this correct?" but rather fixes "**when, who, and with what intent** this existed."

---

## 3. Premise of External Storage

MeDF does not hold document content itself.

- Documents may exist anywhere: local files, Git, web, PDF, print media, etc.
- MeDF **references** these and **points to them with hashes**

This enables freedom from storage methods, distribution methods, and display methods.

---

## 4. Hash as Boundary of Responsibility

In MeDF, hashes are for detecting tampering — **not for guaranteeing trustworthiness or legitimacy**.

What a hash shows is only the fact that "it has not changed from this state."

---

## 5. History Represented as Chains

MeDF does **not** overwrite updates.

- Each state is linked by `previous`
- History may branch
- No "official" history exists

History is material for discussion — it does not need to be unified.

---

## 6. Offline-First

MeDF assumes the following:

- No network connection required
- No central servers required
- No external APIs required

Online services are **optional** — not a condition for MeDF to function.

---

## 7. Why JSON?

JSON is not a philosophy but a **compromise**.

- Human-readable
- Machine-processable
- CLI-generatable
- Future-convertible to other formats

MeDF is not locked into JSON.

---

## 8. What MeDF Aims For

MeDF aims for a world where the following can be handled as history — **separated from evaluation**:

- Academic papers
- Public documents
- Specifications
- Articles
- Personal notes

This is "recording that does not force trust."

---

## Q&A (Philosophy Defense)

### Q: Is this blockchain?

**A: No. Consensus and distribution are not required.**

- Blockchain is a consensus protocol
- MeDF is a state description format
- Distributed consensus is optional

### Q: Can't I trust this?

**A: We operate on a no-trust premise.**

- Trustworthiness is an external concern
- MeDF records "what existed"
- Left to user judgment

### Q: Weak authentication?

**A: We don't authenticate. We only fix state.**

- Signatures show "who fixed"
- Don't prove content correctness
- Record of fact: "at this point, it was like this"

### Q: Wouldn't central management be more convenient?

**A: We prioritize resilience over convenience.**

- Central servers are single points of failure (SPOF)
- Offline operation is essential
- Long-term document preservation has risks with central management

👉 All of these return to the core philosophy: MeDF records existence, not truth.

---

## Japanese Version

See [思想.md](思想.md) for the original Japanese version.
