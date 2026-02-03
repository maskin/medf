#!/usr/bin/env python3
"""
MeDF Validator - Validates MeDF documents against the JSON Schema

Usage:
    python3 validate.py <path-to-medf-file>
    python3 validate.py examples/*.medf.json
"""

import sys
import json
import jsonschema
from pathlib import Path


def load_schema():
    """Load the MeDF JSON Schema"""
    schema_path = Path(__file__).parent / 'schema.json'
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_medf_document(file_path, schema):
    """
    Validate a MeDF document against the schema
    
    Args:
        file_path: Path to the MeDF document
        schema: JSON Schema to validate against
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            document = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except FileNotFoundError:
        return False, f"File not found: {file_path}"
    
    try:
        jsonschema.validate(instance=document, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        path = '.'.join(str(p) for p in e.path) if e.path else 'root'
        return False, f"{e.message}\n  Location: {path}"
    except jsonschema.exceptions.SchemaError as e:
        return False, f"Schema error: {e.message}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <path-to-medf-file> [<path-to-medf-file> ...]")
        print("\nExample:")
        print("  python3 validate.py examples/project-status.v1.0.medf.json")
        print("  python3 validate.py examples/*.medf.json")
        sys.exit(1)
    
    # Load schema
    try:
        schema = load_schema()
    except Exception as e:
        print(f"Error loading schema: {e}")
        sys.exit(1)
    
    # Validate each file
    files = sys.argv[1:]
    total = len(files)
    valid = 0
    
    for file_path in files:
        is_valid, error = validate_medf_document(file_path, schema)
        
        if is_valid:
            print(f"✓ {file_path}")
            valid += 1
        else:
            print(f"✗ {file_path}")
            print(f"  {error}")
    
    # Summary
    print(f"\n{valid}/{total} documents validated successfully")
    
    if valid < total:
        sys.exit(1)


if __name__ == '__main__':
    main()
