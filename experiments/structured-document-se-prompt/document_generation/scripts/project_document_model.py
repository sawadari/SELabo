"""Project a SELabo semantic model into a non-authoritative document model.

The source model remains the only semantic source of truth. This script only
creates document-oriented registries, references, and traceable values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def source_ids(model: Any) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            item_id = value.get("id")
            if isinstance(item_id, str):
                found[item_id] = value
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(model)
    return found


def first_source_refs(model: dict[str, Any]) -> list[str]:
    refs = [item_id for item_id in source_ids(model) if item_id.startswith("SRC-")]
    return refs[:1]


def value_missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def presence_state(value: Any, source: dict[str, Any] | None = None) -> str:
    if value_missing(value):
        return "not_determined"
    if not source:
        return "candidate"
    if (
        source.get("claim_state") in {"inferred", "assumed"}
        or source.get("decision_state") not in {None, "user_confirmed"}
        or source.get("baseline_state") not in {None, "baselined"}
    ):
        return "candidate"
    return "known"


def provenance(source: dict[str, Any] | None, *, derived: bool = False) -> dict[str, Any]:
    source = source or {}
    return {
        "origin": source.get("origin", "ai_context_inference" if derived else "manual"),
        "claim_state": source.get("claim_state", "inferred" if derived else "stated"),
        "decision_state": source.get("decision_state", "proposed"),
        "validity_state": source.get("validity_state", "active"),
        "baseline_state": source.get("baseline_state", "outside_baseline"),
        "confidence": source.get("confidence", "low" if derived else "medium"),
    }


def traceable(
    value: Any,
    source: dict[str, Any] | None = None,
    *,
    source_refs: Iterable[str] = (),
    derivation: str = "direct",
    rationale: str | None = None,
) -> dict[str, Any]:
    source = source or {}
    refs = list(source_refs)
    if isinstance(source.get("id"), str):
        refs.append(source["id"])
    refs.extend(item for item in source.get("evidence_refs", []) if isinstance(item, str))
    refs = unique(refs)
    if not refs:
        refs = ["SRC-0001"]
    details = provenance(source, derived=derivation != "direct" or not source)
    state = presence_state(value, source)
    if rationale is None:
        rationale = "10_se_model.jsonの値を文書投影へ保持した"
    if derivation != "direct":
        rationale = f"10_se_model.jsonの要素から{derivation}として生成した"
    return {
        "value": value,
        "state": state,
        "source_refs": refs,
        "derivation": derivation,
        **details,
        "human_confirmation_required": state != "known" or details["claim_state"] != "stated",
        "rationale": rationale,
    }


def traceable_array(
    values: Iterable[Any],
    source: dict[str, Any] | None = None,
    *,
    source_refs: Iterable[str] = (),
    derivation: str = "direct",
) -> list[dict[str, Any]]:
    return [
        traceable(
            value,
            source,
            source_refs=source_refs,
            derivation=derivation,
        )
        for value in values
    ]


def ref_values(item: dict[str, Any] | None) -> list[str]:
    if not isinstance(item, dict):
        return []
    refs: list[str] = []
    for key, value in item.items():
        if key.endswith("_refs") and isinstance(value, list):
            refs.extend(ref for ref in value if isinstance(ref, str))
    return unique(refs)


def source_elements(model: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = model.get(key, [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def project_scope(scope: dict[str, Any], *, source_refs: Iterable[str]) -> dict[str, Any]:
    return {
        "included": traceable_array(
            scope.get("included", []), scope, source_refs=source_refs, derivation="direct"
        ),
        "excluded": traceable_array(
            scope.get("excluded", []), scope, source_refs=source_refs, derivation="direct"
        ),
        "lifecycle": traceable_array(
            scope.get("lifecycle_scope", []), scope, source_refs=source_refs, derivation="direct"
        ),
        "external_systems": scope.get("external_systems", []),
        "operational_environment": traceable_array(
            scope.get("operational_environment", []),
            scope,
            source_refs=source_refs,
            derivation="direct",
        ),
    }


def project_schedule(schedule: dict[str, Any] | None, *, source_refs: Iterable[str]) -> dict[str, Any]:
    schedule = schedule or {}
    raw_milestones = schedule.get("milestones", [])
    milestones: list[dict[str, Any]] = []
    for index, milestone in enumerate(raw_milestones, start=1):
        if not isinstance(milestone, dict):
            continue
        milestone_refs = unique([*source_refs, *ref_values(milestone)])
        milestones.append(
            {
                "id": milestone.get("id", f"MILESTONE-{index:04d}"),
                "name": milestone.get("name", f"未確定マイルストーン {index}"),
                "planned_date": milestone.get("planned_date"),
                "status": presence_state(milestone.get("status"), milestone),
                "source_refs": milestone_refs,
                "human_confirmation_required": True,
                "rationale": "正本に記載された計画候補を保持する。日付・状態は未確定なら補完しない。",
            }
        )
    raw_state = schedule.get("value_state", schedule.get("state"))
    state = "not_determined" if raw_state in {None, "tbd", "not_determined"} else presence_state(raw_state, schedule)
    return {"state": state, "milestones": milestones}


def project_budget(budget: dict[str, Any] | None, *, source_refs: Iterable[str]) -> dict[str, Any]:
    budget = budget or {}
    raw_state = budget.get("value_state", budget.get("state"))
    state = "not_determined" if raw_state in {None, "tbd", "not_determined"} else presence_state(raw_state, budget)
    basis = budget.get("estimation_basis")
    basis_values = []
    if basis:
        basis_values.append(
            traceable(
                basis,
                budget,
                source_refs=source_refs,
                derivation="direct",
            )
        )
    return {
        "state": state,
        "currency": budget.get("currency", "未指定"),
        "capex": budget.get("base"),
        "opex": None,
        "contingency": None,
        "estimation_basis": basis_values,
        "source_refs": list(source_refs),
        "human_confirmation_required": True,
        "rationale": "費用が未指定の場合はnot_determinedとし、金額を推測しない。",
    }


def project_data_model(model: dict[str, Any], *, source_refs: Iterable[str]) -> dict[str, Any] | None:
    data_models = source_elements(model, "data_models")
    if not data_models:
        return None
    entities: list[dict[str, Any]] = []
    for data_model in data_models:
        data_id = data_model.get("id", "DATA-UNKNOWN")
        for index, entity in enumerate(data_model.get("entity_candidates", []), start=1):
            if not isinstance(entity, dict):
                continue
            attributes = []
            for attribute in entity.get("attributes", []):
                if not isinstance(attribute, dict):
                    continue
                attributes.append(
                    {
                        "name": attribute.get("name", "未指定属性"),
                        "value_type": attribute.get("value_type", "not_determined"),
                        "required_state": presence_state(attribute.get("required_state"), attribute),
                    }
                )
            entities.append(
                {
                    "id": f"{data_id}-ENTITY-{index:04d}",
                    "name": entity.get("name", f"未指定エンティティ {index}"),
                    "description": entity.get("description"),
                    "owner_ref": entity.get("owner_ref"),
                    "source_refs": unique([*source_refs, data_id]),
                    "attributes": attributes,
                    "lifecycle": "candidate",
                    "classification": data_model.get("model_kind", "not_determined"),
                }
            )
    return {
        "model_refs": [item.get("id") for item in data_models if item.get("id")],
        "entities": entities,
        "quality_requirements": [
            {
                "quality_type": "data_quality_profile",
                "state": "not_determined",
                "target": None,
                "unit": None,
                "source_refs": unique([*source_refs, *[item.get("id", "") for item in data_models]]),
                "human_confirmation_required": True,
                "rationale": "正本にデータ品質基準がないため、品質目標を推測しない。",
            }
        ],
    }


def project_document_requirement(requirement: dict[str, Any], index: int) -> dict[str, Any]:
    source_id = requirement["id"]
    statement = requirement.get("statement")
    if not isinstance(statement, str) or not statement:
        raise ValueError(f"{source_id} has no source statement")
    category = requirement.get("requirement_category", "not_classified")
    source_refs = unique([source_id, *requirement.get("evidence_refs", [])])
    rendered = traceable(
        statement,
        requirement,
        source_refs=source_refs,
        derivation="direct",
        rationale="要求本文は10_se_model.jsonのsource statementを変更せずに投影した",
    )
    result: dict[str, Any] = {
        "id": f"DOCREQ-{index:04d}",
        "source_requirement_ref": source_id,
        "classification": {
            "primary": category,
            "secondary": unique(
                [
                    value
                    for value in [
                        "screen" if requirement.get("screen_refs") else None,
                        "api" if requirement.get("api_contract_refs") else None,
                        "data" if requirement.get("data_model_refs") else None,
                    ]
                    if value
                ]
            ),
            "classification_basis": "10_se_model.json.requirement_category",
            "confidence": requirement.get("confidence", "low"),
        },
        "title": requirement.get("name", source_id),
        "statement_policy": "resolve_from_source",
        "rendered_statement": rendered,
        "normative_level": requirement.get("normative_level", "descriptive"),
        "source_need_refs": requirement.get("source_need_refs", []),
        "verification_refs": requirement.get("verification_case_refs", []),
        "validity_state": requirement.get("validity_state", "active"),
        "baseline_state": requirement.get("baseline_state", "outside_baseline"),
        "render_location": "body" if requirement.get("validity_state", "active") == "active" else "appendix_history",
        "candidate_marker": "候補" if rendered["state"] != "known" else None,
    }
    acceptance = requirement.get("acceptance_criteria_candidate")
    if acceptance:
        result["acceptance_criteria"] = traceable(
            acceptance,
            requirement,
            source_refs=unique([*source_refs, *requirement.get("acceptance_criteria_refs", [])]),
            derivation="direct",
            rationale="正本にある受入条件候補を変更せずに投影した",
        )
    return result


def category_refs(requirements: list[dict[str, Any]], category: str) -> list[str]:
    return [
        item["id"]
        for item in requirements
        if item["classification"]["primary"] == category
    ]


def project(model: dict[str, Any], source_path: Path) -> dict[str, Any]:
    meta = model.get("meta", {})
    scope = model.get("scope", {})
    planning_source = model.get("planning", {})
    source_refs = first_source_refs(model)
    target_system = meta.get("target_system", scope.get("target_system", "未指定システム"))
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()

    business = planning_source.get("business_context", {})
    background = business.get("background") or "未指定"
    problem = scope.get("problem_or_opportunity") or business.get("problem_or_opportunity") or "未指定"
    purpose = scope.get("purpose") or "未指定"
    value_proposition = business.get("value_proposition") or purpose
    objectives_source = source_elements(planning_source, "objectives")
    requirements_source = source_elements(model, "requirements")
    document_requirements = [
        project_document_requirement(requirement, index)
        for index, requirement in enumerate(requirements_source, start=1)
    ]
    stakeholders = source_elements(model, "stakeholders")
    needs = source_elements(model, "needs")
    use_cases = source_elements(model, "use_cases")
    scenarios = source_elements(model, "scenarios")
    verification_cases = source_elements(model, "verification_cases")
    validation_cases = source_elements(model, "validation_cases")
    acceptance = source_elements(model, "acceptance_criteria")
    api_contracts = source_elements(model, "api_contracts")
    interfaces = source_elements(model, "interfaces")
    data_models = source_elements(model, "data_models")
    glossary_source = model.get("glossary", [])
    glossary_entries = [
        {
            "id": f"TERM-{index:04d}",
            "term": item.get("term", "未指定") if isinstance(item, dict) else str(item),
            "definition": item.get("definition") if isinstance(item, dict) else None,
            "source_refs": unique([*source_refs]),
        }
        for index, item in enumerate(glossary_source, start=1)
    ]
    all_requirement_refs = [item["id"] for item in document_requirements]
    kpi_refs = unique(
        [
            *scope.get("success_measure_refs", []),
            *[ref for item in objectives_source for ref in item.get("kpi_refs", [])],
        ]
    )
    risk_refs = [item.get("id") for item in source_elements(model, "risks") if item.get("id")]
    assumption_refs = [item.get("id") for item in source_elements(model, "assumptions") if item.get("id")]
    open_issue_refs = unique([*risk_refs, *assumption_refs, *[item.get("id") for item in source_elements(model, "findings") if item.get("id")]])
    planning_scope = project_scope(scope, source_refs=source_refs)
    planning = {
        "title": traceable(
            f"{target_system} 企画書",
            None,
            source_refs=source_refs,
            derivation="summary",
            rationale="正本のtarget_systemから文書タイトルを生成した",
        ),
        "executive_summary": traceable(
            f"{background} {problem} {value_proposition}",
            None,
            source_refs=source_refs,
            derivation="summary",
            rationale="正本の背景・問題・価値提案を要約して投影した",
        ),
        "background": traceable_array([background], None, source_refs=source_refs, derivation="direct"),
        "problem_opportunity": traceable_array([problem], None, source_refs=source_refs, derivation="direct"),
        "purpose": traceable_array([purpose], None, source_refs=source_refs, derivation="direct"),
        "objectives": [
            {
                **traceable(
                    item.get("statement", item.get("name", "未指定")),
                    item,
                    derivation="direct",
                ),
                "id": item.get("id", f"OBJ-{index:04d}"),
                "kpi_refs": item.get("kpi_refs", []),
            }
            for index, item in enumerate(objectives_source, start=1)
        ],
        "scope": planning_scope,
        "stakeholder_refs": unique(
            [*planning_source.get("target_user_refs", []), *[item.get("id", "") for item in stakeholders]]
        ),
        "kpi_refs": kpi_refs,
        "risk_refs": risk_refs,
        "assumption_refs": assumption_refs,
        "open_issues": open_issue_refs,
        "alternatives": [
            {"id": item.get("id"), "source_ref": item.get("id"), "derivation": "direct"}
            for item in source_elements(model, "alternatives")
            if item.get("id")
        ],
        "schedule": project_schedule(planning_source.get("schedule"), source_refs=source_refs),
        "budget": project_budget(planning_source.get("cost_estimate"), source_refs=source_refs),
        "governance": planning_source.get("governance"),
        "dependencies": [],
        "constraints": [],
        "approval_criteria": [],
    }

    category_map = {
        "business": "business",
        "functional": "functional",
        "nonfunctional": "non_functional",
        "security": "security",
        "data": "data",
        "interface": "interface",
        "operational": "operational",
        "migration": "migration",
        "support": "support",
        "regulatory": "regulatory",
        "constraint": "constraint",
        "other": "other",
    }
    categories = {
        key: category_refs(document_requirements, value)
        for key, value in category_map.items()
    }
    requirements_definition = {
        "purpose": traceable(purpose, None, source_refs=source_refs, derivation="direct"),
        "system_context": {
            "target_system": target_system,
            "external_systems": scope.get("external_systems", []),
            "operational_environment": traceable_array(
                scope.get("operational_environment", []),
                None,
                source_refs=source_refs,
                derivation="direct",
            ),
        },
        "scope": planning_scope,
        "stakeholder_refs": [item.get("id") for item in stakeholders if item.get("id")],
        "need_refs": [item.get("id") for item in needs if item.get("id")],
        "use_case_refs": [item.get("id") for item in use_cases if item.get("id")],
        "scenario_refs": [item.get("id") for item in scenarios if item.get("id")],
        "requirements": document_requirements,
        "views": {
            "functional_refs": categories["functional"],
            "nonfunctional_refs": categories["nonfunctional"],
            "business_refs": categories["business"],
            "security_refs": categories["security"],
            "data_refs": categories["data"],
            "interface_refs": categories["interface"],
            "operational_refs": categories["operational"],
            "support_refs": categories["support"],
            "migration_refs": categories["migration"],
            "regulatory_refs": categories["regulatory"],
            "constraint_refs": categories["constraint"],
            "test_requirement_refs": [
                item["id"]
                for item in document_requirements
                if item["verification_refs"] or item.get("acceptance_criteria")
            ],
            "other_refs": categories["other"],
            "unclassified_refs": category_refs(document_requirements, "not_classified"),
        },
        "data_model": project_data_model(model, source_refs=source_refs),
        "glossary": [item["id"] for item in glossary_entries],
        "glossary_entries": glossary_entries,
        "interfaces": {
            "interface_refs": [
                item.get("id") for item in [*api_contracts, *interfaces] if item.get("id")
            ],
            "external_contracts": [
                {"id": item.get("id"), "spec_ref": item.get("spec_ref")}
                for item in api_contracts
                if item.get("id")
            ],
        },
        "operations": {"source_refs": ref_values(model.get("operations_maintenance"))},
        "maintenance": {"source_refs": ref_values(model.get("operations_maintenance"))},
        "migration": {"source_refs": model.get("operations_maintenance", {}).get("migration_requirement_refs", [])},
        "security_privacy": {"source_refs": ref_values(model.get("security"))},
        "verification": {"verification_case_refs": [item.get("id") for item in verification_cases if item.get("id")]},
        "validation": {"validation_case_refs": [item.get("id") for item in validation_cases if item.get("id")]},
        "acceptance": {"acceptance_criteria_refs": [item.get("id") for item in acceptance if item.get("id")]},
        "open_issues": open_issue_refs,
    }

    relations = []
    for relation in model.get("relations", []):
        if not isinstance(relation, dict):
            continue
        relations.append(
            {
                "relation_id": relation.get("id"),
                "relation_type": relation.get("relation_type"),
                "source_id": relation.get("source_id"),
                "target_id": relation.get("target_id"),
                "source_of_truth": "10_se_model.json",
            }
        )

    has_candidates = any(
        isinstance(value, dict) and value.get("claim_state") in {"inferred", "assumed"}
        for value in source_ids(model).values()
    )
    return {
        "meta": {
            "artifact_type": "document_projection_model",
            "schema_version": "1.0.0",
            "project_id": None,
            "target_system": target_system,
            "language": meta.get("language", "ja-JP"),
            "document_status": "candidate",
            "generated_at": None,
            "writing_profile_ref": "../hierarchical-se-prompt/11_JAPANESE_WRITING_PROFILE.json",
        },
        "source_binding": {
            "source_of_truth": "10_se_model.json",
            "schema_version": meta.get("schema_version", "unknown"),
            "content_hash": f"sha256:{source_hash}",
            "projection_policy": "source_resolved_with_summary",
            "allowed_validity_states": ["active", "stale", "superseded"],
            "candidate_policy": "include_marked",
        },
        "document_kinds": ["planning", "requirements_definition"],
        "planning": planning,
        "requirements_definition": requirements_definition,
        "traceability": {
            "relation_source": "se_model.relations",
            "relations": relations,
            "coverage": {
                "source_requirement_count": len(requirements_source),
                "document_requirement_count": len(document_requirements),
                "source_requirement_registry_is_single": True,
            },
        },
        "quality": {
            "schema_validation": "not_performed",
            "reference_integrity": "not_performed",
            "projection_consistency": "pass_with_provisional_assumption" if has_candidates else "pass",
            "japanese_writing_validation": "not_performed",
            "unresolved_findings": [item.get("id") for item in source_elements(model, "findings") if item.get("id")],
            "not_performed": [
                "document projection schema validation",
                "reference integrity validation",
                "Japanese technical writing validation",
                "Markdown/HTML/DOCX/PDF rendering",
                "OpenAPI/AsyncAPI external contract lint",
                "human review and approval",
            ],
        },
        "rendering": {
            "planning_profile": "document_generation/profiles/planning_standard_ja_v1.yaml",
            "requirements_profile": "document_generation/profiles/requirements_standard_ja_v1.yaml",
            "formats": ["markdown", "html", "docx", "pdf"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        model = load_json(args.source)
        projected = project(model, args.source)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(projected, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS")
    print(f"- source: {args.source}")
    print(f"- output: {args.output}")
    print("- source of truth: 10_se_model.json")
    print("- document kinds: planning, requirements_definition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
