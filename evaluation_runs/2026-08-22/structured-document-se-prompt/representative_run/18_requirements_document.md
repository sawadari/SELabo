# 保全依頼管理システム 要件定義書

## 文書の正本性

この文書は、実験3の候補意味正本から生成した要件定義書ビューの候補初稿である。正本参照名は `10_se_model.json`、物理入力は `experiments/structured-document-se-prompt/examples/representative_model.json` である。本書は正式要求、承認済みベースライン、実施済み試験、受入済み結果を示さない。

対象システム: `保全依頼管理システム`  
正本状態: `candidate_semantic_source_of_truth`  
ビューID: `VIEW-0002`  
ビュー種別: `requirements_document`  
想定読者: 要求・設計レビュー参加者  

## 1. 業務要件

### 1.1 業務目的と範囲

- 目的: 保全依頼の受付と進捗確認を一元化する。
- 対象業務: 設備保全依頼業務。
- 含む範囲: 保全依頼登録、進捗確認、通知。
- 含まない範囲: 設備の直接制御。
- 外部システム: 認証サービス。

### 1.2 ニーズ

| ID | 名称 | ニーズ文 | 期待価値 | 状態 |
|---|---|---|---|---|
| `NEED-0001` | 保全依頼の状況を把握する | 設備運用者と保全担当者は、保全依頼の受付と処理状況を確認したい。 | 依頼状況を共有できる | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

参照ステークホルダー: `STK-0001`, `STK-0002`。成功指標: `KPI-0001`。妥当性確認候補: `VAL-0001`。

### 1.3 ユースケース

| ID | 名称 | 状態 |
|---|---|---|
| `UC-0001` | 保全依頼を登録する | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

`VAL-0001` は、設備運用者が依頼を登録し、保全担当者が処理状況を更新する運用文脈で、`NEED-0001` の価値を確認する候補である。妥当性確認は未実施である。

## 2. 機能要件

### 2.1 要求一覧

| 要求ID | 名称 | 要求文 | 要求種別 | 規範レベル | カテゴリ | 状態 |
|---|---|---|---|---|---|---|
| `REQ-0001` | 保全依頼受付 | 有効な保全依頼を受信したとき、保全依頼管理システムは、受付結果を画面に表示する。 | `system_requirement` | `mandatory` | `functional` | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

### 2.2 要求の条件と参照

- 条件: `null`
- トリガー: 有効な保全依頼を受信する
- 必要な応答・性質: 受付結果を画面に表示する
- 対象: 受付結果
- 性能・制限: `null`
- 単位: `null`
- 許容差: `null`
- 導出元ニーズ: `NEED-0001`
- 導出根拠: `NEED-0001から導出した候補要求`
- 配分候補: `[]`
- 検証方法候補: `demonstration`
- 受入条件候補: 受付結果が表示されること
- 画面参照: `SCR-0001`
- API契約参照: `API-0001`
- データモデル参照: `DATA-0001`
- 検証ケース参照: `VER-0001`
- 受入条件参照: `ACC-0001`

上記の `null` は未指定値であり、条件、性能、単位、許容差を補完していない。

## 3. 非機能・セキュリティ要件

### 3.1 運用・保守

`operations_maintenance` の状態は `candidate` である。次の参照配列はすべて空である。

- 運用要求参照: `[]`
- 保守要求参照: `[]`
- 移行要求参照: `[]`
- 教育要求参照: `[]`
- サービスレベル候補: `[]`

したがって、本正本から運用時間、保守時間、移行手順、教育計画、サービスレベルを追加していない。

### 3.2 セキュリティ

`security` の人によるレビュー状態は `pending` である。セキュリティ要求参照、脅威候補、管理策候補、検証参照はすべて `[]` である。`ASM-0001` は認証サービス利用に関する仮定であり、セキュリティ承認や認証方式の決定を意味しない。

## 4. 画面・帳票・API・データ

### 4.1 画面

| ID | 名称 | 種別 | 目的 | 利用者 | 要求参照 | 入力候補 | 状態 |
|---|---|---|---|---|---|---|---|
| `SCR-0001` | 保全依頼登録画面 | `input` | 保全依頼を登録する | `STK-0001` | `REQ-0001` | 依頼内容: `text`, `required` | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

