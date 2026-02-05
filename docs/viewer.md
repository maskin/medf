# MEDF Viewer Specification

**Status:** Draft
**Created:** 2026-02-05
**Authors:** MEDF Project

---

## Abstract

This document specifies the MEDF viewer concept — a flexible, block-based document presentation system that enables responsive viewing, precise citation, and embedding of individual sections.

Unlike PDF's fixed layout, MEDF viewers separate content from presentation, allowing documents to adapt to different contexts while maintaining verifiable integrity.

---

## Design Philosophy

### Core Principles

1. **Content-Presentation Separation**
   - Text content is immutable and verifiable
   - Layout, styling, and rendering are mutable

2. **Block-Based Architecture**
   - Each block is independently addressable
   - Blocks can be displayed individually or in combination

3. **Responsive by Default**
   - Layout adapts to viewport and device
   - No fixed page boundaries

4. **Citation-First Design**
   - Every block has a stable identifier
   - Direct links to specific blocks

---

## Viewer Features

### 1. Block-Level Addressing

**URL Scheme:**
```
https://viewer.example.com/doc/{document_id}#{block_id}
```

**Examples:**
- `https://viewer.example.com/doc/paper-2026-example#abstract`
- `https://viewer.example.com/doc/admin-guideline-2024#scope`

**Fragment Navigation:**
- Opening URL automatically scrolls to block
- Block is visually highlighted
- Browser history navigation supported

### 2. Responsive Layout

**Breakpoints:**
```css
/* Mobile */
@media (max-width: 640px) {
  .medf-block { font-size: 16px; padding: 1rem; }
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
  .medf-block { font-size: 18px; padding: 1.5rem; }
}

/* Desktop */
@media (min-width: 1025px) {
  .medf-block { font-size: 20px; padding: 2rem; max-width: 800px; }
}
```

**Layout Options:**
- Single column (default)
- Two column (desktop)
- Full width (reader mode)

### 3. Display Modes

**Document Mode:**
- Display all blocks in sequence
- Table of contents navigation
- Block-based anchor links

**Block Mode:**
- Display single block
- Context: Show previous/next links
- Embeddable in other pages

**Comparison Mode:**
- Display two documents side-by-side
- Highlight block differences
- Show common blocks once

### 4. Styling Options

**Themes:**
- Light (default)
- Dark
- High contrast
- Print-optimized

**Typography:**
- Font family selection
- Font size adjustment
- Line height control
- Text alignment

**Block-Level Styles:**
```css
.medf-block[data-role="abstract"] {
  background: #f5f5f5;
  border-left: 4px solid #007bff;
}

.medf-block[data-role="policy"] {
  border: 2px solid #dc3545;
  padding: 1.5rem;
}

.medf-block[data-format="markdown"] {
  /* Markdown rendering */
}
```

### 5. Embedding

**HTML Element:**
```html
<medf-block
  document="paper-2026-example"
  block="methodology"
  theme="light"
  show-link="true">
</medf-block>
```

**Web Component:**
```javascript
<medf-block
  document-id="paper-2026-example"
  block-id="methodology"
  src="https://example.com/paper-2026-example.medf.json">
</medf-block>
```

**Iframe:**
```html
<iframe
  src="https://viewer.example.com/embed/paper-2026-example#methodology"
  width="100%"
  height="400">
</iframe>
```

### 6. Citation Tools

**Copy Citation Button:**
- Click block → Copy citation to clipboard
- Format: `MEDF: paper-2026-example#methodology`
- Optional: Include full URL

**Export Block:**
- Download single block as JSON
- Export as Markdown
- Copy as HTML (styled)

**Permalink:**
- Each block has stable permalink
- Includes document version (snapshot)
- Example: `https://viewer.example.com/paper-2026-example/2026-02-05#methodology`

---

## Technical Implementation

### 1. HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MEDF Viewer - {document_id}</title>
  <link rel="stylesheet" href="medf-viewer.css">
</head>
<body>
  <div class="medf-viewer">
    <header class="medf-header">
      <h1>{document_title}</h1>
      <div class="medf-meta">
        <span class="medf-id">MEDF: {document_id}</span>
        <span class="medf-snapshot">{snapshot}</span>
      </div>
    </header>

    <nav class="medf-toc">
      <!-- Table of contents generated from blocks -->
    </nav>

    <main class="medf-content">
      <article class="medf-block" id="{block_id}" data-role="{role}">
        <div class="medf-block-text">
          {block_content}
        </div>
        <div class="medf-block-actions">
          <button class="medf-copy-citation">Copy Citation</button>
          <button class="medf-permalink">Permalink</button>
        </div>
      </article>
    </main>

    <footer class="medf-footer">
      <div class="medf-verification">
        ✔ Integrity verified: {doc_hash}
      </div>
    </footer>
  </div>

  <script src="medf-viewer.js"></script>
</body>
</html>
```

### 2. JavaScript API

**Load Document:**
```javascript
const viewer = new MEDFViewer();

// Load from URL
viewer.load('paper-2026-example.medf.json');

// Load from object
viewer.loadDocument({
  medf_version: "0.2.1",
  id: "paper-2026-example",
  blocks: [...]
});

// Verify before display
viewer.loadAndVerify('paper-2026-example.medf.json')
  .then(doc => {
    if (doc.verified) {
      viewer.render(doc);
    }
  });
```

**Navigate to Block:**
```javascript
// Scroll to block
viewer.navigateToBlock('methodology');

// Get block content
const block = viewer.getBlock('methodology');

// Render single block
viewer.renderBlock('methodology', targetElement);
```

**Event Handling:**
```javascript
viewer.on('blockClick', (blockId) => {
  console.log('Clicked:', blockId);
});

