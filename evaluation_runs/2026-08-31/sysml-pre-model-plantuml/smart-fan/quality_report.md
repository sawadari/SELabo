# 実験5試行品質レポート：スマート扇風機

## 結論

この試行は、投影ルールに関する機械的検査を通過し、実験5のP1パイロットとして`pass_with_provisional_assumption`とする。生成した9ファイルのうち、スタイルSnippetを除く8図は、正本IDまたは正本Scenarioをメタデータへ記録した。Scenarioから作ったAction／MessageはVIEW_DERIVEDとして明示した。

これは正式SysMLモデル、XMI、ツールインポート成功、設計承認、法規・安全適合、検証完了を意味しない。

## 試行メタデータ

| 項目 | 内容 |
|---|---|
| run_id | `E5-2026-08-31-SF-01` |
| target_system | スマート扇風機 |
| condition | P1：実験5コアプロンプト＋Profile＋Quality Rules |
| base_experiment | `hierarchical-se-prompt` 1.1.0 |
| input | 実験1系スマート扇風機候補モデル |
| generated_diagrams | 8（style snippetを除く） |
| strict_projection | 3 |
| projection_with_view_derived_elements | 4 |
| insufficient_data | 6種別をIndexへ記録 |
| executed_at | 2026-08-31 Asia/Tokyo |

## 生成結果

| 図 | 判定 | 根拠 |
|---|---|---|
| Requirement | 生成 | requirements 7件 |
| Activity × 2 | 生成 | Scenario main_flowの明示順序。ActionはVD |
| Sequence × 2 | 生成 | Scenario主体と順序をVD表示。Interfaceは未生成 |
| BDD | 生成 | System Structure 1件。境界限定 |
| Verification Trace | 生成 | target_requirement_refs 7件 |
| Context | 未生成 | 外部Interface不足 |
| Use Case | 未生成 | use_cases 0件 |
| IBD | 未生成 | interfaces 0件、part_refs空 |
| State Machine | 未生成 | State/Transition/Trigger不足 |
| Parametric | 未生成 | constraints 0件 |
| Package | 未生成 | package_hierarchy不足 |

## 検査結果

| 検査 | 結果 | 方法・注記 |
|---|---|---|
| JSON parse | pass | Python `json`で入力を解析 |
| `se_model.schema.json` | pass | jsonschema Draft 2020-12で実験1Schemaを検証 |
| ID重複 | pass | 入力内のIDを収集して重複なし |
| 図メタデータ | pass | 8図の必須メタデータとsource IDを確認 |
| source ID解決 | pass | 図メタデータのCanonical source IDを入力へ解決 |
| PlantUML境界・外部リソース | pass | `@startuml`/`@enduml`、外部URLなしを確認 |
| PlantUML実構文 | pass | PlantUML 1.2026.7 `-checkonly`で8図を確認 |
| 画像レンダリング・可読性 | pass_with_provisional_assumption | PNGを8枚生成し目視確認。人によるSysML意味レビューは未実施 |
| 人のSysML意味レビュー | not_performed | 形式上の投影検査のみ |
| Cameo / Enterprise Architect投入 | not_performed | ツール非依存のPlantUMLのみ |

## ルール別判定

| 規則 | 判定 | 根拠 |
|---|---|---|
| QP-01 正本境界 | pass | 図へ入力にないCanonical Requirement、Block、Interface、Stateを追加していない |
| QP-02 IDとAlias | pass | Canonical IDを表示名・メタデータへ保持 |
| QP-03 VIEW_DERIVED | pass | `VD_SCN_...`をScenario由来の表示専用要素として明記 |
| QP-04 UNRESOLVED | pass_with_provisional_assumption | Interface、State、Constraint等の不足をIndexとNoteへ記録 |
| QP-05 図の生成条件 | pass | 入力件数と生成／未生成理由が一致 |
| QP-06 Relationship | pass | Verification Traceのみtarget refsから投影。要求間関係はrelations空のため未表示 |
| QP-07 抽象度 | pass_with_provisional_assumption | BDDはSystem Structureの境界確認に限定 |
| QP-08 Cross-Diagram | pass_with_provisional_assumption | Requirement→Verification 7/7、IBD関連は未適用 |
| QP-09 PlantUML安全性 | pass | 外部リソースなし、PlantUML 1.2026.7で構文実行済み |
| QP-10 文章・名称 | pass_with_provisional_assumption | 正本名称を維持。未確定の尺度はTBDのまま |

## 残る人間確認事項

1. `REQ_SF-0002`の危険状態、最大停止時間、適用安全規格。
2. `REQ_SF-0003`の音圧、風量、測定位置、環境条件、受入れ範囲。
3. `REQ_SF-0007`の法規適用性、対象構成、10 deg試験方法。
4. 通信断・保守時のInterface、状態、再開トリガー、責任境界。
5. Logical / Physical構造、内部Part、Port、Connector、Allocation。

## 判断

入力の構造化範囲内では、後段専用プロンプトにより、要求・Scenario・System境界・Verificationのレビュー用ビューを作成できた。一方、Interfaceと構造化State／Constraintが不足しているため、IBD、State Machine、Parametricは生成しなかった。次の試行では、これらを明示した別入力を使い、SequenceとIBDの整合、State TransitionとScenarioの整合、Parametric bindingの正本保持を確認する。