画面遷移参照は `[]` である。

### 4.2 帳票・レポート

| ID | 名称 | 種別 | 目的 | 対象者 | データ参照 | 要求参照 | 状態 |
|---|---|---|---|---|---|---|---|
| `RPT-0001` | 保全依頼進捗一覧 | `list` | 保全依頼の進捗を確認する | `STK-0002` | `DATA-0001` | `[]` | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=low` |

`RPT-0001` は正本の `reports` から投影した候補である。`VIEW-0002.element_refs` には含まれていないため、文書ビューの明示参照外であることをトレーサビリティに記録した。

### 4.3 API契約

| ID | 名称 | 種別 | スタイル | 仕様バージョン | 外部仕様参照 | 操作参照 | 要求参照 | 契約状態 |
|---|---|---|---|---|---|---|---|---|
| `API-0001` | 保全依頼API | `api_contract` | `openapi` | `null` | `null` | `[]` | `REQ-0001` | `candidate` |

APIのパス、HTTPメソッド、パラメータ、要求・応答型、認証方式は未指定である。OpenAPI契約の候補参照だけを表示し、パスや型を捏造していない。

### 4.4 データモデル

| ID | 名称 | 種別 | モデル種別 | エンティティ候補 | 関係候補 | 要求参照 | 状態 |
|---|---|---|---|---|---|---|---|
| `DATA-0001` | 保全依頼論理データモデル | `data_model` | `logical` | 保全依頼 | `[]` | `REQ-0001` | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=low` |

エンティティ候補 `保全依頼` の属性候補は `依頼内容`（値型 `text`）である。関係候補は `[]` であり、関係線を補完していない。Mermaid投影は `21_data_model.mermaid.md` に分離している。

## 5. 検証と受入条件

### 5.1 検証ケース

| ID | 名称 | 対象要求 | 方法 | 事前条件 | 入力・刺激 | 観測可能結果 | 状態 |
|---|---|---|---|---|---|---|---|
| `VER-0001` | 保全依頼受付確認 | `REQ-0001` | `demonstration` | 利用者が保全依頼登録画面を利用できる | 有効な保全依頼 | 受付結果が画面に表示されること | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

- 環境: 試験用の保全依頼管理環境
- 測定方法: 目視確認
- 受入条件候補: 受付結果が表示されること
- 必要証拠: `[]`
- 責任ロール参照: `STK-0002`
- ライフサイクル段階: `development`

### 5.2 受入条件

| ID | 名称 | 要求参照 | 事前条件 | イベント | 期待結果 | 合格規則 | 検証参照 | 状態 |
|---|---|---|---|---|---|---|---|---|
| `ACC-0001` | 保全依頼受付の受入条件 | `REQ-0001` | 利用者が保全依頼登録画面を利用できる | 有効な保全依頼を送信する | 受付結果が表示される | `VER-0001が合格すること` | `VER-0001` | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

`VER-0001` の検証および `ACC-0001` の受入判定は実施していない。`22_acceptance_criteria.feature` はこの受入条件の投影であり、実行結果ではない。

## 6. 未確定事項

- `REQ-0001.condition`, `performance_or_limit`, `unit`, `tolerance`: `null`。
- `API-0001.spec_version`, `spec_ref`: `null`。OpenAPI仕様は未提供。
- `RPT-0001.requirement_refs`: `[]`。
- `DATA-0001.relationship_candidates`: `[]`。
- `operations_maintenance` の各要求参照、サービスレベル候補: `[]`。
- `security` の要求、脅威、管理策、検証参照: `[]`、人によるレビュー状態は `pending`。
- `KPI-0001.target_or_range`: `null`。KPIの現状値と目標値は企画レビューで確認する。
- `market_analysis.analysis_state`: `not_performed`。
- `planning.cost_estimate`: 金額は `null`、値の状態は `tbd`。
- `planning.schedule.value_state`: `tbd`、マイルストーンは `[]`。
- `planning.governance.sponsor_ref`: `null`、承認状態は `proposed`。