viewer.on('citationCopy', (citation) => {
  alert('Copied: ' + citation);
});
```

### 3. CSS Architecture

**CSS Variables:**
```css
:root {
  --medf-font-size-base: 18px;
  --medf-line-height: 1.6;
  --medf-max-width: 800px;
  --medf-color-bg: #ffffff;
  --medf-color-text: #333333;
  --medf-color-accent: #007bff;
  --medf-spacing-block: 2rem;
}
```

**Component Classes:**
- `.medf-viewer` - Root container
- `.medf-header` - Document header
- `.medf-toc` - Table of contents
- `.medf-block` - Individual block
- `.medf-block-text` - Block content
- `.medf-block-actions` - Action buttons
- `.medf-footer` - Document footer

---

## Web Component Specification

### Custom Element: `<medf-viewer>`

```html
<medf-viewer
  src="document.medf.json"
  theme="dark"
  show-toc="true"
  show-verification="true">
</medf-viewer>
```

**Attributes:**
- `src` - Path to MEDF JSON file
- `theme` - Theme name (light, dark, high-contrast)
- `show-toc` - Show table of contents (default: true)
- `show-verification` - Show verification status (default: true)
- `initial-block` - Initial block to display

**Methods:**
```javascript
const viewer = document.querySelector('medf-viewer');
viewer.loadDocument('other-document.medf.json');
viewer.navigateToBlock('methodology');
viewer.setTheme('dark');
```

### Custom Element: `<medf-block>`

```html
<medf-block
  src="document.medf.json"
  block-id="methodology"
  theme="light"
  show-link="true">
</medf-block>
```

**Attributes:**
- `src` - Path to MEDF JSON file
- `block-id` - Block identifier to display
- `theme` - Theme name
- `show-link` - Show link to full document (default: true)

---

## Use Cases

### 1. Academic Papers

**Scenario:** Researcher cites specific methodology section

```html
<p>As demonstrated in the methodology:</p>
<medf-block src="paper-2026-example.medf.json" block-id="methodology"></medf-block>
```

**Benefits:**
- Precise section citation
- Always links to latest version
- Embeddable in any website
- Verifiable content

### 2. Technical Documentation

**Scenario:** API documentation with individual examples

```javascript
// Each section is independently addressable
viewer.navigateToBlock('authentication-example');
```

**Benefits:**
- Link to specific code examples
- Responsive on mobile devices
- Print-optimized styles
- Searchable by block ID

### 3. Legal Documents

**Scenario:** Regulations with section-by-section compliance

```html
<medf-viewer src="gdpr-regulation.medf.json">
</medf-viewer>
```

**Benefits:**
- Navigate to specific articles
- Compare versions side-by-side
- Official verification status
- Print individual sections

### 4. Blog Embeds

**Scenario:** Blogger quotes policy document section

```html
<blockquote>
  <medf-block
    src="privacy-policy.medf.json"
    block-id="data-collection"
    show-link="true">
  </medf-block>
</blockquote>
```

**Benefits:**
- Always shows current version
- Links to full document
- Styled for blog theme
- Verifiable source

---

## Comparison: PDF vs MEDF Viewer

| Feature | PDF | MEDF Viewer |
|---------|-----|-------------|
| Layout | Fixed page | Responsive |
| Citation | Page number | Block ID |
| Linking | Page + anchor | Document + Block |
| Embedding | iframe/page image | Web component |
| Mobile | Pinch-to-zoom | Native responsive |
| Accessibility | Varies | Semantic HTML |
| Verification | Signature | Hash verification |
| Updates | New file | New version |
| Block引用 | No | Yes |
| Custom styling | No | Yes |

---

## Security Considerations

### Content Verification

**Viewer should:**
1. Verify document hash before rendering
2. Display verification status prominently
3. Warn if content modified since packing
4. Support signature verification

**User control:**
- Option to disable rendering of unverified documents
- Clear indication of verification status
- Block-level hash display

### XSS Prevention

**Markdown rendering:**
- Sanitize HTML in markdown blocks
- Use DOMPurify or equivalent
- Whitelist approach for HTML tags

**External references:**
- No automatic loading of external resources
- Explicit user approval for remote fetch
- CSP headers for embedded viewers

---

## Performance Considerations

### Lazy Loading

**Strategy:**
- Load visible blocks first
- Lazy load blocks below fold
- Prefetch on hover for TOC links

**Implementation:**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      viewer.loadBlock(entry.target.dataset.blockId);
    }
  });
});
```

### Caching

**Browser cache:**
- Cache MEDF JSON files
- Use ETag for version checking
- Service Worker for offline viewing

**Application cache:**
- IndexedDB for large documents
- SessionStorage for current document
- LocalStorage for preferences

---

## Future Enhancements

### 1. Interactive Features

- Block-level comments/annotations
- Collaborative highlighting
- Version comparison slider
- Block-level translations

### 2. Advanced Navigation

- Graph visualization of references
- Dependency graph between documents
- Backlink tracking (what links to this block?)
- Table of contents with progress

### 3. Export Options

- Export selection as new MEDF document
- Generate PDF from MEDF (fixed layout)
- Export as EPUB
- Export slides from blocks

### 4. Integration

- CMS plugins (WordPress, Hugo)
- Markdown editor integration
- Browser extension for MEDF links
- VS Code extension for preview

---

## Examples

See `examples/viewer/` for:
- `index.html` - Basic viewer implementation
- `embed.html` - Embed example
- `web-component.html` - Custom element usage
- `medf-viewer.css` - Reference styling
- `medf-viewer.js` - Reference implementation

---

## Changelog

### v0.1 (Draft)
- Initial viewer specification
- Block-based navigation
- Responsive design principles
- Web component API
