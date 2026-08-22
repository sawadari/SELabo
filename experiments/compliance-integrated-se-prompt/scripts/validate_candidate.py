#!/usr/bin/env python3
"""Validate a Compliance-integrated SELabo candidate and export traceability CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_EXTENSION_SCHEMA = SCRIPT_DIR.parent / "schemas" / "compliance_se_model.schema.json"
DEFAULT_BASE_SCHEMA = SCRIPT_DIR.parent.parent / "hierarchical-se-prompt" / "schemas" / "se_model.schema.json"

PRODUCT_KINDS = {
    "product_requirement",
    "interface_requirement",
    "constraint_requirement",
    "operational_requirement",
}
NON_PRODUCT_KINDS = {
    "process_requirement",
    "assurance_requirement",
    "organizational_requirement",
    "documentation_requirement",
    "supplier_requirement",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_ids(value: Any) -> tuple[dict[str, dict[str, Any]], list[str]]:
    objects: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            element_id = node.get("id")
            if isinstance(element_id, str):
                if element_id in objects:
                    duplicates.append(element_id)
                else:
                    objects[element_id] = node
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return objects, duplicates


def origin_fields(element: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(element.get("origin", "ai_context_inference")),
        str(element.get("confidence", "medium")),
        str(element.get("validity_state", "active")),
    )


def relation_id(relation_type: str, source_id: str, target_id: str) -> str:
    payload = f"{relation_type}\0{source_id}\0{target_id}".encode("utf-8")
    return "DREL-" + hashlib.sha256(payload).hexdigest()[:16].upper()


def derive_trace_rows(model: dict[str, Any]) -> list[dict[str, str]]:
    rows: dict[tuple[str, str, str], dict[str, str]] = {}

    def add(
        relation_type: str,
        source_id: str,
        target_id: str,
        rationale: str,
        source: dict[str, Any],
    ) -> None:
        if not source_id or not target_id:
            return
        key = (relation_type, source_id, target_id)
        origin, confidence, validity_state = origin_fields(source)
        rows[key] = {
            "relation_id": relation_id(*key),
            "relation_type": relation_type,
            "source_id": source_id,
            "target_id": target_id,
            "rationale": rationale,
            "origin": origin,
            "confidence": confidence,
            "validity_state": validity_state,
        }

    for need in model.get("needs", []):
        for stakeholder_ref in need.get("stakeholder_refs", []):
            add("elicits", stakeholder_ref, need["id"], "Need.stakeholder_refs", need)
        for validation_ref in need.get("validation_case_refs", []):
            add("validated_by", need["id"], validation_ref, "Need.validation_case_refs", need)

    for requirement in model.get("requirements", []):
        for need_ref in requirement.get("source_need_refs", []):
            add("derives_from", requirement["id"], need_ref, "Requirement.source_need_refs", requirement)
        for parent_ref in requirement.get("parent_requirement_refs", []):
            add("derives_from", requirement["id"], parent_ref, "Requirement.parent_requirement_refs", requirement)

    for behavior in model.get("behaviors", []):
        for requirement_ref in behavior.get("requirement_refs", []):
            add("realizes", behavior["id"], requirement_ref, "Behavior.requirement_refs", behavior)

    for structure in model.get("structures", []):
        for requirement_ref in structure.get("requirement_refs", []):
            add("satisfies", structure["id"], requirement_ref, "Structure.requirement_refs", structure)
        for behavior_ref in structure.get("behavior_refs", []):
            add("performs", structure["id"], behavior_ref, "Structure.behavior_refs", structure)

    for verification in model.get("verification_cases", []):
        for requirement_ref in verification.get("target_requirement_refs", []):
            add("verifies", verification["id"], requirement_ref, "VerificationCase.target_requirement_refs", verification)

    for validation in model.get("validation_cases", []):
        for need_ref in validation.get("target_need_refs", []):
            add("validates", validation["id"], need_ref, "ValidationCase.target_need_refs", validation)

    compliance = model.get("compliance", {})
    for source in compliance.get("sources", []):
        for authority_ref in source.get("authority_refs", []):
            add("traces_to", source["id"], authority_ref, "Source.authority_refs", source)
    for provision in compliance.get("provisions", []):
        add("traces_to", provision["id"], provision.get("source_ref", ""), "Provision.source_ref", provision)
    for statement in compliance.get("normative_statements", []):
        for provision_ref in statement.get("provision_refs", []):
            add("traces_to", statement["id"], provision_ref, "NormativeStatement.provision_refs", statement)
    for assessment in compliance.get("applicability_assessments", []):
        for statement_ref in assessment.get("normative_statement_refs", []):
            add("traces_to", assessment["id"], statement_ref, "ApplicabilityAssessment.normative_statement_refs", assessment)
    for obligation in compliance.get("obligations", []):
        for statement_ref in obligation.get("normative_statement_refs", []):
            add("derives_from", obligation["id"], statement_ref, "Obligation.normative_statement_refs", obligation)
        for applicability_ref in obligation.get("applicability_refs", []):
            add("traces_to", obligation["id"], applicability_ref, "Obligation.applicability_refs", obligation)
    for projection in compliance.get("engineering_projections", []):
        for obligation_ref in projection.get("obligation_refs", []):
            add("derives_from", projection["id"], obligation_ref, "EngineeringProjection.obligation_refs", projection)
        for target_ref in projection.get("target_refs", []):
            add("traces_to", projection["id"], target_ref, "EngineeringProjection.target_refs", projection)
    for evidence_requirement in compliance.get("evidence_requirements", []):
        for target_ref in evidence_requirement.get("target_refs", []):
            add("traces_to", evidence_requirement["id"], target_ref, "EvidenceRequirement.target_refs", evidence_requirement)
    for evidence_item in compliance.get("evidence_items", []):
        for requirement_ref in evidence_item.get("evidence_requirement_refs", []):
            add("evidenced_by", requirement_ref, evidence_item["id"], "EvidenceItem.evidence_requirement_refs", evidence_item)
    for activity in compliance.get("assessment_activities", []):
        for obligation_ref in activity.get("target_obligation_refs", []):
            add("traces_to", activity["id"], obligation_ref, "AssessmentActivity.target_obligation_refs", activity)
        for evidence_ref in activity.get("planned_evidence_requirement_refs", []):
            add("traces_to", activity["id"], evidence_ref, "AssessmentActivity.planned_evidence_requirement_refs", activity)
        for configuration_ref in activity.get("configuration_refs", []):
            add("applies_to", activity["id"], configuration_ref, "AssessmentActivity.configuration_refs", activity)
    for result in compliance.get("assessment_results", []):
        add("traces_to", result["id"], result.get("assessment_activity_ref", ""), "AssessmentResult.assessment_activity_ref", result)
        for evidence_ref in result.get("evidence_item_refs", []):
            add("evidenced_by", result["id"], evidence_ref, "AssessmentResult.evidence_item_refs", result)

    for explicit in model.get("relations", []):
        key = (explicit["relation_type"], explicit["source_id"], explicit["target_id"])
        if key in rows:
            continue
        rows[key] = {
            "relation_id": explicit["id"],
            "relation_type": explicit["relation_type"],
            "source_id": explicit["source_id"],
            "target_id": explicit["target_id"],
            "rationale": explicit.get("rationale", "Explicit relation"),
            "origin": explicit.get("origin", "ai_context_inference"),
            "confidence": explicit.get("confidence", "medium"),
            "validity_state": explicit.get("validity_state", "active"),
        }

    return [rows[key] for key in sorted(rows)]


def semantic_errors(model: dict[str, Any], artifact_base: Path | None = None) -> list[str]:
    errors: list[str] = []
    objects, duplicates = collect_ids(model)
    if duplicates:
        errors.append("Duplicate IDs: " + ", ".join(sorted(set(duplicates))))

    requirements = {item["id"]: item for item in model.get("requirements", [])}
    needs = {item["id"]: item for item in model.get("needs", [])}
    stakeholders = {item["id"]: item for item in model.get("stakeholders", [])}
    scenarios = {item["id"]: item for item in model.get("scenarios", [])}
    structures = {item["id"]: item for item in model.get("structures", [])}
    behaviors = {item["id"]: item for item in model.get("behaviors", [])}
    verifications = {item["id"]: item for item in model.get("verification_cases", [])}
    validations = {item["id"]: item for item in model.get("validation_cases", [])}
    projection_targets = {item["id"]: item for item in model.get("projection_targets", [])}
    configurations = {item["id"]: item for item in model.get("configurations", [])}
    parties = {item["id"]: item for item in model.get("parties_or_roles", [])}
    compliance = model.get("compliance", {})
    sources = {item["id"]: item for item in compliance.get("sources", [])}
    provisions = {item["id"]: item for item in compliance.get("provisions", [])}
    statements = {item["id"]: item for item in compliance.get("normative_statements", [])}
    obligations = {item["id"]: item for item in compliance.get("obligations", [])}
    applicability = {
        item["id"]: item for item in compliance.get("applicability_assessments", [])
    }
    projections = {item["id"]: item for item in compliance.get("engineering_projections", [])}
    evidence_requirements = {item["id"]: item for item in compliance.get("evidence_requirements", [])}
    evidence_items = {item["id"]: item for item in compliance.get("evidence_items", [])}
    activities = {item["id"]: item for item in compliance.get("assessment_activities", [])}
    results = {item["id"]: item for item in compliance.get("assessment_results", [])}
    schemes = {item["id"]: item for item in compliance.get("conformity_schemes", [])}

    assessed_as_of: date | None = None
    try:
        assessed_as_of = date.fromisoformat(compliance.get("scope", {}).get("assessed_as_of", ""))
    except ValueError:
        pass

    def parse_timestamp(value: Any) -> datetime | None:
        if not isinstance(value, str) or not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

    def is_confirmed_authorized(party_ref: Any) -> bool:
        party = parties.get(party_ref, {})
        return (
            party.get("status") == "confirmed"
            and party.get("verification_status") == "provided_by_user"
            and bool(party.get("authority_scope"))
        )

    def verify_local_artifact(record_id: str, locator: Any, integrity_hash: Any) -> None:
        if not isinstance(locator, str) or not locator:
            errors.append(f"{record_id}: missing artifact locator")
            return
        if not isinstance(integrity_hash, str) or not integrity_hash.startswith("sha256:"):
            errors.append(f"{record_id}: missing SHA-256 integrity hash")
            return
        parsed = urlparse(locator)
        if parsed.scheme == "file":
            raw_path = unquote(parsed.path)
            if len(raw_path) >= 3 and raw_path[0] == "/" and raw_path[2] == ":":
                raw_path = raw_path[1:]
            artifact_path = Path(raw_path)
        elif parsed.scheme:
            errors.append(f"{record_id}: definitive state requires a locally verifiable artifact")
            return
        else:
            artifact_path = Path(locator)
            if not artifact_path.is_absolute():
                if artifact_base is None:
                    errors.append(f"{record_id}: relative artifact cannot be resolved")
                    return
                artifact_path = artifact_base / artifact_path
        if not artifact_path.is_file():
            errors.append(f"{record_id}: artifact does not exist at {locator}")
            return
        actual_hash = "sha256:" + hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        if actual_hash.lower() != integrity_hash.lower():
            errors.append(f"{record_id}: artifact SHA-256 mismatch")

    for configuration_ref in compliance.get("scope", {}).get("configuration_refs", []):
        if configuration_ref not in configurations:
            errors.append(f"ComplianceScope: unresolved configuration {configuration_ref}")

    for assessment in applicability.values():
        if assessment.get("human_confirmation_state") == "confirmed":
            confirmer_ref = assessment.get("confirmed_by_ref")
            confirmer = parties.get(confirmer_ref, {})
            if (
                confirmer.get("status") != "confirmed"
                or confirmer.get("verification_status") != "provided_by_user"
                or not confirmer.get("authority_scope")
            ):
                errors.append(
                    f"{assessment['id']}: confirmed applicability requires a confirmed authorized human confirmer"
                )

    for scheme in schemes.values():
        scheme_id = scheme["id"]
        for field_name in ("scheme_owner_ref", "decision_authority_ref"):
            party_ref = scheme.get(field_name)
            if party_ref is not None and party_ref not in parties:
                errors.append(f"{scheme_id}: unresolved {field_name} {party_ref}")
        object_ref = scheme.get("object_of_conformity", {}).get("target_ref")
        if object_ref not in objects:
            errors.append(f"{scheme_id}: unresolved object of conformity {object_ref}")
        for obligation_ref in scheme.get("obligation_refs", []):
            if obligation_ref not in obligations:
                errors.append(f"{scheme_id}: unresolved Obligation {obligation_ref}")
        for evidence_ref in scheme.get("required_evidence_requirement_refs", []):
            if evidence_ref not in evidence_requirements:
                errors.append(f"{scheme_id}: unresolved EvidenceRequirement {evidence_ref}")

    for need in needs.values():
        validation_refs = need.get("validation_case_refs", [])
        if not validation_refs and not need.get("success_measure_refs", []):
            errors.append(f"{need['id']}: no ValidationCase or success measure")
        for validation_ref in validation_refs:
            validation = validations.get(validation_ref)
            if validation is None:
                errors.append(f"{need['id']}: unresolved ValidationCase {validation_ref}")
            elif need["id"] not in validation.get("target_need_refs", []):
                errors.append(f"{need['id']}: ValidationCase {validation_ref} does not target the Need")

    for validation in validations.values():
        validation_id = validation["id"]
        if not validation.get("scenario_refs") and not validation.get("success_measure_refs"):
            errors.append(f"{validation_id}: requires a representative Scenario or success measure")
        for need_ref in validation.get("target_need_refs", []):
            need = needs.get(need_ref)
            if need is None:
                errors.append(f"{validation_id}: unresolved Need {need_ref}")
            elif validation_id not in need.get("validation_case_refs", []):
                errors.append(f"{validation_id}: Need {need_ref} does not reference the ValidationCase")
        for stakeholder_ref in validation.get("representative_stakeholder_refs", []):
            if stakeholder_ref not in stakeholders:
                errors.append(f"{validation_id}: unresolved representative stakeholder {stakeholder_ref}")
        for scenario_ref in validation.get("scenario_refs", []):
            if scenario_ref not in scenarios:
                errors.append(f"{validation_id}: unresolved Scenario {scenario_ref}")

    for scenario in scenarios.values():
        scenario_id = scenario["id"]
        if not scenario.get("actor_refs"):
            errors.append(f"{scenario_id}: requires at least one actor")
        for actor_ref in scenario.get("actor_refs", []):
            if actor_ref not in stakeholders:
                errors.append(f"{scenario_id}: unresolved actor {actor_ref}")
        if not scenario.get("main_flow"):
            errors.append(f"{scenario_id}: requires a non-empty main flow")
        if not scenario.get("observable_results"):
            errors.append(f"{scenario_id}: requires at least one observable result")
        if not scenario.get("postconditions"):
            errors.append(f"{scenario_id}: requires at least one postcondition")

    for verification in verifications.values():
        verification_id = verification["id"]
        role_ref = verification.get("responsible_role_ref")
        if role_ref not in parties:
            errors.append(f"{verification_id}: unresolved responsible role {role_ref}")
        configuration_ref = verification.get("configuration")
        if configuration_ref is not None and configuration_ref not in configurations:
            errors.append(f"{verification_id}: unresolved configuration {configuration_ref}")

    for requirement in requirements.values():
        requirement_id = requirement["id"]
        for allocation_ref in requirement.get("allocation_candidate_refs", []):
            structure = structures.get(allocation_ref)
            if structure is None:
                errors.append(f"{requirement_id}: unresolved allocation candidate {allocation_ref}")
            elif requirement_id not in structure.get("requirement_refs", []):
                errors.append(
                    f"{requirement_id}: allocation candidate {allocation_ref} does not satisfy the Requirement"
                )

    for behavior in behaviors.values():
        candidate_performers = set(behavior.get("performer_candidate_refs", []))
        for candidate_ref in candidate_performers:
            if candidate_ref not in structures and candidate_ref not in stakeholders:
                errors.append(f"{behavior['id']}: unresolved performer candidate {candidate_ref}")
        performers = [
            structure
            for structure in structures.values()
            if behavior["id"] in structure.get("behavior_refs", [])
        ]
        if not performers:
            errors.append(f"{behavior['id']}: no performing Structure")
        for performer in performers:
            if (
                candidate_performers
                and performer["id"] not in candidate_performers
                and performer.get("owner_ref") not in candidate_performers
            ):
                errors.append(
                    f"{behavior['id']}: performer {performer['id']} and owner do not match performer candidates"
                )
            missing = set(behavior.get("requirement_refs", [])) - set(
                performer.get("requirement_refs", [])
            )
            if missing:
                errors.append(
                    f"{behavior['id']}: performer {performer['id']} does not satisfy "
                    + ", ".join(sorted(missing))
                )

    for structure in structures.values():
        owner_ref = structure.get("owner_ref")
        if owner_ref is not None and owner_ref not in stakeholders and owner_ref not in parties:
            errors.append(f"{structure['id']}: unresolved owner {owner_ref}")

    scope_markets = set(compliance.get("scope", {}).get("markets", []))
    for assessment in applicability.values():
        assessment_id = assessment["id"]
        for statement_ref in assessment.get("normative_statement_refs", []):
            if statement_ref not in statements:
                errors.append(f"{assessment_id}: unresolved NormativeStatement {statement_ref}")
        context = assessment.get("assessment_context", {})
        if context.get("configuration_ref") not in configurations:
            errors.append(
                f"{assessment_id}: unresolved configuration {context.get('configuration_ref')}"
            )
        if context.get("market") not in scope_markets:
            errors.append(f"{assessment_id}: market is outside ComplianceScope")
        confirmation_state = assessment.get("human_confirmation_state")
        if confirmation_state == "confirmed":
            confirmer_ref = assessment.get("confirmed_by_ref")
            if confirmer_ref not in parties:
                errors.append(f"{assessment_id}: unresolved human confirmer {confirmer_ref}")
            if not assessment.get("confirmed_at"):
                errors.append(f"{assessment_id}: confirmed applicability requires confirmed_at")

    discovery_records = compliance.get("regulatory_discovery_log", [])
    covered_sources: set[str] = set()
    for record in discovery_records:
        record_id = record["id"]
        if record.get("configuration_ref") not in configurations:
            errors.append(
                f"{record_id}: unresolved configuration {record.get('configuration_ref')}"
            )
        if record.get("market") not in scope_markets:
            errors.append(f"{record_id}: market is outside ComplianceScope")
        for source_ref in record.get("candidate_source_refs", []):
            if source_ref not in sources:
                errors.append(f"{record_id}: unresolved candidate Source {source_ref}")
            else:
                covered_sources.add(source_ref)
        if record.get("query_log_state") == "complete" and not record.get("queries"):
            errors.append(f"{record_id}: complete query log requires at least one query")
        if record.get("query_log_state") == "unavailable_legacy_run" and record.get("queries"):
            errors.append(f"{record_id}: unavailable legacy query log must not invent queries")
    if sources and discovery_records:
        for source_id in sorted(set(sources) - covered_sources):
            errors.append(f"RegulatoryDiscoveryLog: Source {source_id} has no disposition record")

    for projection in projections.values():
        projection_id = projection["id"]
        kind = projection["projection_kind"]
        for obligation_ref in projection["obligation_refs"]:
            if obligation_ref not in obligations:
                errors.append(f"{projection_id}: unresolved obligation {obligation_ref}")
        for target_ref in projection["target_refs"]:
            if kind in PRODUCT_KINDS:
                if target_ref not in requirements:
                    errors.append(f"{projection_id}: {kind} target {target_ref} is not a Requirement")
            elif kind in NON_PRODUCT_KINDS:
                target = projection_targets.get(target_ref)
                if target is None:
                    errors.append(f"{projection_id}: unresolved projection target {target_ref}")
                elif target.get("target_kind") != kind:
                    errors.append(
                        f"{projection_id}: target {target_ref} kind {target.get('target_kind')} != {kind}"
                    )
            elif kind == "evidence_requirement" and target_ref not in evidence_requirements:
                errors.append(f"{projection_id}: unresolved EvidenceRequirement {target_ref}")

    for target in projection_targets.values():
        responsible_ref = target.get("responsible_role_ref")
        if responsible_ref is not None and responsible_ref not in parties:
            errors.append(f"{target['id']}: unresolved responsible role {responsible_ref}")

    for requirement in requirements.values():
        for source in requirement.get("derivation_sources", []):
            if source.get("source_kind") != "compliance_obligation":
                continue
            obligation_ref = source["source_ref"]
            projection_ref = source.get("projection_ref")
            if obligation_ref not in obligations:
                errors.append(f"{requirement['id']}: unresolved compliance obligation {obligation_ref}")
            projection = projections.get(projection_ref)
            if projection is None:
                errors.append(f"{requirement['id']}: unresolved projection {projection_ref}")
            elif requirement["id"] not in projection.get("target_refs", []):
                errors.append(f"{requirement['id']}: projection {projection_ref} does not target the requirement")

    projected_obligations = {
        ref for projection in projections.values() for ref in projection.get("obligation_refs", [])
    }
    evidence_targets = {
        ref for evidence in evidence_requirements.values() for ref in evidence.get("target_refs", [])
    }
    for obligation in obligations.values():
        obligation_id = obligation["id"]
        if obligation_id not in projected_obligations:
            errors.append(f"{obligation_id}: no EngineeringProjection")
        if obligation["obligation_kind"] in {"mandatory", "prohibition"} and obligation_id not in evidence_targets:
            errors.append(f"{obligation_id}: no EvidenceRequirement")

    for evidence in evidence_items.values():
        evidence_id = evidence["id"]
        for requirement_ref in evidence.get("evidence_requirement_refs", []):
            if requirement_ref not in evidence_requirements:
                errors.append(f"{evidence_id}: unresolved EvidenceRequirement {requirement_ref}")
        if evidence.get("configuration_ref") not in configurations:
            errors.append(f"{evidence_id}: unresolved configuration {evidence.get('configuration_ref')}")
        if evidence.get("produced_by_activity_ref") not in activities:
            errors.append(f"{evidence_id}: unresolved producing activity {evidence.get('produced_by_activity_ref')}")

    for activity in activities.values():
        activity_id = activity["id"]
        for configuration_ref in activity.get("configuration_refs", []):
            if configuration_ref not in configurations:
                errors.append(f"{activity_id}: unresolved configuration {configuration_ref}")
        responsible_ref = activity.get("responsible_party_ref")
        if responsible_ref is not None and responsible_ref not in parties:
            errors.append(f"{activity_id}: unresolved responsible party {responsible_ref}")
        for requirement_ref in activity.get("planned_evidence_requirement_refs", []):
            if requirement_ref not in evidence_requirements:
                errors.append(f"{activity_id}: unresolved EvidenceRequirement {requirement_ref}")

    for result in results.values():
        result_id = result["id"]
        activity = activities.get(result.get("assessment_activity_ref"))
        if activity is None:
            errors.append(f"{result_id}: unresolved AssessmentActivity {result.get('assessment_activity_ref')}")
            continue
        if result.get("configuration_ref") not in configurations:
            errors.append(f"{result_id}: unresolved configuration {result.get('configuration_ref')}")
        if result.get("configuration_ref") not in activity.get("configuration_refs", []):
            errors.append(f"{result_id}: configuration is outside AssessmentActivity scope")
        if not set(result.get("assessed_obligation_refs", [])).issubset(
            set(activity.get("target_obligation_refs", []))
        ):
            errors.append(f"{result_id}: assessed obligations are outside AssessmentActivity scope")

        outcome = result.get("outcome")
        referenced_evidence = []
        for evidence_ref in result.get("evidence_item_refs", []):
            evidence = evidence_items.get(evidence_ref)
            if evidence is None:
                errors.append(f"{result_id}: unresolved EvidenceItem {evidence_ref}")
            else:
                referenced_evidence.append(evidence)
                if evidence.get("configuration_ref") != result.get("configuration_ref"):
                    errors.append(f"{result_id}: EvidenceItem {evidence_ref} configuration mismatch")

        if outcome in {"inconclusive", "conforming", "nonconforming"}:
            if activity.get("status") != "completed":
                errors.append(f"{result_id}: performed outcome requires completed AssessmentActivity")
            if not result.get("assessed_at") or not result.get("assessor_ref"):
                errors.append(f"{result_id}: performed outcome requires assessed_at and assessor_ref")
            elif result["assessor_ref"] not in parties:
                errors.append(f"{result_id}: unresolved assessor {result['assessor_ref']}")
        if outcome == "inconclusive" and not referenced_evidence and not result.get("finding_refs", []):
            errors.append(f"{result_id}: inconclusive requires EvidenceItem or finding")
        if outcome in {"conforming", "nonconforming"}:
            assessed_at_time = parse_timestamp(result.get("assessed_at"))
            planned = set(activity.get("planned_evidence_requirement_refs", []))
            provided = {
                requirement_ref
                for evidence in referenced_evidence
                for requirement_ref in evidence.get("evidence_requirement_refs", [])
            }
            if not result.get("assessed_obligation_refs"):
                errors.append(f"{result_id}: definitive outcome requires at least one assessed obligation")
            if not planned.issubset(provided):
                errors.append(f"{result_id}: planned EvidenceRequirements are not fully evidenced")
            if not provided.issubset(planned):
                errors.append(f"{result_id}: consumed EvidenceRequirements are outside the activity plan")
            for obligation_ref in result.get("assessed_obligation_refs", []):
                if not any(
                    obligation_ref in evidence_requirements.get(requirement_ref, {}).get(
                        "target_refs", []
                    )
                    for requirement_ref in provided
                ):
                    errors.append(
                        f"{result_id}: consumed EvidenceRequirements do not cover obligation {obligation_ref}"
                    )
            for requirement_ref in provided:
                requirement = evidence_requirements.get(requirement_ref, {})
                requirement_confirmed_at = parse_timestamp(requirement.get("confirmed_at"))
                if (
                    requirement.get("status") != "confirmed"
                    or requirement.get("origin") != "user_confirmed"
                    or requirement.get("human_confirmation_required") is not False
                    or not is_confirmed_authorized(requirement.get("confirmed_by_ref"))
                    or requirement_confirmed_at is None
                ):
                    errors.append(
                        f"{result_id}: EvidenceRequirement {requirement_ref} is not authorized and confirmed"
                    )
                if assessed_at_time and requirement_confirmed_at and requirement_confirmed_at > assessed_at_time:
                    errors.append(
                        f"{result_id}: EvidenceRequirement {requirement_ref} was confirmed after assessment"
                    )
            for evidence in referenced_evidence:
                evidence_id = evidence["id"]
                if evidence.get("review_state") != "reviewed":
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} is not reviewed")
                if evidence.get("validity_state") != "active":
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} is not active")
                if evidence.get("verification_status") != "artifact_verified":
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} artifact is not verified")
                if evidence.get("produced_by_activity_ref") != result.get("assessment_activity_ref"):
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} was produced by another activity")
                producing_activity = activities.get(evidence.get("produced_by_activity_ref"), {})
                if producing_activity.get("status") != "completed":
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} producing activity is not completed")
                produced_at_time = parse_timestamp(evidence.get("produced_at"))
                if assessed_at_time and produced_at_time and produced_at_time > assessed_at_time:
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} was produced after assessment")
                if not is_confirmed_authorized(evidence.get("verified_by_ref")):
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} verifier is not authorized")
                evidence_verified_at = parse_timestamp(evidence.get("verified_at"))
                if produced_at_time and evidence_verified_at and evidence_verified_at < produced_at_time:
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} was verified before production")
                if assessed_at_time and evidence_verified_at and evidence_verified_at > assessed_at_time:
                    errors.append(f"{result_id}: EvidenceItem {evidence_id} was verified after assessment")
                verify_local_artifact(
                    evidence_id,
                    evidence.get("artifact_locator"),
                    evidence.get("integrity_hash"),
                )
                for requirement_ref in evidence.get("evidence_requirement_refs", []):
                    requirement = evidence_requirements.get(requirement_ref)
                    if requirement is None:
                        continue
                    if evidence.get("evidence_type") != requirement.get("evidence_type"):
                        errors.append(
                            f"{result_id}: EvidenceItem {evidence_id} type does not match {requirement_ref}"
                        )
                    property_assessments = evidence.get("property_assessments", [])
                    property_names = [item.get("required_property") for item in property_assessments]
                    if len(property_names) != len(set(property_names)):
                        errors.append(f"{result_id}: EvidenceItem {evidence_id} has duplicate property assessments")
                    property_map = {
                        item.get("required_property"): item for item in property_assessments
                    }
                    for required_property in requirement.get("required_properties", []):
                        property_result = property_map.get(required_property, {})
                        if property_result.get("outcome") != "satisfied":
                            errors.append(
                                f"{result_id}: EvidenceItem {evidence_id} does not satisfy property {required_property}"
                            )
                        if not is_confirmed_authorized(property_result.get("verified_by_ref")):
                            errors.append(
                                f"{result_id}: EvidenceItem {evidence_id} property verifier is not authorized"
                            )
                        property_verified_at = parse_timestamp(property_result.get("verified_at"))
                        if produced_at_time and property_verified_at and property_verified_at < produced_at_time:
                            errors.append(
                                f"{result_id}: EvidenceItem {evidence_id} property was verified before production"
                            )
                        if assessed_at_time and property_verified_at and property_verified_at > assessed_at_time:
                            errors.append(
                                f"{result_id}: EvidenceItem {evidence_id} property was verified after assessment"
                            )
                    required_independence = requirement.get("independence_required")
                    if required_independence not in {"none", "unknown"} and (
                        activity.get("independence") != required_independence
                    ):
                        errors.append(
                            f"{result_id}: AssessmentActivity independence does not satisfy {requirement_ref}"
                        )
            if result.get("validity_state") != "active":
                errors.append(f"{result_id}: definitive outcome must be active")
            valid_from_time = parse_timestamp(result.get("valid_from"))
            valid_to_time = parse_timestamp(result.get("valid_to"))
            if result.get("assessed_at") and assessed_at_time is None:
                errors.append(f"{result_id}: invalid definitive outcome assessed_at timestamp")
            if result.get("valid_from") and valid_from_time is None:
                errors.append(f"{result_id}: invalid definitive outcome valid_from timestamp")
            if result.get("valid_to") and valid_to_time is None:
                errors.append(f"{result_id}: invalid definitive outcome valid_to timestamp")
            if assessed_at_time and valid_from_time and valid_from_time > assessed_at_time:
                errors.append(f"{result_id}: valid_from is after assessed_at")
            if assessed_at_time and valid_to_time and assessed_at_time > valid_to_time:
                errors.append(f"{result_id}: assessed_at is after valid_to")
            if valid_from_time and valid_to_time and valid_from_time > valid_to_time:
                errors.append(f"{result_id}: valid_from is after valid_to")
            if assessed_as_of and valid_from_time and valid_from_time.date() > assessed_as_of:
                errors.append(f"{result_id}: active definitive outcome is not yet valid")
            if assessed_as_of and assessed_at_time and assessed_at_time.date() > assessed_as_of:
                errors.append(f"{result_id}: assessed_at is after the model assessment date")
            if assessed_as_of and valid_to_time and valid_to_time.date() < assessed_as_of:
                errors.append(f"{result_id}: definitive outcome is expired as of assessment date")

            configuration = configurations.get(result.get("configuration_ref"), {})
            if (
                configuration.get("validity_state") != "active"
                or configuration.get("baseline_state") != "baselined"
                or not configuration.get("version")
                or not configuration.get("artifact_locator")
                or not configuration.get("integrity_hash")
                or configuration.get("origin") != "user_confirmed"
                or configuration.get("human_confirmation_required") is not False
            ):
                errors.append(f"{result_id}: definitive outcome requires a confirmed baselined configuration")
            if not is_confirmed_authorized(configuration.get("verified_by_ref")):
                errors.append(f"{result_id}: configuration verifier is not authorized")
            configuration_verified_at = parse_timestamp(configuration.get("verified_at"))
            if assessed_at_time and configuration_verified_at and configuration_verified_at > assessed_at_time:
                errors.append(f"{result_id}: configuration was verified after assessment")
            verify_local_artifact(
                configuration.get("id", str(result.get("configuration_ref"))),
                configuration.get("artifact_locator"),
                configuration.get("integrity_hash"),
            )

            assessor = parties.get(result.get("assessor_ref"), {})
            if (
                assessor.get("status") != "confirmed"
                or assessor.get("verification_status") != "provided_by_user"
                or not assessor.get("authority_scope")
            ):
                errors.append(f"{result_id}: definitive outcome requires a confirmed authorized assessor")

            for obligation_ref in result.get("assessed_obligation_refs", []):
                obligation = obligations.get(obligation_ref, {})
                obligation_confirmed_at = parse_timestamp(obligation.get("confirmed_at"))
                if obligation.get("compliance_status") != "assessed":
                    errors.append(f"{result_id}: obligation {obligation_ref} is not in assessed state")
                if not obligation.get("normative_statement_refs") or not obligation.get(
                    "applicability_refs"
                ):
                    errors.append(f"{result_id}: obligation {obligation_ref} has an empty legal scope")
                if (
                    obligation.get("origin") != "user_confirmed"
                    or obligation.get("human_confirmation_required") is not False
                    or not is_confirmed_authorized(obligation.get("confirmed_by_ref"))
                    or obligation_confirmed_at is None
                ):
                    errors.append(f"{result_id}: obligation {obligation_ref} is not authorized and confirmed")
                if assessed_at_time and obligation_confirmed_at and obligation_confirmed_at > assessed_at_time:
                    errors.append(f"{result_id}: obligation {obligation_ref} was confirmed after assessment")
                for applicability_ref in obligation.get("applicability_refs", []):
                    assessment = applicability.get(applicability_ref, {})
                    if assessment.get("decision") not in {"applicable", "partially_applicable"}:
                        errors.append(
                            f"{result_id}: applicability {applicability_ref} is not definitively applicable"
                        )
                    if assessment.get("human_confirmation_state") != "confirmed":
                        errors.append(
                            f"{result_id}: applicability {applicability_ref} is not human-confirmed"
                        )
                    applicability_confirmed_at = parse_timestamp(assessment.get("confirmed_at"))
                    if assessed_at_time and applicability_confirmed_at and (
                        applicability_confirmed_at > assessed_at_time
                    ):
                        errors.append(
                            f"{result_id}: applicability {applicability_ref} was confirmed after assessment"
                        )
                    context = assessment.get("assessment_context", {})
                    if context.get("configuration_ref") != result.get("configuration_ref"):
                        errors.append(
                            f"{result_id}: applicability {applicability_ref} configuration mismatch"
                        )
                    if context.get("market") not in scope_markets:
                        errors.append(
                            f"{result_id}: applicability {applicability_ref} market mismatch"
                        )
                for statement_ref in obligation.get("normative_statement_refs", []):
                    statement = statements.get(statement_ref, {})
                    for provision_ref in statement.get("provision_refs", []):
                        provision = provisions.get(provision_ref, {})
                        source = sources.get(provision.get("source_ref"), {})
                        if provision.get("verification_status") not in {
                            "provided_by_user",
                            "retrieved_from_official_source",
                        }:
                            errors.append(
                                f"{result_id}: definitive outcome depends on unverified Provision {provision_ref}"
                            )
                        provision_verified_at = parse_timestamp(provision.get("verified_at"))
                        if (
                            not is_confirmed_authorized(provision.get("verified_by_ref"))
                            or provision_verified_at is None
                        ):
                            errors.append(
                                f"{result_id}: definitive outcome depends on Provision without authorized verification {provision_ref}"
                            )
                        if assessed_at_time and provision_verified_at and provision_verified_at > assessed_at_time:
                            errors.append(
                                f"{result_id}: Provision {provision_ref} was verified after assessment"
                            )
                        locator = provision.get("locator", {})
                        if not locator.get("canonical"):
                            errors.append(
                                f"{result_id}: definitive outcome depends on Provision without a canonical locator {provision_ref}"
                            )
                        if assessed_as_of and provision.get("valid_from"):
                            try:
                                if date.fromisoformat(provision["valid_from"]) > assessed_as_of:
                                    errors.append(
                                        f"{result_id}: definitive outcome depends on not-yet-effective Provision {provision_ref}"
                                    )
                            except ValueError:
                                errors.append(f"{result_id}: invalid Provision valid_from date {provision_ref}")
                        if assessed_as_of and provision.get("valid_to"):
                            try:
                                if date.fromisoformat(provision["valid_to"]) < assessed_as_of:
                                    errors.append(
                                        f"{result_id}: definitive outcome depends on expired Provision {provision_ref}"
                                    )
                            except ValueError:
                                errors.append(f"{result_id}: invalid Provision valid_to date {provision_ref}")
                        if source.get("status") != "active":
                            errors.append(
                                f"{result_id}: definitive outcome depends on non-active Source {source.get('id')}"
                            )
                        if source.get("applicability_version_state") != "confirmed":
                            errors.append(
                                f"{result_id}: definitive outcome depends on unconfirmed Source version {source.get('id')}"
                            )
                        if source.get("verification_status") not in {
                            "provided_by_user",
                            "retrieved_from_official_source",
                        }:
                            errors.append(
                                f"{result_id}: definitive outcome depends on unverified Source {source.get('id')}"
                            )
                        source_verified_at = parse_timestamp(source.get("verified_at"))
                        if (
                            not is_confirmed_authorized(source.get("verified_by_ref"))
                            or source_verified_at is None
                        ):
                            errors.append(
                                f"{result_id}: definitive outcome depends on Source without authorized verification {source.get('id')}"
                            )
                        if assessed_at_time and source_verified_at and source_verified_at > assessed_at_time:
                            errors.append(
                                f"{result_id}: Source {source.get('id')} was verified after assessment"
                            )
                        if not source.get("identifier") or not (
                            source.get("edition") or source.get("effective_from")
                        ):
                            errors.append(
                                f"{result_id}: definitive outcome depends on Source without a confirmed version identity {source.get('id')}"
                            )
                        if assessed_as_of and source.get("effective_to"):
                            try:
                                if date.fromisoformat(source["effective_to"]) < assessed_as_of:
                                    errors.append(
                                        f"{result_id}: definitive outcome depends on expired Source {source.get('id')}"
                                    )
                            except ValueError:
                                errors.append(
                                    f"{result_id}: invalid Source effective_to date {source.get('id')}"
                                )
                        if assessed_as_of and source.get("effective_from"):
                            try:
                                if date.fromisoformat(source["effective_from"]) > assessed_as_of:
                                    errors.append(
                                        f"{result_id}: definitive outcome depends on not-yet-effective Source {source.get('id')}"
                                    )
                            except ValueError:
                                errors.append(
                                    f"{result_id}: invalid Source effective_from date {source.get('id')}"
                                )

    for attestation in compliance.get("attestations", []):
        attestation_id = attestation["id"]
        if attestation.get("configuration_ref") not in configurations:
            errors.append(f"{attestation_id}: unresolved configuration {attestation.get('configuration_ref')}")
        issuer_ref = attestation.get("issuer_ref")
        if issuer_ref is not None and issuer_ref not in parties:
            errors.append(f"{attestation_id}: unresolved issuer {issuer_ref}")
        if attestation.get("scheme_ref") not in schemes:
            errors.append(f"{attestation_id}: unresolved ConformityScheme {attestation.get('scheme_ref')}")
        attestation_results = []
        for result_ref in attestation.get("assessment_result_refs", []):
            result = results.get(result_ref)
            if result is None:
                errors.append(f"{attestation_id}: unresolved AssessmentResult {result_ref}")
            else:
                attestation_results.append(result)
        if attestation.get("status") == "issued":
            if not attestation_results or any(
                result.get("outcome") != "conforming" or result.get("validity_state") != "active"
                for result in attestation_results
            ):
                errors.append(f"{attestation_id}: issued Attestation requires active conforming results")
            if any(
                result.get("configuration_ref") != attestation.get("configuration_ref")
                for result in attestation_results
            ):
                errors.append(f"{attestation_id}: AssessmentResult configuration mismatch")
            scheme = schemes.get(attestation.get("scheme_ref"), {})
            if (
                not scheme.get("obligation_refs")
                or not scheme.get("required_evidence_requirement_refs")
                or not scheme.get("assessment_methods")
            ):
                errors.append(f"{attestation_id}: ConformityScheme has an empty issuance scope")
            if (
                scheme.get("origin") != "user_confirmed"
                or scheme.get("human_confirmation_required") is not False
                or not is_confirmed_authorized(scheme.get("confirmed_by_ref"))
                or parse_timestamp(scheme.get("confirmed_at")) is None
            ):
                errors.append(f"{attestation_id}: ConformityScheme is not authorized and confirmed")
            if attestation.get("output_kind") != scheme.get("output_kind"):
                errors.append(f"{attestation_id}: output kind does not match ConformityScheme")
            if scheme.get("output_kind") == "none":
                errors.append(f"{attestation_id}: ConformityScheme does not permit an issued output")
            if issuer_ref != scheme.get("decision_authority_ref"):
                errors.append(f"{attestation_id}: issuer is not the ConformityScheme decision authority")
            if attestation.get("object_ref") != scheme.get("object_of_conformity", {}).get(
                "target_ref"
            ):
                errors.append(f"{attestation_id}: attestation object does not match ConformityScheme object")
            issuer = parties.get(issuer_ref, {})
            if (
                issuer.get("status") != "confirmed"
                or issuer.get("verification_status") != "provided_by_user"
                or not issuer.get("authority_scope")
            ):
                errors.append(f"{attestation_id}: issued Attestation requires a confirmed authorized issuer")
            if attestation.get("object_ref") not in objects:
                errors.append(f"{attestation_id}: unresolved attestation object {attestation.get('object_ref')}")
            assessed_obligations = {
                obligation_ref
                for result in attestation_results
                for obligation_ref in result.get("assessed_obligation_refs", [])
            }
            if not set(scheme.get("obligation_refs", [])).issubset(assessed_obligations):
                errors.append(f"{attestation_id}: ConformityScheme obligations are not fully assessed")
            required_evidence = set(scheme.get("required_evidence_requirement_refs", []))
            provided_evidence = {
                requirement_ref
                for result in attestation_results
                for evidence_ref in result.get("evidence_item_refs", [])
                for requirement_ref in evidence_items.get(evidence_ref, {}).get(
                    "evidence_requirement_refs", []
                )
            }
            if not required_evidence.issubset(provided_evidence):
                errors.append(f"{attestation_id}: ConformityScheme EvidenceRequirements are incomplete")
            for requirement_ref in required_evidence:
                requirement = evidence_requirements.get(requirement_ref, {})
                if (
                    requirement.get("status") != "confirmed"
                    or requirement.get("origin") != "user_confirmed"
                    or requirement.get("human_confirmation_required") is not False
                    or not is_confirmed_authorized(requirement.get("confirmed_by_ref"))
                    or parse_timestamp(requirement.get("confirmed_at")) is None
                ):
                    errors.append(
                        f"{attestation_id}: Scheme EvidenceRequirement {requirement_ref} is not authorized and confirmed"
                    )
            issued_at_time = parse_timestamp(attestation.get("issued_at"))
            valid_from_time = parse_timestamp(attestation.get("valid_from"))
            valid_to_time = parse_timestamp(attestation.get("valid_to"))
            if attestation.get("issued_at") and issued_at_time is None:
                errors.append(f"{attestation_id}: invalid Attestation issued_at timestamp")
            if attestation.get("valid_from") and valid_from_time is None:
                errors.append(f"{attestation_id}: invalid Attestation valid_from timestamp")
            if attestation.get("valid_to") and valid_to_time is None:
                errors.append(f"{attestation_id}: invalid Attestation valid_to timestamp")
            scheme_confirmed_at = parse_timestamp(scheme.get("confirmed_at"))
            if issued_at_time and scheme_confirmed_at and scheme_confirmed_at > issued_at_time:
                errors.append(f"{attestation_id}: ConformityScheme was confirmed after issuance")
            required_scheme_independence = scheme.get("independence")
            if required_scheme_independence not in {None, "unknown", "mixed"}:
                for result in attestation_results:
                    result_activity = activities.get(result.get("assessment_activity_ref"), {})
                    if result_activity.get("independence") != required_scheme_independence:
                        errors.append(
                            f"{attestation_id}: AssessmentActivity independence does not satisfy ConformityScheme"
                        )
            if not is_confirmed_authorized(attestation.get("verified_by_ref")):
                errors.append(f"{attestation_id}: Attestation artifact verifier is not authorized")
            attestation_verified_at = parse_timestamp(attestation.get("verified_at"))
            if issued_at_time and attestation_verified_at and attestation_verified_at < issued_at_time:
                errors.append(f"{attestation_id}: Attestation artifact was verified before issuance")
            if assessed_as_of and attestation_verified_at and attestation_verified_at.date() > assessed_as_of:
                errors.append(f"{attestation_id}: Attestation artifact was verified after model assessment date")
            verify_local_artifact(
                attestation_id,
                attestation.get("artifact_locator"),
                attestation.get("integrity_hash"),
            )
            if issued_at_time and valid_to_time and issued_at_time > valid_to_time:
                errors.append(f"{attestation_id}: issued_at is after valid_to")
            if valid_from_time and valid_to_time and valid_from_time > valid_to_time:
                errors.append(f"{attestation_id}: valid_from is after valid_to")
            for result in attestation_results:
                result_time = parse_timestamp(result.get("assessed_at"))
                if issued_at_time and result_time and result_time > issued_at_time:
                    errors.append(
                        f"{attestation_id}: AssessmentResult {result['id']} was assessed after issuance"
                    )
            if assessed_as_of and valid_from_time and valid_from_time.date() > assessed_as_of:
                errors.append(f"{attestation_id}: active issued Attestation is not yet valid")
            if assessed_as_of and issued_at_time and issued_at_time.date() > assessed_as_of:
                errors.append(f"{attestation_id}: issued_at is after the model assessment date")
            if assessed_as_of and valid_to_time and valid_to_time.date() < assessed_as_of:
                errors.append(f"{attestation_id}: issued Attestation is expired as of assessment date")
        elif attestation.get("status") in {"suspended", "withdrawn", "expired"}:
            if attestation.get("validity_state") == "active" or not attestation.get(
                "invalidation_reason"
            ):
                errors.append(
                    f"{attestation_id}: inactive Attestation status requires non-active validity and reason"
                )

    outcome_set = {result.get("outcome") for result in results.values()}
    expected_assurance = "not_performed"
    if outcome_set and outcome_set != {"not_performed"}:
        expected_assurance = next(iter(outcome_set)) if len(outcome_set) == 1 else "mixed"
    actual_assurance = compliance.get("summary", {}).get("assurance_outcome")
    if actual_assurance != expected_assurance:
        errors.append(
            f"ComplianceSummary: assurance_outcome {actual_assurance} != derived {expected_assurance}"
        )
    if actual_assurance == "conforming":
        unresolved_applicability = sorted(
            applicability_ref
            for obligation in obligations.values()
            for applicability_ref in obligation.get("applicability_refs", [])
            if applicability.get(applicability_ref, {}).get("decision") == "uncertain"
            or applicability.get(applicability_ref, {}).get("human_confirmation_state")
            != "confirmed"
            or not is_confirmed_authorized(
                applicability.get(applicability_ref, {}).get("confirmed_by_ref")
            )
            or parse_timestamp(applicability.get(applicability_ref, {}).get("confirmed_at"))
            is None
        )
        if unresolved_applicability:
            errors.append(
                "ComplianceSummary: conforming assurance has unresolved applicability "
                + ", ".join(unresolved_applicability)
            )
        scope_applicable_obligations = {
            obligation_id
            for obligation_id, obligation in obligations.items()
            if any(
                applicability.get(applicability_ref, {}).get("decision")
                in {"applicable", "partially_applicable"}
                and applicability.get(applicability_ref, {}).get("human_confirmation_state")
                == "confirmed"
                for applicability_ref in obligation.get("applicability_refs", [])
            )
        }
        active_conforming_obligations = {
            obligation_ref
            for result in results.values()
            if result.get("outcome") == "conforming"
            and result.get("validity_state") == "active"
            for obligation_ref in result.get("assessed_obligation_refs", [])
        }
        missing_scope = sorted(scope_applicable_obligations - active_conforming_obligations)
        if missing_scope:
            errors.append(
                "ComplianceSummary: conforming assurance does not cover applicable obligations "
                + ", ".join(missing_scope)
            )

    for row in derive_trace_rows(model):
        for field in ("source_id", "target_id"):
            ref = row[field]
            if ref not in objects:
                errors.append(f"{row['relation_id']}: unresolved {field} {ref}")

    return sorted(set(errors))


def write_trace_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "relation_id",
        "relation_type",
        "source_id",
        "target_id",
        "rationale",
        "origin",
        "confidence",
        "validity_state",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=Path)
    parser.add_argument("--base-schema", type=Path, default=DEFAULT_BASE_SCHEMA)
    parser.add_argument("--extension-schema", type=Path, default=DEFAULT_EXTENSION_SCHEMA)
    parser.add_argument("--trace-csv", type=Path)
    args = parser.parse_args()

    try:
        model = load_json(args.model)
        base_schema = load_json(args.base_schema)
        extension_schema = load_json(args.extension_schema)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    registry = Registry().with_resource(base_schema["$id"], Resource.from_contents(base_schema))
    validator = Draft202012Validator(
        extension_schema,
        registry=registry,
        format_checker=FormatChecker(),
    )
    schema_errors = sorted(validator.iter_errors(model), key=lambda item: list(item.absolute_path))
    errors = [
        f"schema {'/'.join(map(str, error.absolute_path))}: {error.message}" for error in schema_errors
    ]
    if not schema_errors:
        errors.extend(semantic_errors(model, args.model.resolve().parent))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL {args.model} errors={len(errors)}", file=sys.stderr)
        return 1

    rows = derive_trace_rows(model)
    if args.trace_csv:
        write_trace_csv(args.trace_csv, rows)
    print(
        f"PASS {args.model} ids={len(collect_ids(model)[0])} "
        f"derived_relations={len(rows)} trace_csv={args.trace_csv or 'not_written'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
