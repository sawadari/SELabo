# Conformity and Evidence Plan

## Gate境界

| モデル品質 | Assurance outcome | Compliance approvalではない | Reviewer Gate |
|---|---|---|---|
| pass_with_provisional_assumption | not_performed | true | generator=pass<br>compliance=revise<br>se=revise<br>assurance=revise<br>meta_judge=revise |

## 適合性評価スキーム候補

| ID | 種別 | 所有者 | 決定権者 | 適合対象 | Obligation | 必要Evidence | 独立性 | 出力 |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — |

## 必要な証拠（Evidence Requirement）

| ID | 対象 | 種別 | 必要属性 | 構成必須 | 独立性 | 状態 |
|---|---|---|---|---|---|---|
| EVR-SF-001 | REQ_SF-0001 | inspection_record | 対象構成<br>選択モード<br>表示結果 | true | none | planned |
| EVR-SF-002 | REQ_SF-0002 | test_report | 対象構成<br>危険状態定義<br>停止時間閾値<br>測定結果 | true | unknown | planned |
| EVR-SF-003 | REQ_SF-0003 | test_report | 対象構成<br>音圧測定条件<br>風量測定条件<br>測定結果 | true | none | planned |
| EVR-SF-004 | REQ_SF-0004 | test_report | 対象構成<br>通信切断条件<br>停止操作結果 | true | none | planned |
| EVR-SF-005 | REQ_SF-0005 | test_report | 対象構成<br>通信切断条件<br>再開操作結果 | true | none | planned |
| EVR-SF-006 | REQ_SF-0006 | test_report | 対象構成<br>保守状態定義<br>起動操作結果 | true | none | planned |
| EVR-SF-007 | OBL-SF-002<br>REQ_SF-0007 | test_report | 対象構成<br>高さ設定<br>通常使用状態<br>傾斜方向および角度<br>転倒有無 | true | unknown | planned |
| EVR-SF-008 | OBL-SF-001 | traceability_report | 対象電気用品分類<br>対象構成<br>採用した技術基準および版<br>評価活動および結果への参照<br>責任者および確認日 | true | unknown | planned |
| EVR-SF-009 | OBL-SF-003<br>OBL-SF-004<br>OBL-SF-005<br>OBL-SF-006 | traceability_report | 無線方式および周波数<br>対象モジュール識別<br>免許要否の確認根拠<br>技術基準適合証明または工事設計認証の識別子および管理版<br>CFG-SF-001のHW・SW・アンテナ構成と認証工事設計の照合結果<br>構成差分の処置、再評価要否および変更管理記録<br>表示方法および表示権限の確認結果 | true | unknown | planned |

## 存在を確認した証拠（Evidence Item）

| ID | EVR | 構成 | 版 | 検証状態 | 有効性 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 評価活動候補 / Assessment Result / Findingと是正

| Activity | 構成 | 状態 | Result | Outcome | Finding | 有効性 | 人確認 |
|---|---|---|---|---|---|---|---|
| AST-SF-001 | CFG-SF-001 | planned | ASR-SF-001 | not_performed | — | active | pending |
| AST-SF-002 | CFG-SF-001 | planned | ASR-SF-002 | not_performed | — | active | pending |

## Attestation

| ID | Scheme | Result | 構成 | 状態 | 有効性 | 人確認 |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## 未実施事項

- AST-SF-001: status=planned
- AST-SF-002: status=planned

> Evidence Itemが0件またはAssessment Resultがnot_performedの場合、適合・認証・市場投入承認を意味しません。
