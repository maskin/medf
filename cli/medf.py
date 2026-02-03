#!/usr/bin/env python3
"""
MeDF CLI Tool - Meaning-anchored Document Format Command Line Interface

Usage:
    python medf.py convert <input.md> <output.medf> [options]
    python medf.py validate <file.medf>
    python medf.py to-html <input.medf> <output.html>
    python medf.py hash <file.medf>
    python medf.py verify <file.medf>
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import markdown
    from jsonschema import validate, ValidationError
except ImportError:
    print("Required packages: markdown, jsonschema")
    print("Install with: pip install markdown jsonschema")
    sys.exit(1)


class MeDFConverter:
    """Convert Markdown to MeDF format."""

    def __init__(self):
        self.sections = []

    def extract_sections(self, content: str) -> List[Dict[str, Any]]:
        """Extract section structure from Markdown content."""
        sections = []
        lines = content.split('\n')

        for line in lines:
            # Match Markdown headers: # Title {:id=xxx}
            match = re.match(r'^(#{1,6})\s+(.+?)(?:\s+\{:id=([a-z0-9-]+)\})?$', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                section_id = match.group(3) or self._slugify(title)

                sections.append({
                    'id': section_id,
                    'title': title,
                    'level': level,
                    'summary': ''
                })

        return sections

    def _slugify(self, text: str) -> str:
        """Convert text to slug format."""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        return text

    def extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from Markdown frontmatter or content."""
        metadata = {}

        # Extract title from first h1
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            metadata['title'] = match.group(1).strip()

        # Extract summary if present
        summary_match = re.search(r'<!--\s*summary:\s*(.+?)\s*-->', content, re.DOTALL)
        if summary_match:
            metadata['summary'] = summary_match.group(1).strip()

        return metadata

    def convert(
        self,
        input_path: Path,
        output_path: Path,
        doc_id: str,
        authority: str,
        snapshot: Optional[str] = None,
        document_type: str = "public_notice",
        references: Optional[List[Dict[str, str]]] = None,
        extensions: Optional[Dict[str, Any]] = None,
        version: str = "0.2",
        issuer: Optional[str] = None,
        issued_at: Optional[str] = None,
        language: str = "ja"
    ) -> None:
        """Convert Markdown file to MeDF format."""
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate snapshot timestamp if not provided
        if not snapshot:
            snapshot = datetime.now(timezone.utc).isoformat()

        # Use snapshot as issued_at if not provided
        if not issued_at:
            issued_at = snapshot

        # Extract metadata
        metadata = self.extract_metadata(content)
        sections = self.extract_sections(content)

        # Build authority object
        authority_obj = {'name': authority} if isinstance(authority, str) else authority

        # Build MeDF structure
        medf = {
            'medf_version': version,
            'document_type': document_type,
            'id': doc_id,
            'snapshot': snapshot,
            'authority': authority_obj,
            'content': content,
            'index': {
                'title': metadata.get('title', ''),
                'summary': metadata.get('summary', {}),
                'sections': sections
            }
        }

        # Add v0.2 specific fields
        if version == "0.2":
            medf['issued_at'] = issued_at
            medf['language'] = language
            if issuer:
                medf['issuer'] = issuer

        # Add optional fields
        if references:
            medf['references'] = references

        if extensions:
            medf['extensions'] = extensions

        # Calculate hash
        hash_value = self._calculate_hash(medf)
        medf['hash'] = {
            'algorithm': 'sha-256',
            'value': hash_value
        }

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(medf, f, ensure_ascii=False, indent=2)

        print(f"✓ Created MeDF file: {output_path}")
        print(f"  Version: {version}")
        print(f"  Type: {document_type}")
        print(f"  ID: {doc_id}")
        print(f"  Authority: {authority_obj.get('name', authority)}")
        if issuer:
            print(f"  Issuer: {issuer}")
        print(f"  Language: {language}")
        print(f"  Hash: {hash_value[:16]}...")

    def _calculate_hash(self, medf: Dict[str, Any]) -> str:
        """Calculate SHA-256 hash of MeDF content."""
        # Fields to include in hash calculation
        hash_fields = {
            'id': medf['id'],
            'snapshot': medf['snapshot'],
            'authority': medf['authority'],
            'content': medf['content']
        }

        # Add index if present
        if 'index' in medf:
            hash_fields['index'] = json.dumps(medf['index'], ensure_ascii=False)

        # Add references if present
        if 'references' in medf:
            hash_fields['references'] = json.dumps(medf['references'], ensure_ascii=False)

        # Create canonical string representation
        canonical = json.dumps(hash_fields, ensure_ascii=False, sort_keys=True)

        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


class MeDFValidator:
    """Validate MeDF files."""

    def __init__(self, schema_path: Optional[Path] = None, version: str = "0.2"):
        if schema_path:
            self.schema_path = schema_path
        else:
            schema_file = f'medf-v{version}-public.schema.json' if version == "0.2" else 'medf-v0.1.schema.json'
            self.schema_path = Path(__file__).parent.parent / 'schema' / schema_file
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema for validation."""
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate(self, file_path: Path) -> bool:
        """Validate MeDF file against schema."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            validate(instance=data, schema=self.schema)

            # Verify hash
            if 'hash' in data:
                calculator = MeDFConverter()
                # Reconstruct minimal structure for hash calculation
                hash_input = {
                    'id': data['id'],
                    'snapshot': data['snapshot'],
                    'authority': data['authority'],
                    'content': data['content']
                }
                if 'index' in data:
                    hash_input['index'] = json.dumps(data['index'], ensure_ascii=False)
                if 'references' in data:
                    hash_input['references'] = json.dumps(data['references'], ensure_ascii=False)

                canonical = json.dumps(hash_input, ensure_ascii=False, sort_keys=True)
                calculated_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()

                if calculated_hash != data['hash']['value']:
                    print(f"✗ Hash mismatch!")
                    print(f"  Expected: {data['hash']['value']}")
                    print(f"  Calculated: {calculated_hash}")
                    return False

            print(f"✓ {file_path} is valid")
            return True

        except ValidationError as e:
            print(f"✗ Validation error: {e.message}")
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False


