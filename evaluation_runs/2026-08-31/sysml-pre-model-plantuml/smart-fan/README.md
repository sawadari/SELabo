# 実験5評価実行：スマート扇風機

## 結論

実験1系の候補SEモデルを入力に、要求、Scenario由来のActivity／Sequence、System境界BDD、Requirement・Verification Traceをレビュー用PlantUMLとして作成できた。入力に存在しないInterface、内部Part、State Transition、Constraint、Packageは生成しなかった。

入力Schema・ID・メタデータ・PlantUML境界検査、PlantUMLレンダラーによる実構文検証、PNG生成と目視確認はPASSした。人によるSysML意味レビュー、正式モデリングツールへの投入は未実施である。

## 実行情報

| 項目 | 内容 |
|---|---|
| run_id | `E5-2026-08-31-SF-01` |
| target_system | スマート扇風機 |
| condition | P1：実験5後段投影プロンプト |
| executed_at | 2026-08-31 Asia/Tokyo |
| source_of_truth | `10_se_model.json` |
| source_model | [candidate_model.json](../../../2026-08-22/compliance-integrated-se-prompt/smart-fan/candidate_model.json) |
| result_archive | [smart-fan_sysml_pre_model_plantuml.zip](smart-fan_sysml_pre_model_plantuml.zip) |

## 成果物

- [input_reference.md](input_reference.md)：入力と適用範囲
- [quality_report.md](quality_report.md)：検査結果と未実施事項
- [00_style.puml](00_style.puml)：ローカルstyle snippet
- [01_requirement_overview.puml](01_requirement_overview.puml)：Requirement Diagram
- [02_activity_scn_SF_0001.puml](02_activity_scn_SF_0001.puml)：代表運転Activity
- [03_activity_scn_SF_0002.puml](03_activity_scn_SF_0002.puml)：安全側移行Activity
- [04_sequence_scn_SF_0001.puml](04_sequence_scn_SF_0001.puml)：代表運転Sequence
- [05_sequence_scn_SF_0002.puml](05_sequence_scn_SF_0002.puml)：安全側移行Sequence
- [06_system_bdd.puml](06_system_bdd.puml)：System境界BDD
- [07_verification_trace.puml](07_verification_trace.puml)：Requirement・Verification Trace
- [99_generation_index.puml](99_generation_index.puml)：生成／未生成図Index

レンダリング画像は[rendered](rendered/)フォルダーにあります。

## 読み方

Scenarioから作った順序やMessageは`VIEW_DERIVED`であり、新しいBehaviorやInterfaceではない。入力の`interfaces`が空のため、Sequence図は通信契約の確定を示さない。Indexの`insufficient_data`と品質レポートの`TBD`を先に確認する。
