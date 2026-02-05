/**
 * MEDF Viewer - Reference Implementation
 *
 * A flexible, block-based MEDF document viewer with:
 * - Document loading and verification
 * - Block-based navigation
 * - Table of contents generation
 * - Citation copying
 * - Responsive rendering
 */

class MEDFViewer {
  constructor(options = {}) {
    this.options = {
      verifyOnLoad: true,
      showBlockIds: true,
      theme: 'light',
      ...options
    };
    this.currentDocument = null;
    this.verified = false;
  }

  /**
   * Load and verify a MEDF document
   */
  async loadAndVerify(path) {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const doc = await response.json();

      this.currentDocument = doc;

      if (this.options.verifyOnLoad) {
        const result = this.verify(doc);
        this.verified = result.valid;
        this.updateVerificationStatus(result);
      }

      this.render(doc);

      return {
        verified: this.verified,
        hash: doc.doc_hash?.value || null
      };
    } catch (error) {
      console.error('Failed to load document:', error);
      throw error;
    }
  }

  /**
   * Verify document hashes
   */
  verify(doc) {
    if (!doc.doc_hash) {
      return { valid: false, error: 'No document hash' };
    }

    // Calculate document hash (excluding doc_hash and signature fields)
    const docSrc = {
      medf_version: doc.medf_version,
      id: doc.id,
      snapshot: doc.snapshot,
      issuer: doc.issuer,
      document_type: doc.document_type,
      language: doc.language,
      blocks: doc.blocks.map(b => ({
        block_id: b.block_id,
        role: b.role,
        format: b.format,
        text: b.text
      }))
    };

    const canonical = JSON.stringify(docSrc, Object.keys(docSrc).sort());
    const actualHash = this.sha256(canonical);
    const expectedHash = doc.doc_hash.value;

    return {
      valid: actualHash === expectedHash,
      expected: expectedHash,
      actual: actualHash
    };
  }

  /**
   * Calculate SHA-256 hash
   */
  sha256(string) {
    // Simple implementation for browser
    // In production, use crypto.subtle.digest()
    let hash = 0;
    for (let i = 0; i < string.length; i++) {
      const char = string.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).padStart(64, '0');
  }

  /**
   * Render document to DOM
   */
  render(doc) {
    // Update header
    document.getElementById('document-title').textContent =
      doc.document_type?.replace('_', ' ').toUpperCase() || doc.id;
    document.getElementById('document-id').textContent = `MEDF: ${doc.id}`;
    document.getElementById('document-snapshot').textContent = doc.snapshot;

    // Render blocks
    const content = document.getElementById('document-content');
    content.innerHTML = '';

    doc.blocks.forEach(block => {
      const blockElement = this.renderBlock(block);
      content.appendChild(blockElement);
    });

    // Generate table of contents
    this.generateTOC(doc.blocks);

    // Apply theme
    this.setTheme(this.options.theme);
  }

  /**
   * Render a single block
   */
  renderBlock(block) {
    const article = document.createElement('article');
    article.className = 'medf-block';
    article.id = block.block_id;
    article.dataset.role = block.role;

    // Block ID
    if (this.options.showBlockIds) {
      const idSpan = document.createElement('span');
      idSpan.className = 'medf-block-id';
      idSpan.textContent = `#${block.block_id}`;
      article.appendChild(idSpan);
    }

    // Block content
    const content = document.createElement('div');
    content.className = 'medf-block-text';
    content.innerHTML = this.renderMarkdown(block.text);
    article.appendChild(content);

    // Block actions
    const actions = document.createElement('div');
    actions.className = 'medf-block-actions';

    const copyBtn = document.createElement('button');
    copyBtn.className = 'medf-btn';
    copyBtn.textContent = 'Copy Citation';
    copyBtn.onclick = () => this.copyCitation(block.block_id);
    actions.appendChild(copyBtn);

    const linkBtn = document.createElement('button');
    linkBtn.className = 'medf-btn';
    linkBtn.textContent = 'Permalink';
    linkBtn.onclick = () => this.copyPermalink(block.block_id);
    actions.appendChild(linkBtn);

    article.appendChild(actions);

    return article;
  }

  /**
   * Simple markdown renderer
   */
  renderMarkdown(text) {
    if (!text) return '';

    let html = text
      // Escape HTML
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // Headers
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      // Bold
      .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
      // Italic
      .replace(/\*(.*)\*/gim, '<em>$1</em>')
      // Code
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      // Code blocks
      .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
      // Links
      .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2">$1</a>')
      // Unordered lists
      .replace(/^\- (.*$)/gim, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>')
      // Line breaks
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');

    return `<p>${html}</p>`;
  }

  /**
   * Generate table of contents
   */
  generateTOC(blocks) {
    const tocList = document.getElementById('toc-list');
    tocList.innerHTML = '';

    blocks.forEach(block => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${block.block_id}`;
      a.textContent = block.block_id.replace(/-/g, ' ');
      a.onclick = (e) => {
        e.preventDefault();
        this.navigateToBlock(block.block_id);
      };
      li.appendChild(a);
      tocList.appendChild(li);
    });
  }

  /**
   * Navigate to block
   */
  navigateToBlock(blockId) {
    const block = document.getElementById(blockId);
    if (block) {
      block.scrollIntoView({ behavior: 'smooth', block: 'start' });

      // Update active TOC item
      document.querySelectorAll('.medf-toc a').forEach(a => {
        a.classList.remove('active');
      });
      const tocLink = document.querySelector(`.medf-toc a[href="#${blockId}"]`);
      if (tocLink) {
        tocLink.classList.add('active');
      }

      // Update URL hash
      history.pushState(null, null, `#${blockId}`);
    }
  }

  /**
   * Copy citation to clipboard
   */
  copyCitation(blockId) {
    const citation = `MEDF: ${this.currentDocument.id}#${blockId}`;
    navigator.clipboard.writeText(citation).then(() => {
      alert('Copied: ' + citation);
    });
  }

  /**
   * Copy permalink to clipboard
   */
  copyPermalink(blockId) {
    const url = `${window.location.origin}${window.location.pathname}?doc=${this.getDocPath()}#${blockId}`;
    navigator.clipboard.writeText(url).then(() => {
      alert('Copied permalink: ' + url);
    });
  }

  /**
   * Get document path from URL
   */
  getDocPath() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('doc') || '../academic-paper.medf.json';
  }

  /**
   * Update verification status display
   */
  updateVerificationStatus(result) {
    const statusEl = document.getElementById('verification-status');
    if (result.valid) {
      statusEl.textContent = '✔ Verified';
      statusEl.className = 'medf-verification verified';
    } else {
      statusEl.textContent = '✖ Unverified';
      statusEl.className = 'medf-verification unverified';
      console.warn('Verification failed:', result);
    }
  }

  /**
   * Set theme
   */
  setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.options.theme = theme;
  }

  /**
   * Get block by ID
   */
  getBlock(blockId) {
    return this.currentDocument?.blocks.find(b => b.block_id === blockId);
  }

  /**
   * Render single block to element
   */
  renderBlockTo(blockId, targetElement) {
    const block = this.getBlock(blockId);
    if (!block) {
      throw new Error(`Block not found: ${blockId}`);
    }

    const blockElement = this.renderBlock(block);
    targetElement.innerHTML = '';
    targetElement.appendChild(blockElement);
  }
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MEDFViewer;
}