class MeDFHTMLConverter:
    """Convert MeDF to HTML."""

    def convert(self, input_path: Path, output_path: Path) -> None:
        """Convert MeDF file to HTML."""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert Markdown content to HTML
        html_content = markdown.markdown(
            data['content'],
            extensions=['extra', 'codehilite', 'toc']
        )

        # Build HTML document
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['index'].get('title', data['id'])}</title>
    <style>
        body {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
        }}
        .medf-metadata {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
        .medf-metadata dt {{
            font-weight: bold;
            margin-top: 10px;
        }}
        .medf-metadata dd {{
            margin-left: 0;
            word-break: break-all;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
        }}
        code {{
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        pre {{
            background: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 15px;
            margin-left: 0;
            color: #666;
        }}
    </style>
</head>
<body>
    <dl class="medf-metadata">
        <dt>MeDF ID</dt>
        <dd>{data['id']}</dd>
        <dt>Snapshot</dt>
        <dd>{data['snapshot']}</dd>
        <dt>Authority</dt>
        <dd>{data['authority']}</dd>
        <dt>Hash</dt>
        <dd>{data['hash']['value']}</dd>
    </dl>

    <main>
        {html_content}
    </main>
</body>
</html>"""

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Created HTML file: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='MeDF CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # convert command
    convert_parser = subparsers.add_parser('convert', help='Convert Markdown to MeDF')
    convert_parser.add_argument('input', type=Path, help='Input Markdown file')
    convert_parser.add_argument('output', type=Path, help='Output MeDF file')
    convert_parser.add_argument('--id', required=True, help='Document ID (e.g., JP-MLIT-2026-GUIDE-001@2026-02-04T10:00:00Z)')
    convert_parser.add_argument('--authority', required=True, help='Authority name (or JSON object with name, code, department)')
    convert_parser.add_argument('--snapshot', help='Snapshot timestamp (ISO 8601)')
    convert_parser.add_argument('--issued-at', help='Issuance timestamp (ISO 8601)')
    convert_parser.add_argument('--type', default='public_notice', choices=['public_notice', 'guideline', 'press_release', 'report', 'white_paper', 'official_statement'], help='Document type')
    convert_parser.add_argument('--version', default='0.2', choices=['0.1', '0.2'], help='MeDF version')
    convert_parser.add_argument('--issuer', help='Issuer organization code (e.g., JP-MLIT)')
    convert_parser.add_argument('--language', default='ja', help='Language code (e.g., ja, en)')
    convert_parser.add_argument('--reference', action='append', help='Reference URI (can be used multiple times)')

    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate MeDF file')
    validate_parser.add_argument('file', type=Path, help='MeDF file to validate')
    validate_parser.add_argument('--version', default='0.2', choices=['0.1', '0.2'], help='MeDF version for schema validation')

    # to-html command
    html_parser = subparsers.add_parser('to-html', help='Convert MeDF to HTML')
    html_parser.add_argument('input', type=Path, help='Input MeDF file')
    html_parser.add_argument('output', type=Path, help='Output HTML file')

    # hash command
    hash_parser = subparsers.add_parser('hash', help='Calculate hash of MeDF file')
    hash_parser.add_argument('file', type=Path, help='MeDF file')

    # verify command
    verify_parser = subparsers.add_parser('verify', help='Verify hash of MeDF file')
    verify_parser.add_argument('file', type=Path, help='MeDF file')
    verify_parser.add_argument('--version', default='0.2', choices=['0.1', '0.2'], help='MeDF version for schema validation')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'convert':
        references = None
        if args.reference:
            references = [{'uri': uri, 'type': 'source'} for uri in args.reference]

        converter = MeDFConverter()
        converter.convert(
            args.input,
            args.output,
            doc_id=args.id,
            authority=args.authority,
            snapshot=args.snapshot,
            document_type=args.type,
            references=references,
            version=args.version,
            issuer=getattr(args, 'issuer', None),
            issued_at=getattr(args, 'issued_at', None),
            language=getattr(args, 'language', 'ja')
        )

    elif args.command == 'validate':
        validator = MeDFValidator(version=args.version)
        return 0 if validator.validate(args.file) else 1

    elif args.command == 'to-html':
        converter = MeDFHTMLConverter()
        converter.convert(args.input, args.output)

    elif args.command == 'hash':
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        converter = MeDFConverter()
        hash_input = {
            'id': data['id'],
            'snapshot': data['snapshot'],
            'authority': data['authority'],
            'content': data['content']
        }
        if 'index' in data:
            hash_input['index'] = json.dumps(data['index'], ensure_ascii=False)
        if 'references' in data:
            hash_input['references'] = json.dumps(data['references'], ensure_ascii=False)

        canonical = json.dumps(hash_input, ensure_ascii=False, sort_keys=True)
        calculated_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()

        print(f"Hash: {calculated_hash}")

    elif args.command == 'verify':
        validator = MeDFValidator(version=args.version)
        return 0 if validator.validate(args.file) else 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
