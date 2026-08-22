# Conformity and Evidence Plan

## Gate境界

| モデル品質 | Assurance outcome | Compliance approvalではない | Reviewer Gate |
|---|---|---|---|
| pass_with_provisional_assumption | not_performed | true | generator=pass<br>compliance=review_pending<br>se=review_pending<br>assurance=review_pending<br>meta_judge=not_performed |

## 適合性評価スキーム候補

| ID | 種別 | 所有者 | 決定権者 | 適合対象 | Obligation | 必要Evidence | 独立性 | 出力 |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — |

## 必要な証拠（Evidence Requirement）

| ID | 対象 | 種別 | 必要属性 | 構成必須 | 独立性 | 状態 |
|---|---|---|---|---|---|---|
| EVR-SF-REQ-001 | REQ_SF-0001 | inspection_record | 対象構成<br>選択モード<br>表示結果 | true | none | planned |
| EVR-SF-REQ-002 | REQ_SF-0002 | test_report | 対象構成<br>危険状態定義<br>停止閾値<br>結果 | true | unknown | planned |
| EVR-SF-REQ-003 | REQ_SF-0003 | test_report | 対象構成<br>音圧条件<br>風量条件<br>結果 | true | none | planned |
| EVR-SF-REQ-004 | REQ_SF-0004 | test_report | 対象構成<br>通信切断条件<br>停止結果 | true | none | planned |
| EVR-SF-REQ-005 | REQ_SF-0005 | test_report | 対象構成<br>通信切断条件<br>安全停止条件<br>再開結果 | true | none | planned |
| EVR-SF-REQ-006 | REQ_SF-0006 | test_report | 対象構成<br>清掃状態<br>起動操作<br>結果 | true | none | planned |
| EVR-SF-PSE | OBL-SF-PSE | traceability_report | 対象分類<br>対象構成<br>技術基準版<br>評価活動<br>責任者 | true | unknown | planned |
| EVR-SF-INSPECTION | OBL-SF-INSPECTION | inspection_record | 対象構成<br>検査方法<br>結果<br>実施日<br>責任者 | true | unknown | planned |
| EVR-SF-STABILITY | OBL-SF-STABILITY<br>REQ_SF-0007 | test_report | 対象構成<br>高さ設定<br>通常使用状態<br>傾斜方向<br>傾斜角<br>転倒有無 | true | unknown | planned |
| EVR-SF-AGING | OBL-SF-AGING | inspection_record | 対象構成<br>表示内容<br>表示位置<br>判読性<br>耐久性 | true | unknown | planned |
| EVR-SF-RADIO | OBL-SF-RADIO | supplier_declaration | 無線方式<br>周波数<br>出力<br>モジュール識別<br>免許要否<br>適合表示または証明識別 | true | unknown | planned |

## 存在を確認した証拠（Evidence Item）

| ID | EVR | 構成 | 版 | 検証状態 | 有効性 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 評価活動候補 / Assessment Result / Findingと是正

| Activity | 構成 | 状態 | Result | Outcome | Finding | 有効性 | 人確認 |
|---|---|---|---|---|---|---|---|
| AST-SF-PSE | CFG-SF-CONCEPT | planned | ASR-SF-PSE | not_performed | — | active | pending |
| AST-SF-RADIO | CFG-SF-CONCEPT | planned | ASR-SF-RADIO | not_performed | — | active | pending |

## Attestation

| ID | Scheme | Result | 構成 | 状態 | 有効性 | 人確認 |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## 未実施事項

- AST-SF-PSE: status=planned
- AST-SF-RADIO: status=planned

> Evidence Itemが0件またはAssessment Resultがnot_performedの場合、適合・認証・市場投入承認を意味しません。
