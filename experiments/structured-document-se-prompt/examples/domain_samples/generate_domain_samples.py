"""Create small domain fixtures from the representative SELabo semantic model."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


SCENARIOS: dict[str, dict[str, Any]] = {
    "automotive": {
        "target_system": "次世代電動SUV",
        "source_summary": "次世代電動SUVの商品企画と車両システム要求を一貫して定義・検証したい。",
        "purpose": "次世代電動SUVの商品価値と車両システム要求を整合させる",
        "problem": "商品企画、車両システム設計、評価計画に分散した要求と前提条件を一貫して追跡しにくい",
        "included": ["車両基本性能要求", "高電圧バッテリー・充電要求", "車両エネルギー管理", "評価・受入条件"],
        "excluded": ["量産工場の設備制御", "対象市場未確定の法規認証取得", "自動運転機能の詳細設計"],
        "external_systems": ["充電インフラ", "車両クラウドサービス", "試験・計測環境"],
        "environment": ["一般道・高速道路を想定した車両利用環境で評価する", "開発・評価担当者が車両システム要求と検証結果を管理する"],
        "glossary_term": "車両システム要求",
        "glossary_definition": "車両全体または車両サブシステムが満たすべき機能・性能・制約を記述した要求",
        "stakeholders": ["車両商品企画担当", "車両開発・評価担当"],
        "concern": "商品価値・車両性能・安全要求の整合性",
        "need_name": "車両の商品価値とシステム要求を追跡する",
        "need_statement": "車両商品企画担当と車両開発・評価担当は、商品価値から車両システム要求と検証結果までを追跡したい。",
        "value": "商品企画と車両開発の判断根拠を共有できる",
        "kpi_name": "車両システム要求の検証完了率",
        "kpi_observable": "承認対象の車両システム要求に対して検証結果が記録された割合",
        "use_case": "車両システム要求を定義・検証する",
        "requirement_name": "充電状態表示",
        "requirement_statement": "走行用バッテリーの充電状態を取得できるとき、次世代電動SUVは、運転者に充電状態を表示する。",
        "required_response": "運転者に充電状態を表示する",
        "screen": "メーターディスプレイ",
        "screen_purpose": "運転者へ車両状態を表示する",
        "report": "車両性能評価レポート",
        "report_purpose": "車両システム要求に対する評価結果を確認する",
        "api": "車両診断インターフェース",
        "data_model": "車両エネルギー管理論理データモデル",
        "entity": "充電状態情報",
        "attribute": "充電状態",
        "assumption": "対象市場と評価条件を確定できる",
        "assumption_statement": "開発チームは対象市場の法規・評価条件を車両要求の確定前に確認できる。",
        "acceptance": "充電状態表示の受入条件",
        "event": "走行用バッテリーの充電状態を取得する",
        "expected": "メーターディスプレイに充電状態が表示される",
        "objective": "商品企画の性能目標と車両システム要求を整合させる",
        "section_1": "車両開発企画の背景と目的",
        "section_2": "車両システム要求",
    },
    "manufacturing": {
        "target_system": "工場設備保全依頼管理システム",
        "source_summary": "工場設備の保全依頼受付と復旧状況を一元管理したい。",
        "purpose": "工場設備の保全依頼受付と復旧状況確認を一元化する",
        "problem": "電話・紙・個別チャットに分散した設備異常と復旧状況を把握しにくい",
        "included": ["設備異常登録", "保全作業割当確認", "復旧状況通知"],
        "excluded": ["設備の自動制御", "安全インターロックの変更"],
        "external_systems": ["工場認証サービス", "設備台帳システム"],
        "environment": ["製造ライン担当者が異常を登録する", "保全担当者が復旧状況を更新する"],
        "glossary_term": "設備異常",
        "glossary_definition": "設備の停止、性能低下、または異常兆候を示す業務情報",
        "stakeholders": ["製造ライン担当者", "保全担当者"],
        "concern": "設備異常と復旧状況の可視性",
        "need_name": "設備異常と復旧状況を把握する",
        "need_statement": "製造ライン担当者と保全担当者は、設備異常の受付と復旧状況を確認したい。",
        "value": "異常と復旧状況を共有できる",
        "kpi_name": "設備異常受付所要時間",
        "kpi_observable": "異常発生から保全依頼登録完了表示までの時間",
        "use_case": "設備異常を登録する",
        "requirement_name": "設備異常受付",
        "requirement_statement": "有効な設備異常を受信したとき、工場設備保全依頼管理システムは、受付結果を画面に表示する。",
        "required_response": "受付結果を画面に表示する",
        "screen": "設備異常登録画面",
        "screen_purpose": "設備異常を登録する",
        "report": "設備保全進捗一覧",
        "report_purpose": "設備異常の復旧状況を確認する",
        "api": "設備保全依頼API",
        "data_model": "設備保全依頼論理データモデル",
        "entity": "設備保全依頼",
        "attribute": "設備識別番号",
        "assumption": "設備台帳を参照できる",
        "assumption_statement": "製造ライン担当者は設備台帳システムから設備情報を参照できる。",
        "acceptance": "設備異常受付の受入条件",
        "event": "有効な設備異常を送信する",
        "expected": "受付結果が表示される",
        "objective": "設備異常の受付所要時間を短縮する",
        "section_1": "工場保全業務の背景と目的",
        "section_2": "設備保全の機能要件",
    },
    "logistics": {
        "target_system": "物流拠点入出荷作業管理システム",
        "source_summary": "物流拠点の入出荷作業受付と進捗確認を一元管理したい。",
        "purpose": "物流拠点の入出荷作業受付と進捗確認を一元化する",
        "problem": "電話・紙・個別表計算に分散した入出荷作業の進捗を把握しにくい",
        "included": ["入荷作業登録", "出荷作業進捗確認", "作業遅延通知"],
        "excluded": ["車両の自動運転制御", "荷主との契約条件変更"],
        "external_systems": ["物流拠点認証サービス", "在庫管理システム"],
        "environment": ["拠点担当者が入出荷作業を登録する", "現場責任者が作業進捗を更新する"],
        "glossary_term": "入出荷作業",
        "glossary_definition": "物流拠点で貨物の入荷または出荷を処理する業務作業",
        "stakeholders": ["拠点担当者", "現場責任者"],
        "concern": "入出荷作業の進捗可視性",
        "need_name": "入出荷作業の進捗を把握する",
        "need_statement": "拠点担当者と現場責任者は、入出荷作業の受付と処理状況を確認したい。",
        "value": "作業進捗を共有できる",
        "kpi_name": "入出荷作業受付所要時間",
        "kpi_observable": "作業受付開始から受付完了表示までの時間",
        "use_case": "入出荷作業を登録する",
        "requirement_name": "入出荷作業受付",
        "requirement_statement": "有効な入出荷作業を受信したとき、物流拠点入出荷作業管理システムは、受付結果を画面に表示する。",
        "required_response": "受付結果を画面に表示する",
        "screen": "入出荷作業登録画面",
        "screen_purpose": "入出荷作業を登録する",
        "report": "入出荷作業進捗一覧",
        "report_purpose": "入出荷作業の進捗と遅延を確認する",
        "api": "入出荷作業API",
        "data_model": "入出荷作業論理データモデル",
        "entity": "入出荷作業",
        "attribute": "作業受付番号",
        "assumption": "在庫情報を参照できる",
        "assumption_statement": "拠点担当者は在庫管理システムから対象貨物の情報を参照できる。",
        "acceptance": "入出荷作業受付の受入条件",
        "event": "有効な入出荷作業を送信する",
        "expected": "受付結果が表示される",
        "objective": "入出荷作業の受付所要時間を短縮する",
        "section_1": "物流業務の背景と目的",
        "section_2": "入出荷作業の機能要件",
    },
}


def apply_scenario(base: dict[str, Any], scenario: dict[str, Any], slug: str) -> dict[str, Any]:
    model = copy.deepcopy(base)
    meta = model["meta"]
    meta["target_system"] = scenario["target_system"]
    meta["sample_domain"] = slug

    model["source_fragments"][0].update(
        {
            "content_summary": scenario["source_summary"],
            "source_locator": f"sample_domain:{slug}",
        }
    )
    scope = model["scope"]
    scope.update(
        {
            "target_system": scenario["target_system"],
            "purpose": scenario["purpose"],
            "problem_or_opportunity": scenario["problem"],
            "included": scenario["included"],
            "excluded": scenario["excluded"],
            "external_systems": scenario["external_systems"],
            "operational_environment": scenario["environment"],
        }
    )
    model["glossary"][0].update(
        {"term": scenario["glossary_term"], "definition": scenario["glossary_definition"]}
    )
    for item, name in zip(model["stakeholders"], scenario["stakeholders"]):
        item["name"] = name
    model["concerns"][0]["name"] = scenario["concern"]
    need = model["needs"][0]
    need.update(
        {
            "name": scenario["need_name"],
            "statement": scenario["need_statement"],
            "expected_value": scenario["value"],
        }
    )
    measure = model["measures"][0]
    measure.update(
        {
            "name": scenario["kpi_name"],
            "observable": scenario["kpi_observable"],
            "measurement_context": "現状値と目標値は業務レビューで確認する",
        }
    )
    model["use_cases"][0]["name"] = scenario["use_case"]
    requirement = model["requirements"][0]
    requirement.update(
        {
            "name": scenario["requirement_name"],
            "statement": scenario["requirement_statement"],
            "subject": scenario["target_system"],
            "trigger": scenario["event"],
            "required_response_or_property": scenario["required_response"],
            "object": "受付結果",
        }
    )
    model["verification_cases"][0].update(
        {
            "name": f"{scenario['requirement_name']}確認",
            "objective": f"{scenario['requirement_name']}の表示結果を確認する",
            "item_under_verification": "受付結果表示",
            "observable": "受付結果が画面に表示されること",
            "preconditions": ["利用者が登録画面を利用できる"],
        }
    )
    model["validation_cases"][0]["operational_context"] = f"{scenario['stakeholders'][0]}が登録し、{scenario['stakeholders'][1]}が処理状況を更新する"
    assumption = model["assumptions"][0]
    assumption.update({"name": scenario["assumption"], "statement": scenario["assumption_statement"]})
    planning = model["planning"]
    planning["business_context"].update(
        {
            "background": scenario["problem"],
            "problem_or_opportunity": scenario["problem"],
            "target_service_or_business": scenario["target_system"],
            "value_proposition": scenario["purpose"],
        }
    )
    planning["objectives"][0].update(
        {"name": scenario["objective"], "statement": f"{scenario['objective']}。"}
    )
    model["screens"][0].update({"name": scenario["screen"], "purpose": scenario["screen_purpose"]})
    model["reports"][0].update({"name": scenario["report"], "purpose": scenario["report_purpose"]})
    model["api_contracts"][0]["name"] = scenario["api"]
    data_model = model["data_models"][0]
    data_model["name"] = scenario["data_model"]
    data_model["entity_candidates"][0].update(
        {"name": scenario["entity"], "attributes": [{"name": scenario["attribute"], "value_type": "text"}]}
    )
    acceptance = model["acceptance_criteria"][0]
    acceptance.update(
        {
            "name": scenario["acceptance"],
            "event": scenario["event"],
            "expected_outcome": scenario["expected"],
        }
    )
    planning_view, requirements_view = model["document_views"]
    planning_view.update(
        {
            "name": f"{scenario['target_system']}企画書ビュー",
            "title": f"{scenario['target_system']} 企画書",
            "audience": "業務・企画レビュー参加者",
        }
    )
    planning_view["section_order"][0]["title"] = scenario["section_1"]
    requirements_view.update(
        {
            "name": f"{scenario['target_system']}要件定義書ビュー",
            "title": f"{scenario['target_system']} 要件定義書",
            "audience": "要求・設計レビュー参加者",
        }
    )
    requirements_view["section_order"][0]["title"] = scenario["section_2"]
    return model


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("output_root", type=Path)
    args = parser.parse_args()
    with args.base.open(encoding="utf-8") as handle:
        base = json.load(handle)
    for slug, scenario in SCENARIOS.items():
        output = args.output_root / slug / "10_se_model.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        model = apply_scenario(base, scenario, slug)
        with output.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(model, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(f"created: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
