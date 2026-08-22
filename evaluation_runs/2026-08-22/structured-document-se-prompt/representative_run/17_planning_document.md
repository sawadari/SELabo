# 保全依頼管理システム 企画書

## 文書の位置付け

この文書は、実験3の候補意味正本から生成した企画書ビューの候補初稿である。正本は `10_se_model.json` として参照され、物理入力は `experiments/structured-document-se-prompt/examples/representative_model.json` である。本文中のID、名称、状態、`null`、`tbd` は正本の値を投影しており、本書で確定・承認したものではない。

対象システム: `保全依頼管理システム`  
正本状態: `candidate_semantic_source_of_truth`  
ビューID: `VIEW-0001`  
ビュー種別: `planning_document`  
想定読者: 企画レビュー参加者  

## 1. 事業背景

### 1.1 背景と問題・機会

- 背景: 現行業務では保全依頼が電話とメールに分散している。
- 問題・機会: 依頼の受付状況と処理状況を一元的に把握しにくい。
- 対象サービス・業務: 設備保全依頼業務。
- 提供価値: 依頼受付と進捗確認を一元化する。

出典要素: `planning.business_context`、`SRC-0001`。

### 1.2 企画対象

- 対象システム: 保全依頼管理システム。
- 目的: 保全依頼の受付と進捗確認を一元化する。
- 対象業務上の機会: 電話とメールに分散した依頼の状況を把握しにくい状態を扱う。

## 2. 目的とKPI

### 2.1 目的

| ID | 名称 | 目的文 | 状態 |
|---|---|---|---|
| `OBJ-0001` | 受付所要時間を短縮する | 保全依頼の受付所要時間を短縮する。 | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=medium` |

`OBJ-0001` のKPI参照は `KPI-0001`、ステークホルダー参照は `STK-0001`、要求参照は `REQ-0001` である。

### 2.2 KPI

| ID | 名称 | 観測対象 | 単位 | 基準値・目標値 | 測定文脈 | 状態 |
|---|---|---|---|---|---|---|
| `KPI-0001` | 保全依頼受付所要時間 | 依頼登録から受付完了表示までの時間 | `min` | `null` | 現状値と目標値は企画レビューで確認する | `origin=ai_context_inference`; `claim_state=inferred`; `decision_state=proposed`; `validity_state=active`; `baseline_state=outside_baseline`; `confidence=low` |

`KPI-0001.target_or_range` は `null` のまま保持する。数値、許容範囲、基準値、目標値は補完していない。

## 3. 対象ユーザー

`planning.target_user_refs` の参照先は次のとおりである。

| ID | 名称 | 由来 | 主張状態 | 決定状態 | 適用性 | 確信度 |
|---|---|---|---|---|---|---|
| `STK-0001` | 設備運用者 | `user_explicit` | `stated` | `proposed` | `applicable` | `high` |
| `STK-0002` | 保全担当者 | `ai_context_inference` | `inferred` | `proposed` | `uncertain` | `medium` |

`STK-0002` は、業務分担の確認が必要な候補である。これは正本の `applicability_rationale` に従った表示であり、企画書で確定していない。

## 4. 対象範囲

### 4.1 含む範囲

- 保全依頼登録
- 進捗確認
- 通知

### 4.2 含まない範囲

- 設備の直接制御

### 4.3 外部システムと運用環境

- 外部システム: 認証サービス
- 運用環境: 設備運用者と保全担当者が業務で利用する
- ライフサイクル範囲: `concept`, `utilization`, `support`

範囲要素は `scope` から投影した。成功指標参照は `KPI-0001`、仮定参照は `ASM-0001` である。

### 4.4 仮定

| ID | 名称 | 仮定文 | 確認方法 | 人による確認 |
|---|---|---|---|---|
| `ASM-0001` | 利用者が認証できる | 設備運用者と保全担当者は認証サービスを利用できる。 | 業務・セキュリティ担当者への確認 | `true` |

この仮定は `assumed`、`proposed`、`active`、`outside_baseline`、`low` の状態を持つ候補である。認証方式や利用者区分が決定されたときが改訂条件である。

## 5. 代替案・市場分析

- 分析状態: `not_performed`
- 代替案: `[]`
- 証拠参照: `[]`
- 注記: 現行運用継続、既存サービス導入、個別開発の比較は未実施。

市場分析や代替案の評価結果は、正本にないため追加していない。

## 6. 費用とスケジュール

### 6.1 費用

| 通貨 | 下限 | 基準 | 上限 | 値の状態 | 見積根拠 |
|---|---:|---:|---:|---|---|
| `JPY` | `null` | `null` | `null` | `tbd` | 費用見積条件が未指定 |

費用は未指定であり、金額を補完していない。

### 6.2 スケジュール

- 値の状態: `tbd`
- マイルストーン: `[]`

日付、期間、マイルストーンは未指定であり、補完していない。

## 7. 体制と未確定事項

### 7.1 ガバナンス

- スポンサー参照: `null`
- 意思決定プロセス: 企画レビューで確認する
- 承認状態: `proposed`

### 7.2 企画レビューで確認する事項

- `KPI-0001`: 現状値、目標値、基準値・範囲。
- `STK-0002`: 業務分担と適用性。
- `ASM-0001`: 認証サービスの利用可否、認証方式、利用者区分。
- `planning.market_analysis`: 代替案・市場分析。
- `planning.cost_estimate`: 見積条件と費用。
- `planning.schedule`: スケジュールとマイルストーン。
- `planning.governance.sponsor_ref`: スポンサー。

## 文書ビューの参照

`VIEW-0001` の `section_order` に従い、次の順序で投影した。

1. `PLAN-01` 事業背景と目的: `OBJ-0001`, `NEED-0001`
2. `PLAN-02` 対象範囲: `REQ-0001`

企画書の内容は、上記の要素および正本の `planning`、`scope` から投影したものであり、独立した事実を追加していない。
