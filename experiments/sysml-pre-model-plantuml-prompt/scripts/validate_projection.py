"""Validate an experiment 5 PlantUML projection without a PlantUML renderer."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


METADATA_KEYS = (
    "diagram_id",
    "diagram_type",
    "title",
    "purpose",
    "question",
    "source_of_truth",
    "semantic_mode",
    "abstraction_level",
    "source_ids",
    "omitted_ids",
    "limitation",
)
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*-[A-Z0-9][A-Z0-9._-]*$")
ID_TOKEN_PATTERN = r"[A-Z][A-Z0-9_]*-[A-Z0-9][A-Z0-9._-]*"


def load_json(path: Path) -> Any:
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


def metadata_value(text: str, key: str) -> str | None:
    match = re.search(rf"^' {re.escape(key)}:\s*(.*?)\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("projection_dir", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        model = load_json(args.model)
        schema = load_json(args.schema)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL\n- input loading error: {exc}")
        return 1

    for error in Draft202012Validator(schema).iter_errors(model):
        location = "$" + "".join(
            f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.path
        )
        errors.append(f"schema error at {location}: {error.message}")

    ids: dict[str, str] = {}
    duplicates: list[str] = []
    collect_ids(model, ids, duplicates)
    errors.extend(f"duplicate ID: {item}" for item in duplicates)

    if not args.projection_dir.is_dir():
        errors.append(f"projection directory does not exist: {args.projection_dir}")
    else:
        puml_files = sorted(args.projection_dir.glob("*.puml"))
        if not (args.projection_dir / "99_generation_index.puml").is_file():
            errors.append("99_generation_index.puml is missing")
        if not puml_files:
            errors.append("no PlantUML files found")

        for path in puml_files:
            text = path.read_text(encoding="utf-8")
            if path.name != "00_style.puml":
                if not text.startswith("@startuml"):
                    errors.append(f"{path.name}: missing @startuml at file start")
                if not text.rstrip().endswith("@enduml"):
                    errors.append(f"{path.name}: missing @enduml at file end")
                for key in METADATA_KEYS:
                    if metadata_value(text, key) is None:
                        errors.append(f"{path.name}: missing metadata {key}")
                source_ids = metadata_value(text, "source_ids") or ""
                for source_id in re.findall(ID_TOKEN_PATTERN, source_ids):
                    if source_id not in ids:
                        errors.append(f"{path.name}: unresolved metadata source ID {source_id}")
                if re.search(r"https?://|!includeurl|sprite\(", text, re.IGNORECASE):
                    errors.append(f"{path.name}: external/network PlantUML resource found")
            elif "@startuml" in text or "@enduml" in text:
                errors.append("00_style.puml: style snippet must not contain diagram boundary tokens")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(f"- schema: {args.schema}")
    print(f"- unique IDs: {len(ids)}")
    print(f"- PlantUML files: {len(list(args.projection_dir.glob('*.puml')))}")
    print("- syntax_validation: not_performed (no PlantUML renderer was invoked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
