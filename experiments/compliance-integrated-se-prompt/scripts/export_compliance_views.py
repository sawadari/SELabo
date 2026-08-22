#!/usr/bin/env python3
"""Export deterministic Compliance Layer review views from the canonical JSON model."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cell(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "<br>".join(cell(item) for item in value) or "—"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(cell(value) for value in row) + " |" for row in rows)
    if not rows:
        lines.append("| " + " | ".join("—" for _ in headers) + " |")
    return "\n".join(lines)


def source_register(model: dict[str, Any]) -> str:
    compliance = model["compliance"]
    scope = compliance["scope"]
    sources = compliance["sources"]
    provisions = compliance["provisions"]
    lines = [
        "# Compliance Source Register",
        "",
        "## 対象範囲",
        "",
        table(
            ["法域", "市場", "製品分類", "構成", "評価時点"],
            [[scope["jurisdictions"], scope["markets"], scope["product_classifications"], scope["configuration_refs"], scope["assessed_as_of"]]],
        ),
        "",
        "## Authority",
        "",
        table(
            ["ID", "名称", "種別", "法域", "検証状態", "公式参照先"],
            [[item["id"], item["name"], item["authority_type"], item["jurisdictions"], item["verification_status"], item.get("official_locator")] for item in compliance["authorities"]],
        ),
        "",
        "## Source",
        "",
        table(
            ["ID", "種別", "名称", "識別子／版", "発行日", "発効日", "失効日", "公開状態", "適用版確認", "原典取得状況", "確認者／日時", "保存方針", "公式参照先"],
            [[item["id"], item["source_type"], item["title"], [item.get("identifier"), item.get("edition")], item.get("publication_date"), item.get("effective_from"), item.get("effective_to"), item["status"], item["applicability_version_state"], item["verification_status"], [item.get("verified_by_ref"), item.get("verified_at")], item["text_storage_policy"], item.get("official_locator")] for item in sources],
        ),
        "",
        "## Provision",
        "",
        table(
            ["ID", "Source", "位置", "見出し", "検証状態", "確認者／日時"],
            [[item["id"], item["source_ref"], item["locator"].get("canonical"), item.get("heading"), item["verification_status"], [item.get("verified_by_ref"), item.get("verified_at")]] for item in provisions],
        ),
        "",
        "## 未確認事項",
        "",
        *[f"- {value}" for value in compliance["summary"]["source_limitations"]],
        "",
        "> このregisterは候補モデルの投影であり、外部原典そのものではありません。",
        "",
    ]
    return "\n".join(lines)


def applicability_register(model: dict[str, Any]) -> str:
    compliance = model["compliance"]
    lines = [
        "# Applicability and Obligation Register",
        "",
        "## Normative Statement",
        "",
        table(
            ["ID", "Provision", "種別", "様相", "主体", "条件", "行為／性質", "対象", "限界", "解釈状態"],
            [[item["id"], item["provision_refs"], item["statement_kind"], item["modality"], item.get("bearer"), item.get("condition"), item.get("action_or_property"), item.get("object"), item.get("limit"), item["interpretation_status"]] for item in compliance["normative_statements"]],
        ),
        "",
        "## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）",
        "",
        table(
            ["ID", "Normative Statement", "コンテキスト", "判断候補", "拘束根拠", "理由", "人確認状態", "確認者", "確認日時", "再評価トリガー"],
            [[item["id"], item["normative_statement_refs"], item["assessment_context"], item["decision"], item["binding_basis"], item["basis"], item["human_confirmation_state"], item.get("confirmed_by_ref"), item.get("confirmed_at"), item["review_triggers"]] for item in compliance["applicability_assessments"]],
        ),
        "",
        "## Obligation",
        "",
        table(
            ["ID", "種別", "義務主体候補", "対象", "条件", "必要結果", "状態"],
            [[item["id"], item["obligation_kind"], item["obligated_party"], item["object_of_conformity"], item["condition"], item["required_outcome"], item["compliance_status"]] for item in compliance["obligations"]],
        ),
        "",
        "## 人の確認バックログ",
        "",
        *[f"- {item['id']}: {item['basis']}" for item in compliance["applicability_assessments"] if item["human_confirmation_required"]],
        "",
    ]
    return "\n".join(lines)


def projection_csv(model: dict[str, Any]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=["projection_id", "obligation_id", "projection_kind", "target_level", "target_id", "derivation_basis", "status", "confidence", "human_confirmation_required"],
        lineterminator="\n",
    )
    writer.writeheader()
    for projection in sorted(model["compliance"]["engineering_projections"], key=lambda item: item["id"]):
        for obligation_id in sorted(projection["obligation_refs"]):
            for target_id in sorted(projection["target_refs"]):
                writer.writerow(
                    {
                        "projection_id": projection["id"],
                        "obligation_id": obligation_id,
                        "projection_kind": projection["projection_kind"],
                        "target_level": projection["target_level"],
                        "target_id": target_id,
                        "derivation_basis": projection["derivation_basis"],
                        "status": projection["status"],
                        "confidence": projection["confidence"],
                        "human_confirmation_required": str(projection["human_confirmation_required"]).lower(),
                    }
                )
    return output.getvalue().encode("utf-8-sig")


def evidence_plan(model: dict[str, Any]) -> str:
    compliance = model["compliance"]
    summary = compliance["summary"]
    lines = [
        "# Conformity and Evidence Plan",
        "",
        "## Gate境界",
        "",
        table(
            ["モデル品質", "Assurance outcome", "Compliance approvalではない", "Reviewer Gate"],
            [[summary["model_quality_result"], summary["assurance_outcome"], summary["not_a_compliance_approval"], [f"{key}={value}" for key, value in summary["reviewer_gates"].items()]]],
        ),
        "",
        "## 適合性評価スキーム候補",
        "",
        table(
            ["ID", "種別", "所有者", "決定権者", "適合対象", "Obligation", "必要Evidence", "独立性", "出力"],
            [[item["id"], item["scheme_type"], item["scheme_owner_ref"], item["decision_authority_ref"], item["object_of_conformity"].get("target_ref"), item["obligation_refs"], item["required_evidence_requirement_refs"], item["independence"], item["output_kind"]] for item in compliance["conformity_schemes"]],
        ),
        "",
        "## 必要な証拠（Evidence Requirement）",
        "",
        table(
            ["ID", "対象", "種別", "必要属性", "構成必須", "独立性", "状態"],
            [[item["id"], item["target_refs"], item["evidence_type"], item["required_properties"], item["configuration_required"], item["independence_required"], item["status"]] for item in compliance["evidence_requirements"]],
        ),
        "",
        "## 存在を確認した証拠（Evidence Item）",
        "",
        table(
            ["ID", "EVR", "構成", "版", "検証状態", "有効性"],
            [[item["id"], item["evidence_requirement_refs"], item["configuration_ref"], item["version"], item["verification_status"], item["validity_state"]] for item in compliance["evidence_items"]],
        ),
        "",
        "## 評価活動候補 / Assessment Result / Findingと是正",
        "",
        table(
            ["Activity", "構成", "状態", "Result", "Outcome", "Finding", "有効性", "人確認"],
            [[activity["id"], activity["configuration_refs"], activity["status"], result["id"], result["outcome"], result["finding_refs"], result["validity_state"], result["human_confirmation_state"]] for activity in compliance["assessment_activities"] for result in compliance["assessment_results"] if result["assessment_activity_ref"] == activity["id"]],
        ),
        "",
        "## Attestation",
        "",
        table(
            ["ID", "Scheme", "Result", "構成", "状態", "有効性", "人確認"],
            [[item["id"], item["scheme_ref"], item["assessment_result_refs"], item["configuration_ref"], item["status"], item["validity_state"], item["human_confirmation_state"]] for item in compliance["attestations"]],
        ),
        "",
        "## 未実施事項",
        "",
        *[f"- {item['id']}: status={item['status']}" for item in compliance["assessment_activities"] if item["status"] != "completed"],
        "",
        "> Evidence Itemが0件またはAssessment Resultがnot_performedの場合、適合・認証・市場投入承認を意味しません。",
        "",
    ]
    return "\n".join(lines)


def discovery_log(model: dict[str, Any]) -> str:
    records = model["compliance"]["regulatory_discovery_log"]
    lines = [
        "# Regulatory Discovery Log",
        "",
        "## 対象構成と市場",
        "",
        table(
            ["ID", "市場", "構成"],
            [[item["id"], item["market"], item["configuration_ref"]] for item in records],
        ),
        "",
        "## 探索した公式台帳・探索queryと実行時点",
        "",
        table(
            ["ID", "公式探索先", "Query", "Query記録状態", "実行時点"],
            [[item["id"], item["official_registers_checked"], item["queries"], item["query_log_state"], item["searched_at"]] for item in records],
        ),
        "",
        "## 採用・除外・保留候補Sourceと理由",
        "",
        table(
            ["ID", "候補Source", "扱い", "理由"],
            [[item["id"], item["candidate_source_refs"], item["disposition"], item["disposition_reason"]] for item in records],
        ),
        "",
        "## 網羅性の限界・人によるinventory確認",
        "",
        table(
            ["ID", "Query記録状態", "inventory確認"],
            [[item["id"], item["query_log_state"], item["human_inventory_confirmation_state"]] for item in records],
        ),
        "",
        "> Queryまたは除外候補が未記録、あるいは人のinventory確認がpendingの場合、探索の網羅性を主張できません。",
        "",
    ]
    return "\n".join(lines)


def expected_files(model: dict[str, Any]) -> dict[str, bytes]:
    return {
        "17_compliance_source_register.md": source_register(model).encode("utf-8"),
        "18_applicability_obligation_register.md": applicability_register(model).encode("utf-8"),
        "19_engineering_projection_traceability.csv": projection_csv(model),
        "20_conformity_evidence_plan.md": evidence_plan(model).encode("utf-8"),
        "21_regulatory_discovery_log.md": discovery_log(model).encode("utf-8"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = expected_files(load_json(args.model))
    errors: list[str] = []
    for name, expected in outputs.items():
        path = args.output_dir / name
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                errors.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if errors:
        print("FAIL stale_or_missing=" + ",".join(errors))
        return 1
    print(("PASS checked" if args.check else "PASS exported") + f" files={len(outputs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
