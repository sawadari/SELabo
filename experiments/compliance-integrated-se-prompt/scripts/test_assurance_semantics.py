#!/usr/bin/env python3
"""Regression tests for Assurance semantic checks that JSON Schema cannot express."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_candidate import (  # noqa: E402
    DEFAULT_BASE_SCHEMA,
    DEFAULT_EXTENSION_SCHEMA,
    semantic_errors,
)


MODEL_PATH = SCRIPT_DIR.parent / "examples" / "representative_model.json"
EVIDENCE_PATH = SCRIPT_DIR.parent / "examples" / "evidence" / "synthetic_thermal_test_report.json"


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def schema_error_messages(model: dict) -> list[str]:
    base_schema = json.loads(DEFAULT_BASE_SCHEMA.read_text(encoding="utf-8"))
    extension_schema = json.loads(DEFAULT_EXTENSION_SCHEMA.read_text(encoding="utf-8"))
    registry = Registry().with_resource(base_schema["$id"], Resource.from_contents(base_schema))
    validator = Draft202012Validator(
        extension_schema,
        registry=registry,
        format_checker=FormatChecker(),
    )
    return [error.message for error in validator.iter_errors(model)]


def positive_model() -> dict:
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    compliance = model["compliance"]
    compliance["scope"]["assessed_as_of"] = "2026-08-22"
    source = compliance["sources"][0]
    source["status"] = "active"
    source["applicability_version_state"] = "confirmed"
    source["verified_by_ref"] = "ROLE-TEST-REVIEWER"
    source["verified_at"] = "2026-08-22T13:30:00+09:00"
    provision = compliance["provisions"][0]
    provision["verified_by_ref"] = "ROLE-TEST-REVIEWER"
    provision["verified_at"] = "2026-08-22T13:45:00+09:00"

    configuration = model["configurations"][0]
    configuration.update(
        {
            "version": "fixture-baseline-1",
            "baseline_state": "baselined",
            "artifact_locator": MODEL_PATH.resolve().as_uri(),
            "integrity_hash": file_digest(MODEL_PATH),
            "verified_by_ref": "ROLE-TEST-REVIEWER",
            "verified_at": "2026-08-22T13:00:00+09:00",
            "origin": "user_confirmed",
            "confidence": "high",
            "human_confirmation_required": False,
        }
    )

    model["parties_or_roles"] = [
        {
            "id": "ROLE-TEST-REVIEWER",
            "name": "合成独立評価者",
            "kind": "role",
            "organization": None,
            "authority_scope": "合成fixtureの評価",
            "verification_status": "provided_by_user",
            "status": "confirmed",
            "origin": "user_confirmed",
            "confidence": "high",
            "human_confirmation_required": False,
        }
    ]
    activity = compliance["assessment_activities"][0]
    activity["status"] = "completed"
    activity["responsible_party_ref"] = "ROLE-TEST-REVIEWER"
    activity["independence"] = "unknown"
    applicability = compliance["applicability_assessments"][0]
    applicability.update(
        {
            "decision": "applicable",
            "human_confirmation_state": "confirmed",
            "confirmed_by_ref": "ROLE-TEST-REVIEWER",
            "confirmed_at": "2026-08-22T14:00:00+09:00",
        }
    )
    compliance["obligations"][0]["compliance_status"] = "assessed"
    compliance["obligations"][0].update(
        {
            "origin": "user_confirmed",
            "confidence": "high",
            "human_confirmation_required": False,
            "confirmed_by_ref": "ROLE-TEST-REVIEWER",
            "confirmed_at": "2026-08-22T14:15:00+09:00",
        }
    )
    evidence_requirement = compliance["evidence_requirements"][0]
    evidence_requirement.update(
        {
            "status": "confirmed",
            "origin": "user_confirmed",
            "confidence": "high",
            "human_confirmation_required": False,
            "confirmed_by_ref": "ROLE-TEST-REVIEWER",
            "confirmed_at": "2026-08-22T14:30:00+09:00",
        }
    )
    compliance["evidence_items"] = [
        {
            "id": "EVI-0001",
            "evidence_requirement_refs": ["EVR-0001"],
            "evidence_type": "test_report",
            "artifact_locator": EVIDENCE_PATH.resolve().as_uri(),
            "version": "1.0",
            "configuration_ref": "CFG-0001",
            "produced_by_activity_ref": "AST-0001",
            "produced_at": "2026-08-22T15:00:00+09:00",
            "integrity_hash": file_digest(EVIDENCE_PATH),
            "review_state": "reviewed",
            "validity_state": "active",
            "verification_status": "artifact_verified",
            "verified_by_ref": "ROLE-TEST-REVIEWER",
            "verified_at": "2026-08-22T15:30:00+09:00",
            "property_assessments": [
                {
                    "required_property": required_property,
                    "outcome": "satisfied",
                    "rationale": "合成fixtureで当該propertyを満たしたことを確認した。",
                    "verified_by_ref": "ROLE-TEST-REVIEWER",
                    "verified_at": "2026-08-22T15:30:00+09:00",
                }
                for required_property in evidence_requirement["required_properties"]
            ],
        }
    ]
    result = compliance["assessment_results"][0]
    result.update(
        {
            "evidence_item_refs": ["EVI-0001"],
            "outcome": "conforming",
            "finding_refs": [],
            "assessed_at": "2026-08-22T16:00:00+09:00",
            "assessor_ref": "ROLE-TEST-REVIEWER",
            "human_confirmation_state": "confirmed",
            "configuration_ref": "CFG-0001",
            "validity_state": "active",
            "valid_from": "2026-08-22T16:00:00+09:00",
            "valid_to": None,
            "invalidation_reason": None,
            "rationale": "意味検査の正例fixture。実製品の適合主張ではない。",
        }
    )
    compliance["summary"]["assurance_outcome"] = "conforming"
    return model


def expect_failure(name: str, model: dict, text: str) -> None:
    schema_errors = schema_error_messages(model)
    if schema_errors:
        raise AssertionError(f"{name}: negative case must remain schema-valid; actual={schema_errors}")
    errors = semantic_errors(model, SCRIPT_DIR.parent)
    if not any(text in error for error in errors):
        raise AssertionError(f"{name}: expected {text!r}; actual={errors}")


def expect_success(name: str, model: dict) -> None:
    schema_errors = schema_error_messages(model)
    errors = semantic_errors(model, SCRIPT_DIR.parent)
    if schema_errors or errors:
        raise AssertionError(f"{name}: schema={schema_errors}; semantic={errors}")


def expect_rejection(name: str, model: dict, text: str) -> None:
    errors = schema_error_messages(model) + semantic_errors(model, SCRIPT_DIR.parent)
    if not any(text in error for error in errors):
        raise AssertionError(f"{name}: expected {text!r}; actual={errors}")


def issued_model() -> dict:
    model = positive_model()
    compliance = model["compliance"]
    compliance["conformity_schemes"] = [
        {
            "id": "SCH-0001",
            "name": "合成宣言Scheme",
            "scheme_type": "declaration",
            "scheme_owner_ref": "ROLE-TEST-REVIEWER",
            "decision_authority_ref": "ROLE-TEST-REVIEWER",
            "object_of_conformity": {"kind": "configuration", "target_ref": "CFG-0001"},
            "applicability_condition": "合成fixtureだけを対象とする",
            "obligation_refs": ["OBL-0001"],
            "assessment_methods": ["test"],
            "required_evidence_requirement_refs": ["EVR-0001"],
            "independence": "unknown",
            "review_required": True,
            "decision_required": True,
            "output_kind": "declaration",
            "surveillance": {"required": False, "description": None},
            "renewal": {"required": False, "description": None},
            "confirmed_by_ref": "ROLE-TEST-REVIEWER",
            "confirmed_at": "2026-08-22T16:30:00+09:00",
            "origin": "user_confirmed",
            "confidence": "high",
            "human_confirmation_required": False,
        }
    ]
    compliance["attestations"] = [
        {
            "id": "ATT-0001",
            "scheme_ref": "SCH-0001",
            "assessment_result_refs": ["ASR-0001"],
            "output_kind": "declaration",
            "issuer_ref": "ROLE-TEST-REVIEWER",
            "object_ref": "CFG-0001",
            "artifact_locator": MODEL_PATH.resolve().as_uri(),
            "version": "1.0",
            "integrity_hash": file_digest(MODEL_PATH),
            "verified_by_ref": "ROLE-TEST-REVIEWER",
            "verified_at": "2026-08-22T17:30:00+09:00",
            "configuration_ref": "CFG-0001",
            "issued_at": "2026-08-22T17:00:00+09:00",
            "valid_from": "2026-08-22T17:00:00+09:00",
            "valid_to": "2027-08-22T17:00:00+09:00",
            "validity_state": "active",
            "invalidation_reason": None,
            "status": "issued",
            "human_confirmation_state": "confirmed",
        }
    ]
    return model


def main() -> int:
    positive = positive_model()
    expect_success("conforming positive", positive)

    nonconforming = copy.deepcopy(positive)
    nonconforming["compliance"]["assessment_results"][0]["outcome"] = "nonconforming"
    nonconforming["compliance"]["summary"]["assurance_outcome"] = "nonconforming"
    expect_success("nonconforming positive", nonconforming)

    expect_success("issued positive", issued_model())

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_activities"][0]["status"] = "planned"
    expect_failure("unfinished activity", case, "requires completed AssessmentActivity")

    case = copy.deepcopy(positive)
    case["configurations"].append(
        {
            **case["configurations"][0],
            "id": "CFG-0002",
            "name": "別構成",
        }
    )
    case["compliance"]["evidence_items"][0]["configuration_ref"] = "CFG-0002"
    expect_failure("different configuration", case, "configuration mismatch")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["validity_state"] = "stale"
    expect_failure("stale evidence", case, "is not active")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["verification_status"] = "reference_only"
    expect_failure("unverified artifact", case, "artifact is not verified")

    case = copy.deepcopy(positive)
    case["compliance"]["sources"][0]["applicability_version_state"] = "unconfirmed"
    expect_failure("unconfirmed source version", case, "unconfirmed Source version")

    case = copy.deepcopy(positive)
    applicability = case["compliance"]["applicability_assessments"][0]
    applicability.update(
        {
            "decision": "uncertain",
            "human_confirmation_state": "pending",
            "confirmed_by_ref": None,
            "confirmed_at": None,
        }
    )
    expect_failure("uncertain applicability", case, "is not definitively applicable")

    case = copy.deepcopy(positive)
    case["compliance"]["obligations"][0]["compliance_status"] = "candidate"
    expect_failure("candidate obligation", case, "is not in assessed state")

    case = copy.deepcopy(positive)
    case["configurations"][0]["baseline_state"] = "outside_baseline"
    expect_failure("unbaselined configuration", case, "requires a confirmed baselined configuration")

    case = copy.deepcopy(positive)
    case["parties_or_roles"][0]["status"] = "candidate"
    expect_failure("candidate assessor", case, "requires a confirmed authorized assessor")

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_results"][0]["valid_to"] = "2026-08-21T23:59:59+09:00"
    expect_failure("expired result", case, "definitive outcome is expired")

    case = copy.deepcopy(positive)
    result = case["compliance"]["assessment_results"][0]
    result["outcome"] = "inconclusive"
    result["evidence_item_refs"] = []
    result["finding_refs"] = []
    case["compliance"]["summary"]["assurance_outcome"] = "inconclusive"
    expect_failure("empty inconclusive", case, "inconclusive requires EvidenceItem or finding")

    case = issued_model()
    case["compliance"]["assessment_results"][0]["outcome"] = "nonconforming"
    case["compliance"]["summary"]["assurance_outcome"] = "nonconforming"
    expect_failure("issued from nonconforming", case, "requires active conforming results")

    case = issued_model()
    case["parties_or_roles"].append(
        {**case["parties_or_roles"][0], "id": "ROLE-TEST-OTHER", "name": "別の確認済み役割"}
    )
    case["compliance"]["attestations"][0]["issuer_ref"] = "ROLE-TEST-OTHER"
    expect_failure("wrong issuing authority", case, "issuer is not the ConformityScheme decision authority")

    case = issued_model()
    case["compliance"]["attestations"][0]["object_ref"] = "CFG-NOT-FOUND"
    expect_failure("unresolved attestation object", case, "unresolved attestation object")

    case = issued_model()
    extra_obligation = copy.deepcopy(case["compliance"]["obligations"][0])
    extra_obligation["id"] = "OBL-0002"
    case["compliance"]["obligations"].append(extra_obligation)
    case["compliance"]["conformity_schemes"][0]["obligation_refs"].append("OBL-0002")
    expect_failure("incomplete scheme obligation scope", case, "obligations are not fully assessed")

    case = issued_model()
    case["compliance"]["attestations"][0]["valid_to"] = "2026-08-21T23:59:59+09:00"
    expect_failure("expired issued attestation", case, "issued Attestation is expired")

    case = issued_model()
    case["compliance"]["conformity_schemes"][0]["scheme_owner_ref"] = "ROLE-NOT-FOUND"
    expect_failure("unresolved scheme owner", case, "unresolved scheme_owner_ref")

    case = issued_model()
    case["compliance"]["conformity_schemes"][0]["object_of_conformity"]["target_ref"] = "CFG-NOT-FOUND"
    expect_failure("unresolved scheme object", case, "unresolved object of conformity")

    case = issued_model()
    case["compliance"]["conformity_schemes"][0]["obligation_refs"] = ["OBL-NOT-FOUND"]
    expect_failure("unresolved scheme obligation", case, "unresolved Obligation")

    case = issued_model()
    case["compliance"]["conformity_schemes"][0]["required_evidence_requirement_refs"] = [
        "EVR-NOT-FOUND"
    ]
    expect_failure("unresolved scheme evidence", case, "unresolved EvidenceRequirement")

    case = copy.deepcopy(positive)
    candidate_confirmer = {
        **case["parties_or_roles"][0],
        "id": "ROLE-TEST-CANDIDATE-CONFIRMER",
        "name": "未確認の適用性確認者候補",
        "verification_status": "ai_candidate",
        "status": "candidate",
        "origin": "ai_context_inference",
        "human_confirmation_required": True,
    }
    case["parties_or_roles"].append(candidate_confirmer)
    case["compliance"]["applicability_assessments"][0]["confirmed_by_ref"] = candidate_confirmer[
        "id"
    ]
    expect_failure(
        "unauthorized applicability confirmer",
        case,
        "confirmed applicability requires a confirmed authorized human confirmer",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["sources"][0]["verification_status"] = "ai_candidate"
    expect_failure("unverified definitive source", case, "depends on unverified Source")

    case = copy.deepcopy(positive)
    case["compliance"]["sources"][0]["verified_by_ref"] = "ROLE-NOT-FOUND"
    expect_failure(
        "source without authorized verifier",
        case,
        "depends on Source without authorized verification",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["provisions"][0]["verified_by_ref"] = "ROLE-NOT-FOUND"
    expect_failure(
        "provision without authorized verifier",
        case,
        "depends on Provision without authorized verification",
    )

    case = copy.deepcopy(positive)
    source = case["compliance"]["sources"][0]
    source["edition"] = None
    source["effective_from"] = None
    expect_failure(
        "source without version identity",
        case,
        "Source without a confirmed version identity",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["sources"][0]["effective_to"] = "2026-08-21"
    expect_failure("expired definitive source", case, "depends on expired Source")

    case = issued_model()
    case["compliance"]["attestations"][0]["object_ref"] = "ROLE-TEST-REVIEWER"
    expect_failure(
        "attestation scheme object mismatch",
        case,
        "attestation object does not match ConformityScheme object",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_results"][0]["valid_to"] = "not-a-date"
    expect_rejection(
        "invalid result validity timestamp",
        case,
        "invalid definitive outcome valid_to timestamp",
    )

    case = issued_model()
    case["compliance"]["attestations"][0]["valid_to"] = "not-a-date"
    expect_rejection(
        "invalid attestation validity timestamp",
        case,
        "invalid Attestation valid_to timestamp",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_results"][0]["valid_to"] = "2026-08-22T15:00:00+09:00"
    expect_failure("result assessed after validity", case, "assessed_at is after valid_to")

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_results"][0]["valid_from"] = "2026-08-23T00:00:00+09:00"
    expect_failure("result validity starts in future", case, "valid_from is after assessed_at")

    case = issued_model()
    case["compliance"]["attestations"][0]["valid_to"] = "2026-08-22T16:00:00+09:00"
    expect_failure("attestation issued after expiry", case, "issued_at is after valid_to")

    case = issued_model()
    case["compliance"]["attestations"][0]["issued_at"] = "2026-08-22T15:00:00+09:00"
    expect_failure(
        "attestation issued before assessment",
        case,
        "was assessed after issuance",
    )

    case = issued_model()
    case["compliance"]["attestations"][0]["valid_from"] = "2026-08-23T00:00:00+09:00"
    expect_failure("active attestation starts in future", case, "is not yet valid")

    case = copy.deepcopy(positive)
    case["compliance"]["sources"][0]["effective_from"] = "2027-01-01"
    expect_failure("not yet effective source", case, "depends on not-yet-effective Source")

    case = copy.deepcopy(positive)
    result = case["compliance"]["assessment_results"][0]
    result["assessed_at"] = "2027-01-01T16:00:00+09:00"
    result["valid_from"] = "2026-08-22T16:00:00+09:00"
    expect_failure("future assessment", case, "assessed_at is after the model assessment date")

    case = issued_model()
    case["compliance"]["attestations"][0]["issued_at"] = "2027-01-01T17:00:00+09:00"
    expect_failure("future issuance", case, "issued_at is after the model assessment date")

    case = copy.deepcopy(positive)
    case["configurations"][0]["artifact_locator"] = "file:///definitely/missing/configuration.json"
    expect_failure("missing configuration artifact", case, "artifact does not exist")

    case = copy.deepcopy(positive)
    case["configurations"][0]["integrity_hash"] = "sha256:" + "0" * 64
    expect_failure("configuration artifact hash mismatch", case, "artifact SHA-256 mismatch")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["artifact_locator"] = (
        "file:///definitely/missing/evidence.json"
    )
    expect_failure("missing evidence artifact", case, "artifact does not exist")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["integrity_hash"] = "sha256:" + "0" * 64
    expect_failure("evidence artifact hash mismatch", case, "artifact SHA-256 mismatch")

    case = copy.deepcopy(positive)
    other_activity = copy.deepcopy(case["compliance"]["assessment_activities"][0])
    other_activity["id"] = "AST-0002"
    other_activity["status"] = "planned"
    case["compliance"]["assessment_activities"].append(other_activity)
    case["compliance"]["evidence_items"][0]["produced_by_activity_ref"] = "AST-0002"
    expect_failure("evidence from another activity", case, "was produced by another activity")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["produced_at"] = "2026-08-22T18:00:00+09:00"
    expect_failure("evidence produced after assessment", case, "was produced after assessment")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_requirements"][0]["status"] = "planned"
    expect_failure("planned evidence requirement", case, "is not authorized and confirmed")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["property_assessments"] = []
    expect_failure("missing evidence property assessment", case, "does not satisfy property")

    case = issued_model()
    scheme = case["compliance"]["conformity_schemes"][0]
    scheme["origin"] = "ai_context_inference"
    scheme["confidence"] = "low"
    scheme["human_confirmation_required"] = True
    expect_failure("AI candidate scheme", case, "ConformityScheme is not authorized and confirmed")

    case = issued_model()
    case["compliance"]["conformity_schemes"][0]["independence"] = "third_party"
    expect_failure(
        "scheme independence mismatch",
        case,
        "independence does not satisfy ConformityScheme",
    )

    case = copy.deepcopy(positive)
    obligation = case["compliance"]["obligations"][0]
    obligation["origin"] = "ai_context_inference"
    obligation["confidence"] = "low"
    obligation["human_confirmation_required"] = True
    expect_failure("AI candidate obligation", case, "is not authorized and confirmed")

    case = issued_model()
    case["compliance"]["attestations"][0]["artifact_locator"] = (
        "file:///definitely/missing/attestation.json"
    )
    expect_failure("missing attestation artifact", case, "artifact does not exist")

    case = issued_model()
    case["compliance"]["attestations"][0]["integrity_hash"] = "sha256:" + "0" * 64
    expect_failure("attestation artifact hash mismatch", case, "artifact SHA-256 mismatch")

    case = copy.deepcopy(positive)
    case["compliance"]["obligations"][0]["normative_statement_refs"] = []
    case["compliance"]["obligations"][0]["applicability_refs"] = []
    expect_rejection("empty definitive obligation scope", case, "empty legal scope")

    case = issued_model()
    scheme = case["compliance"]["conformity_schemes"][0]
    scheme["obligation_refs"] = []
    scheme["required_evidence_requirement_refs"] = []
    scheme["assessment_methods"] = []
    expect_rejection("empty issued scheme scope", case, "empty issuance scope")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["verified_at"] = "2026-08-22T14:00:00+09:00"
    expect_failure("evidence verified before production", case, "was verified before production")

    case = issued_model()
    case["compliance"]["attestations"][0]["verified_at"] = "2026-08-22T16:00:00+09:00"
    expect_failure("attestation verified before issuance", case, "verified before issuance")

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_requirements"][0]["target_refs"] = ["REQ-0001"]
    expect_failure(
        "evidence requirement misses assessed obligation",
        case,
        "consumed EvidenceRequirements do not cover obligation",
    )

    case = copy.deepcopy(positive)
    extra_requirement = copy.deepcopy(case["compliance"]["evidence_requirements"][0])
    extra_requirement.update(
        {
            "id": "EVR-0002",
            "status": "planned",
            "origin": "ai_context_inference",
            "confidence": "low",
            "human_confirmation_required": True,
            "confirmed_by_ref": None,
            "confirmed_at": None,
        }
    )
    case["compliance"]["evidence_requirements"].append(extra_requirement)
    case["compliance"]["assessment_activities"][0]["planned_evidence_requirement_refs"] = [
        "EVR-0001"
    ]
    case["compliance"]["evidence_items"][0]["evidence_requirement_refs"].append("EVR-0002")
    expect_failure(
        "unplanned unconfirmed consumed evidence requirement",
        case,
        "consumed EvidenceRequirements are outside the activity plan",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_activities"][0]["planned_evidence_requirement_refs"] = []
    expect_failure(
        "post-hoc evidence requirement with empty plan",
        case,
        "consumed EvidenceRequirements are outside the activity plan",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["assessment_results"][0]["assessed_obligation_refs"] = []
    expect_rejection(
        "vacuous definitive outcome",
        case,
        "[] should be non-empty",
    )

    case = copy.deepcopy(positive)
    extra_obligation = copy.deepcopy(case["compliance"]["obligations"][0])
    extra_obligation["id"] = "OBL-9999"
    case["compliance"]["obligations"].append(extra_obligation)
    expect_failure(
        "conforming summary misses applicable obligation",
        case,
        "conforming assurance does not cover applicable obligations OBL-9999",
    )

    case = copy.deepcopy(positive)
    uncertain_applicability = copy.deepcopy(case["compliance"]["applicability_assessments"][0])
    uncertain_applicability.update(
        {
            "id": "APP-9999",
            "decision": "uncertain",
            "human_confirmation_state": "pending",
            "confirmed_by_ref": None,
            "confirmed_at": None,
        }
    )
    case["compliance"]["applicability_assessments"].append(uncertain_applicability)
    extra_obligation = copy.deepcopy(case["compliance"]["obligations"][0])
    extra_obligation.update(
        {
            "id": "OBL-9999",
            "applicability_refs": ["APP-9999"],
            "compliance_status": "candidate",
            "origin": "ai_context_inference",
            "confidence": "low",
            "human_confirmation_required": True,
            "confirmed_by_ref": None,
            "confirmed_at": None,
        }
    )
    case["compliance"]["obligations"].append(extra_obligation)
    expect_failure(
        "conforming summary hides uncertain applicability",
        case,
        "conforming assurance has unresolved applicability APP-9999",
    )

    case = copy.deepcopy(positive)
    case["compliance"]["evidence_items"][0]["property_assessments"][0]["verified_at"] = (
        "2026-08-22T14:00:00+09:00"
    )
    expect_failure(
        "evidence property verified before production",
        case,
        "property was verified before production",
    )

    case = issued_model()
    case["compliance"]["evidence_requirements"][0]["status"] = "planned"
    expect_failure(
        "unconfirmed scheme evidence requirement",
        case,
        "Scheme EvidenceRequirement EVR-0001 is not authorized and confirmed",
    )

    case = issued_model()
    case["compliance"]["attestations"][0]["output_kind"] = "certificate"
    expect_failure("attestation output mismatch", case, "output kind does not match")

    case = copy.deepcopy(positive)
    case["compliance"]["provisions"][0]["verification_status"] = "ai_candidate"
    expect_failure("unverified definitive provision", case, "depends on unverified Provision")

    case = copy.deepcopy(positive)
    case["compliance"]["applicability_assessments"][0]["confirmed_at"] = (
        "2027-01-01T00:00:00+09:00"
    )
    expect_failure("future applicability confirmation", case, "was confirmed after assessment")

    expired = issued_model()
    expired_attestation = expired["compliance"]["attestations"][0]
    expired_attestation.update(
        {
            "status": "expired",
            "validity_state": "stale",
            "invalidation_reason": "合成fixtureの期限満了",
        }
    )
    expect_success("expired attestation state", expired)

    print("PASS assurance integrated regression positives=4 negatives=65")
    return 0


if __name__ == "__main__":
    sys.exit(main())
