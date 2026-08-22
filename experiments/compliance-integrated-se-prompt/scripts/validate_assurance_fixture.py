#!/usr/bin/env python3
"""Validate the synthetic assurance fixture, artifact integrity, and stale transition."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = SCRIPT_DIR.parent
DEFAULT_FIXTURE = EXPERIMENT_DIR / "examples" / "assurance_inconclusive_fixture.json"
DEFAULT_FIXTURE_SCHEMA = EXPERIMENT_DIR / "schemas" / "assurance_fixture.schema.json"
DEFAULT_EXTENSION_SCHEMA = EXPERIMENT_DIR / "schemas" / "compliance_se_model.schema.json"
DEFAULT_BASE_SCHEMA = EXPERIMENT_DIR.parent / "hierarchical-se-prompt" / "schemas" / "se_model.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", nargs="?", type=Path, default=DEFAULT_FIXTURE)
    args = parser.parse_args()

    fixture_path = args.fixture.resolve()
    fixture = load_json(fixture_path)
    fixture_schema = load_json(DEFAULT_FIXTURE_SCHEMA)
    extension_schema = load_json(DEFAULT_EXTENSION_SCHEMA)
    base_schema = load_json(DEFAULT_BASE_SCHEMA)

    registry = Registry().with_resources(
        [
            (base_schema["$id"], Resource.from_contents(base_schema)),
            (extension_schema["$id"], Resource.from_contents(extension_schema)),
            (fixture_schema["$id"], Resource.from_contents(fixture_schema)),
        ]
    )
    errors = [
        f"schema:{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in Draft202012Validator(fixture_schema, registry=registry).iter_errors(fixture)
    ]

    before = fixture["before_change"]
    after = fixture["after_change"]
    event = fixture["change_event"]
    evidence_requirement = fixture["evidence_requirement"]
    activity = fixture["assessment_activity"]
    before_item = before["evidence_item"]
    after_item = after["evidence_item"]

    artifact_path = fixture_path.parent / before_item["artifact_locator"]
    if not artifact_path.is_file():
        errors.append(f"artifact:missing:{artifact_path}")
    else:
        actual_hash = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        expected_hash = before_item["integrity_hash"].removeprefix("sha256:")
        if actual_hash != expected_hash:
            errors.append(f"artifact:sha256 mismatch expected={expected_hash} actual={actual_hash}")

    evidence_id = before_item["id"]
    requirement_id = evidence_requirement["id"]
    activity_id = activity["id"]
    if before_item["evidence_requirement_refs"] != [requirement_id]:
        errors.append("semantic:before evidence requirement reference mismatch")
    if activity["planned_evidence_requirement_refs"] != [requirement_id]:
        errors.append("semantic:assessment activity evidence requirement reference mismatch")
    if before_item["produced_by_activity_ref"] != activity_id:
        errors.append("semantic:evidence producer activity reference mismatch")
    if before["assessment_result"]["evidence_item_refs"] != [evidence_id]:
        errors.append("semantic:before assessment evidence reference mismatch")
    if after["assessment_result"]["evidence_item_refs"] != [evidence_id]:
        errors.append("semantic:after assessment evidence reference mismatch")
    if before_item["validity_state"] != "active" or after_item["validity_state"] != "stale":
        errors.append("semantic:required active-to-stale transition missing")
    if event["previous_configuration_ref"] != before_item["configuration_ref"]:
        errors.append("semantic:change event previous configuration mismatch")
    if event["new_configuration_ref"] == before_item["configuration_ref"]:
        errors.append("semantic:change event does not change configuration")
    if evidence_id not in event["affected_evidence_item_refs"]:
        errors.append("semantic:change event does not identify evidence item")
    if before["assessment_result"]["outcome"] != "inconclusive":
        errors.append("semantic:before outcome must remain inconclusive")
    if after["assessment_result"]["outcome"] != "inconclusive":
        errors.append("semantic:after outcome must remain inconclusive")

    if errors:
        print("FAIL", fixture_path)
        for error in sorted(errors):
            print("-", error)
        return 1

    print(
        "PASS",
        fixture_path,
        f"artifact_sha256={before_item['integrity_hash']}",
        "outcome=inconclusive",
        "transition=active_to_stale",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
