"""Validate the experiment 3 candidate model without fetching remote schemas."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9._-]*$")
IGNORED_REFERENCE_KEYS = {
    "source_locator",
    "spec_ref",
    "source_of_truth_ref",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def collect_ids(value: Any, found: dict[str, str], duplicates: list[str], path: str = "$") -> None:
    if isinstance(value, dict):
        candidate = value.get("id")
        if isinstance(candidate, str) and ID_PATTERN.match(candidate):
            if candidate in found:
                duplicates.append(f"{candidate}: {found[candidate]} and {path}.id")
            else:
                found[candidate] = f"{path}.id"
        for key, child in value.items():
            collect_ids(child, found, duplicates, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_ids(child, found, duplicates, f"{path}[{index}]")


def looks_like_id(value: str) -> bool:
    return bool(ID_PATTERN.match(value))


def collect_reference_errors(value: Any, ids: set[str], errors: list[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in IGNORED_REFERENCE_KEYS:
                continue
            if key.endswith("_refs") and isinstance(child, list):
                for index, item in enumerate(child):
                    if isinstance(item, str) and looks_like_id(item) and item not in ids:
                        errors.append(f"dangling reference at {child_path}[{index}]: {item}")
            elif key.endswith("_ref") and isinstance(child, str):
                if looks_like_id(child) and child not in ids:
                    errors.append(f"dangling reference at {child_path}: {child}")
            elif key == "required_evidence" and isinstance(child, list):
                for index, item in enumerate(child):
                    if isinstance(item, str) and looks_like_id(item) and item not in ids:
                        errors.append(f"dangling evidence reference at {child_path}[{index}]: {item}")
            collect_reference_errors(child, ids, errors, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_reference_errors(child, ids, errors, f"{path}[{index}]")


def check_document_views(model: dict[str, Any], ids: set[str], errors: list[str]) -> None:
    views = model.get("document_views", [])
    kinds = {view.get("view_kind") for view in views if isinstance(view, dict)}
    for required in ("planning_document", "requirements_document"):
        if required not in kinds:
            errors.append(f"document_views is missing required view_kind: {required}")
    for index, view in enumerate(views):
        if not isinstance(view, dict):
            continue
        for ref in view.get("element_refs", []):
            if ref not in ids:
                errors.append(f"document view element_refs[{index}] does not resolve: {ref}")
        for section in view.get("section_order", []):
            for ref in section.get("element_refs", []):
                if ref not in ids:
                    errors.append(f"document view section reference does not resolve: {ref}")
        if view.get("source_of_truth_ref") != "10_se_model.json":
            errors.append(f"document view {view.get('id')} does not point to 10_se_model.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument(
        "--base-schema",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "hierarchical-se-prompt" / "schemas" / "se_model.schema.json",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "schemas" / "planning_requirements_se_model.schema.json",
    )
    args = parser.parse_args()

    try:
        model = load_json(args.model)
        base_schema = load_json(args.base_schema)
        schema = load_json(args.schema)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: input loading error: {exc}")
        return 1

    errors: list[str] = []
    registry = (
        Registry()
        .with_resource(base_schema["$id"], Resource.from_contents(base_schema))
        .with_resource(schema["$id"], Resource.from_contents(schema))
    )
    validator = Draft202012Validator(schema, registry=registry)
    for error in sorted(validator.iter_errors(model), key=lambda item: list(item.path)):
        location = "$" + "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.path)
        errors.append(f"schema error at {location}: {error.message}")

    ids: dict[str, str] = {}
    duplicates: list[str] = []
    collect_ids(model, ids, duplicates)
    errors.extend(f"duplicate ID: {item}" for item in duplicates)
    reference_errors: list[str] = []
    collect_reference_errors(model, set(ids), reference_errors)
    errors.extend(reference_errors)
    check_document_views(model, set(ids), errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(f"- schema: {args.schema}")
    print(f"- base schema: {args.base_schema}")
    print(f"- unique IDs: {len(ids)}")
    print("- document views: planning_document, requirements_document")
    print("- external API contract details are not linted by this validator")
    return 0


if __name__ == "__main__":
    sys.exit(main())
