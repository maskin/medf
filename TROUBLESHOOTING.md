# MEDF Troubleshooting

Common issues and solutions when working with MEDF documents and tools.

---

## CLI Tool Issues

### "command not found: medf"

**Cause**: The `medf` command is not in your PATH.

**Solutions**:
1. **Use python3 directly**:
   ```bash
   python3 medf.py <command>
   ```

2. **Create an alias** (add to `~/.zshrc` or `~/.bashrc`):
   ```bash
   alias medf='python3 /path/to/medf.py'
   source ~/.zshrc  # Reload shell
   ```

3. **Make script executable** (optional):
   ```bash
   chmod +x medf.py
   ./medf.py <command>
   ```

---

### "IndentationError" or "SyntaxError"

**Cause**: Python version incompatible or file corrupted.

**Solutions**:
1. Check Python version (requires Python 3.6+):
   ```bash
   python3 --version
   ```

2. Re-clone repository to ensure clean files:
   ```bash
   git clone https://github.com/maskin/medf.git
   ```

---

## Document Issues

### "Block hash mismatch"

**Cause**: Document content was modified after packing.

**Example error**:
```
✖ Block hash mismatch

Details:
  block_id: methodology
  expected: sha256:abc123...
  actual:   sha256:def456...

The text content of this block has been altered.
```

**Solutions**:
1. **Re-pack the document**:
   ```bash
   python3 medf.py pack document.medf.json
   ```

2. **If you need to preserve the original hash**:
   - Revert changes to the block text
   - Re-verify with original hash

**Prevention**:
- Always modify source Markdown, then re-import
- Don't manually edit `.medf.json` files unless necessary

---

### "No document hash found"

**Cause**: Document was created but not packed.

**Example error**:
```
✖ No document hash found
```

**Solution**:
```bash
python3 medf.py pack document.medf.json
```

**Note**: If using `import` command, packing is automatic:
```bash
# Auto-packs by default
python3 medf.py import document.md

# Skip packing if editing
python3 medf.py import document.md --no-pack
```

---

### "Document hash mismatch"

**Cause**: Document structure was altered after packing.

**Common causes**:
- Added/removed blocks
- Changed `medf_version`, `id`, or `snapshot`
- Modified `blocks` array structure

**Solution**:
```bash
python3 medf.py pack document.medf.json
```

**Prevention**:
- Edit documents before packing
- If you need changes, re-pack after modification

---

## Verification Issues

### "Signature verification failed"

**Cause**: Document content changed after signing, or wrong signature.

**Example error**:
```
✖ Signature verification failed

The signature does not match the document hash.
```

**Solutions**:
1. **If content was modified**: Re-sign the document
   ```bash
   python3 medf.py sign document.medf.json --key private.key
   ```

2. **If signature is wrong**: Remove and re-sign
   ```bash
   # Edit JSON to remove "signature" field
   python3 medf.py sign document.medf.json --key private.key
   ```

**Note**: Signatures are optional. A document can be verified without a signature.

---

## Import Issues

### "File not found" when importing

**Cause**: Incorrect path or file doesn't exist.

**Solution**:
1. Check file path:
   ```bash
   ls -la /path/to/document.md
   ```

2. Use absolute or relative path:
   ```bash
   # Absolute path
   python3 medf.py import /full/path/to/document.md

   # Relative path
   python3 medf.py import ../documents/document.md
   ```

---

### "Only 1 section found" (expected more)

**Cause**: Markdown file doesn't use `##` headers for sections.

**Solution**:
1. Add `##` headers to your Markdown:
   ```markdown
   # Document Title

   ## Section 1
   Content here...

   ## Section 2
   More content...
   ```

2. Or use `--no-pack` and create blocks manually

---

## Performance Issues

### Large file processing is slow

**Cause**: Very large documents with many blocks.

**Solutions**:
1. **Split into smaller documents** by topic
2. **Use `--no-pack`** when editing, pack only when done
3. **Verify specific blocks** instead of entire document (future feature)

---

## JSON Issues

### "JSONDecodeError" when loading document

**Cause**: Corrupted or malformed JSON file.

**Common causes**:
- Missing comma
- Trailing comma (not valid in JSON)
- Unescaped quotes in text

**Solution**:
1. **Validate JSON**:
   ```bash
   python3 -m json.tool document.medf.json > /dev/null
   ```

2. **Fix syntax errors** manually or use JSON validator
3. **Re-create from source**:
   ```bash
   python3 medf.py import source.md
   ```

---

## Encoding Issues

### "UnicodeDecodeError" or encoding errors

**Cause**: File not UTF-8 encoded.

**Solution**:
1. **Convert file to UTF-8**:
   ```bash
   iconv -f ISO-8859-1 -t UTF-8 input.txt > output.md
   ```

2. **Save as UTF-8** in your text editor

**Requirement**: All MEDF files MUST be UTF-8 encoded.

---

## Dependencies

### "Module not found" errors

**PyNaCl not installed** (for signing):
```bash
pip install pynacl
```

**Or use without signing** (signing is optional):
```bash
python3 medf.py verify document.medf.json  # Works without PyNaCl
```

---

## Getting Help

If you're still stuck:

1. **Check documentation**:
   - [README.md](README.md) - Quick start guide
   - [PHILOSOPHY.md](PHILOSOPHY.md) - Design principles
   - [docs/](docs/) - Additional documentation

2. **Verify your document**:
   ```bash
   python3 medf.py verify document.medf.json --explain
   ```

3. **Check examples**:
   - [examples/](examples/) - Sample MEDF documents
   - [examples/viewer/](examples/viewer/) - Viewer implementation

4. **Report issues**:
   - GitHub: https://github.com/maskin/medf/issues
   - Include error message, command used, and MEDF file (if possible)

---

## Common Mistakes

### ❌ Editing `.medf.json` directly
**✅ Do**: Edit source Markdown, then re-import
```bash
python3 medf.py import document.md
```

### ❌ Forgetting to pack after changes
**✅ Do**: Always pack after modifying
```bash
python3 medf.py pack document.medf.json
```

### ❌ Expecting "correctness" validation
**✅ Remember**: MEDF verifies integrity, not correctness
- Hash matches = Content unchanged ✓
- Does NOT mean = Content is correct ✗

### ❌ Trusting signatures blindly
**✅ Remember**: Signatures show "who signed", not "trustworthy"
- Verify signer's identity separately
- Signature ≠ Authority

---

## Prevention Best Practices

1. **Always work from source Markdown**
   - Keep `.md` files as source of truth
   - Re-import when making changes

2. **Verify after packing**
   ```bash
   python3 medf.py pack document.medf.json
   python3 medf.py verify document.medf.json
   ```

3. **Use version control**
   ```bash
   git add document.medf.json
   git commit -m "Update document"
   ```

4. **Keep backups of signing keys**
   - Store `private.key` securely
   - Never commit keys to Git

5. **Document your workflow**
   - Note MEDF version used
   - Record snapshot timestamps
   - Track document versions

---

For more information, see:
- [Design Principles](README.md#design-principles)
- [Specification](spec/medf.schema.json)
- [Philosophy](PHILOSOPHY.md)
