"""Validate a document projection against its SELabo semantic source."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9._-]*$")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def collect_ids(value: Any, found: dict[str, str], path: str = "$") -> None:
    if isinstance(value, dict):
        item_id = value.get("id")
        if isinstance(item_id, str) and ID_PATTERN.match(item_id):
            found[item_id] = f"{path}.id"
        for key, child in value.items():
            collect_ids(child, found, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_ids(child, found, f"{path}[{index}]")


def check_id_references(value: Any, ids: set[str], errors: list[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.endswith("_refs") and isinstance(child, list):
                for index, item in enumerate(child):
                    if isinstance(item, str) and ID_PATTERN.match(item) and item not in ids:
                        errors.append(f"dangling reference at {child_path}[{index}]: {item}")
            elif key.endswith("_ref") and isinstance(child, str):
                if ID_PATTERN.match(child) and child not in ids:
                    errors.append(f"dangling reference at {child_path}: {child}")
            check_id_references(child, ids, errors, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_id_references(child, ids, errors, f"{path}[{index}]")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="10_se_model.json or representative model")
    parser.add_argument("document_model", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "schemas" / "se_document_projection.schema.json",
    )
    args = parser.parse_args()

    try:
        source = load_json(args.source)
        document = load_json(args.document_model)
        schema = load_json(args.schema)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: input loading error: {exc}")
        return 1

    errors: list[str] = []
    for error in sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path)):
        location = "$" + "".join(
            f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.path
        )
        errors.append(f"schema error at {location}: {error.message}")

    source_id_map: dict[str, str] = {}
    document_id_map: dict[str, str] = {}
    collect_ids(source, source_id_map)
    collect_ids(document, document_id_map)
    source_ids = set(source_id_map)
    all_ids = source_ids | set(document_id_map)
    check_id_references(document, all_ids, errors)

    expected_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    actual_hash = document.get("source_binding", {}).get("content_hash")
    if actual_hash not in {expected_hash, f"sha256:{expected_hash}"}:
        errors.append("source_binding.content_hash does not match the semantic source")
    if document.get("source_binding", {}).get("source_of_truth") != "10_se_model.json":
        errors.append("source_binding.source_of_truth must be 10_se_model.json")

    doc_requirements = document.get("requirements_definition", {}).get("requirements", [])
    seen_source_requirements: set[str] = set()
    source_requirements = {
        item.get("id"): item
        for item in source.get("requirements", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for index, item in enumerate(doc_requirements):
        if not isinstance(item, dict):
            continue
        source_ref = item.get("source_requirement_ref")
        if source_ref in seen_source_requirements:
            errors.append(f"duplicate source requirement projection: {source_ref}")
        if isinstance(source_ref, str):
            seen_source_requirements.add(source_ref)
        if source_ref not in source_requirements:
            errors.append(f"DOCREQ at index {index} does not resolve: {source_ref}")
            continue
        source_statement = source_requirements[source_ref].get("statement")
        rendered_statement = item.get("rendered_statement", {}).get("value")
        if rendered_statement != source_statement:
            errors.append(f"DOCREQ {item.get('id')} changed the source requirement statement")
        for key in ("source_need_refs", "verification_refs"):
            for ref in item.get(key, []):
                if ref not in all_ids:
                    errors.append(f"DOCREQ {item.get('id')} has dangling {key}: {ref}")

    if set(source_requirements) != seen_source_requirements:
        missing = sorted(set(source_requirements) - seen_source_requirements)
        errors.append(f"document requirement registry is incomplete: {missing}")

    for relation in document.get("traceability", {}).get("relations", []):
        for key in ("relation_id", "source_id", "target_id"):
            if relation.get(key) not in source_ids:
                errors.append(f"traceability {key} does not resolve: {relation.get(key)}")
        if relation.get("source_of_truth") != "10_se_model.json":
            errors.append("traceability relation source_of_truth is not 10_se_model.json")

    for key in ("functional_refs", "nonfunctional_refs", "business_refs", "security_refs", "data_refs", "interface_refs", "operational_refs", "support_refs", "migration_refs", "regulatory_refs", "constraint_refs", "test_requirement_refs", "other_refs", "unclassified_refs"):
        for ref in document.get("requirements_definition", {}).get("views", {}).get(key, []):
            if ref not in document_id_map:
                errors.append(f"requirements view {key} does not resolve: {ref}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    not_performed = document.get("quality", {}).get("not_performed", [])
    print("PASS")
    print(f"- schema: {args.schema}")
    print(f"- source: {args.source}")
    print(f"- projected IDs: {len(document_id_map)}")
    print(f"- DOCREQ registry: {len(doc_requirements)} entries")
    print("- source requirement statements: unchanged")
    print(f"- not performed: {len(not_performed)} items recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
