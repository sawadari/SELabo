"""Render deterministic Markdown/CSV views from a document projection model."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def display(value: Any) -> str:
    if not isinstance(value, dict) or "value" not in value:
        return "未指定" if value in (None, "", []) else str(value)
    raw = value.get("value")
    text = "未確定" if raw in (None, "", []) else str(raw)
    if value.get("state") == "not_determined":
        return f"【未確定】{text}"
    if value.get("state") == "candidate":
        return f"【候補】{text}"
    return text


def markdown_list(values: list[Any]) -> str:
    if not values:
        return "- 未指定"
    return "\n".join(f"- {display(value)}" for value in values)


def table_cell(value: Any) -> str:
    return display(value).replace("|", "\\|").replace("\n", " ")


def render_planning(model: dict[str, Any]) -> str:
    planning = model["planning"]
    scope = planning["scope"]
    lines = [
        f"# {display(planning['title'])}",
        "",
        "> 文書状態: candidate。本文の意味は `10_se_model.json` を正本とし、この文書は投影です。",
        "",
        "## エグゼクティブサマリ",
        "",
        display(planning["executive_summary"]),
        "",
        "## 背景",
        "",
        markdown_list(planning["background"]),
        "",
        "## 問題・機会",
        "",
        markdown_list(planning["problem_opportunity"]),
        "",
        "## 目的",
        "",
        markdown_list(planning["purpose"]),
        "",
        "## 目標とKPI",
        "",
        "- KPI参照: " + (", ".join(planning["kpi_refs"]) if planning["kpi_refs"] else "未指定"),
        "",
        "## 対象範囲",
        "",
        "### 対象",
        "",
        markdown_list(scope["included"]),
        "",
        "### 対象外",
        "",
        markdown_list(scope["excluded"]),
        "",
        "## スケジュール",
        "",
        f"- 状態: {planning['schedule']['state']}",
        "- マイルストーン: " + (", ".join(item["name"] for item in planning["schedule"]["milestones"]) if planning["schedule"]["milestones"] else "未指定"),
        "",
        "## 予算",
        "",
        f"- 状態: {planning['budget']['state']}",
        f"- 通貨: {planning['budget']['currency']}",
        "- 金額: 未確定（正本に基準値なし）" if planning["budget"]["capex"] is None else f"- 金額: {planning['budget']['capex']}",
        "",
        "## リスク・仮定・未確定事項",
        "",
        "- リスク: " + (", ".join(planning["risk_refs"]) if planning["risk_refs"] else "未指定"),
        "- 仮定: " + (", ".join(planning["assumption_refs"]) if planning["assumption_refs"] else "未指定"),
        "- オープン事項: " + (", ".join(planning["open_issues"]) if planning["open_issues"] else "未指定"),
        "",
        "## 位置づけ",
        "",
        "この文書は候補初稿であり、承認済み企画、確定予算、確定スケジュールを意味しません。",
        "",
    ]
    return "\n".join(lines)


def render_requirements(model: dict[str, Any]) -> str:
    requirements = model["requirements_definition"]
    lines = [
        f"# {model['meta']['target_system']} 要件定義書",
        "",
        "> 文書状態: candidate。要求の意味は `10_se_model.json` を正本とし、`DOCREQ-*`は文書投影上の参照レジストリです。",
        "",
        "## 目的",
        "",
        display(requirements["purpose"]),
        "",
        "## システムコンテキスト",
        "",
        f"- 対象システム: {requirements['system_context']['target_system']}",
        "- 外部システム: " + (", ".join(requirements["system_context"]["external_systems"]) if requirements["system_context"]["external_systems"] else "未指定"),
        "",
        "## 要求一覧",
        "",
        "| DOCREQ | 正本要求 | 分類 | 要求文 | 状態 |",
        "|---|---|---|---|---|",
    ]
    for item in requirements["requirements"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    item["id"],
                    item["source_requirement_ref"],
                    item["classification"]["primary"],
                    table_cell(item["rendered_statement"]),
                    item["rendered_statement"]["state"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 要求分類ビュー",
            "",
            "- 業務: " + (", ".join(requirements["views"]["business_refs"]) or "未指定"),
            "- 機能: " + (", ".join(requirements["views"]["functional_refs"]) or "未指定"),
            "- 非機能: " + (", ".join(requirements["views"]["nonfunctional_refs"]) or "未指定"),
            "- セキュリティ: " + (", ".join(requirements["views"]["security_refs"]) or "未指定"),
            "- データ: " + (", ".join(requirements["views"]["data_refs"]) or "未指定"),
            "- インターフェース: " + (", ".join(requirements["views"]["interface_refs"]) or "未指定"),
            "- 運用・支援: " + (", ".join(requirements["views"]["operational_refs"] + requirements["views"]["support_refs"]) or "未指定"),
            "- 移行: " + (", ".join(requirements["views"]["migration_refs"]) or "未指定"),
            "- テスト要求: " + (", ".join(requirements["views"]["test_requirement_refs"]) or "未指定"),
            "- 未分類: " + (", ".join(requirements["views"]["unclassified_refs"]) or "未指定"),
            "",
            "## データモデルと品質",
            "",
            "- データモデル: " + (", ".join(requirements["data_model"]["model_refs"]) if requirements["data_model"] else "未指定"),
            "- データ品質基準: " + (requirements["data_model"]["quality_requirements"][0]["state"] if requirements["data_model"] and requirements["data_model"]["quality_requirements"] else "未指定"),
            "",
            "## 検証・妥当性確認・受入",
            "",
            "- 検証ケース: " + (", ".join(requirements["verification"]["verification_case_refs"]) or "未指定"),
            "- 妥当性確認ケース: " + (", ".join(requirements["validation"]["validation_case_refs"]) or "未指定"),
            "- 受入条件: " + (", ".join(requirements["acceptance"]["acceptance_criteria_refs"]) or "未指定"),
            "",
            "## 未確定事項",
            "",
            "- " + (", ".join(requirements["open_issues"]) if requirements["open_issues"] else "未指定"),
            "",
            "この文書は候補初稿であり、要求ベースライン、設計承認、試験実施、受入完了を意味しません。",
            "",
        ]
    )
    return "\n".join(lines)


def render_traceability(model: dict[str, Any], output: Path) -> None:
    rows: list[dict[str, Any]] = []
    planning = model["planning"]
    for order, (section_id, values) in enumerate(
        [("PLN-01", planning["background"]), ("PLN-02", planning["problem_opportunity"]), ("PLN-03", planning["purpose"])],
        start=1,
    ):
        for value in values:
            rows.append(
                {
                    "document_kind": "planning",
                    "section_id": section_id,
                    "order": order,
                    "element_id": value["source_refs"][0] if value["source_refs"] else "",
                    "source_refs": ";".join(value["source_refs"]),
                    "derivation": value["derivation"],
                    "state": value["state"],
                    "source_of_truth": "10_se_model.json",
                }
            )
    for order, item in enumerate(model["requirements_definition"]["requirements"], start=1):
        value = item["rendered_statement"]
        rows.append(
            {
                "document_kind": "requirements_definition",
                "section_id": "REQ-01",
                "order": order,
                "element_id": item["id"],
                "source_refs": ";".join(value["source_refs"]),
                "derivation": value["derivation"],
                "state": value["state"],
                "source_of_truth": "10_se_model.json",
            }
        )
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["document_kind"])
        writer.writeheader()
        writer.writerows(rows)


def render_quality(model: dict[str, Any]) -> str:
    quality = model["quality"]
    lines = [
        "# 文書生成品質レポート",
        "",
        "## 判定",
        "",
        "| 検査 | 状態 |",
        "|---|---|",
        f"| Schema | {quality['schema_validation']} |",
        f"| 参照整合性 | {quality['reference_integrity']} |",
        f"| 投影一貫性 | {quality['projection_consistency']} |",
        f"| 日本語技術文章 | {quality['japanese_writing_validation']} |",
        "",
        "## 未実施",
        "",
    ]
    lines.extend(f"- {item}" for item in quality["not_performed"])
    lines.extend(["", "## 位置づけ", "", "本レポートは候補生成の検査状態を示すもので、承認・受入・法令適合を証明しません。", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document_model", type=Path)
    args = parser.parse_args()
    model = load_json(args.document_model)
    output_dir = args.document_model.parent
    (output_dir / "21_planning_document.md").write_text(render_planning(model), encoding="utf-8", newline="\n")
    (output_dir / "22_requirements_definition.md").write_text(render_requirements(model), encoding="utf-8", newline="\n")
    render_traceability(model, output_dir / "23_document_traceability.csv")
    (output_dir / "24_document_quality_report.md").write_text(render_quality(model), encoding="utf-8", newline="\n")
    manifest = {
        "artifact_type": "document_generation_bundle_candidate",
        "source_of_truth": "10_se_model.json",
        "document_model": "20_document_model.json",
        "outputs": [
            "21_planning_document.md",
            "22_requirements_definition.md",
            "23_document_traceability.csv",
            "24_document_quality_report.md",
        ],
        "render_formats_not_performed": ["html", "docx", "pdf"],
        "document_status": model["meta"]["document_status"],
        "source_hash": model["source_binding"]["content_hash"],
    }
    (output_dir / "25_document_generation_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print("PASS")
    print(f"- output directory: {output_dir}")
    print("- markdown views: planning, requirements_definition")
    print("- traceability: CSV")
    print("- html/docx/pdf: not_performed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
