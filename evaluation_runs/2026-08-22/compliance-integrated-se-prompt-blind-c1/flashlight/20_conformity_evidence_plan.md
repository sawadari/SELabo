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
| EVR-SE-0001 | REQ-0001 | test_report | 対象構成<br>操作入力<br>観測状態 | true | first_party | planned |
| EVR-SE-0002 | REQ-0002 | test_report | 対象構成<br>電池状態<br>通知開始 | true | first_party | planned |
| EVR-SE-0003 | REQ-0003 | test_report | 対象構成<br>通知時点<br>光出力履歴<br>停止原因 | true | first_party | planned |
| EVR-DENAN-0001 | OBL-DENAN-0001<br>REQ-0004 | traceability_report | 対象区分<br>技術基準と版<br>対象構成<br>項目別判定<br>根拠参照 | true | unknown | planned |
| EVR-CSPSA-0001 | OBL-CSPSA-0001<br>PTGT-0001<br>PTGT-0002 | audit_record | 対象製品<br>事故認知日<br>該当性判断<br>報告日<br>提出内容 | true | unknown | planned |

## 存在を確認した証拠（Evidence Item）

| ID | EVR | 構成 | 版 | 検証状態 | 有効性 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 評価活動候補 / Assessment Result / Findingと是正

| Activity | 構成 | 状態 | Result | Outcome | Finding | 有効性 | 人確認 |
|---|---|---|---|---|---|---|---|
| AST-DENAN-0001 | CFG-0001 | candidate | ASR-DENAN-0001 | not_performed | — | active | pending |
| AST-CSPSA-0001 | CFG-0001 | candidate | ASR-CSPSA-0001 | not_performed | — | active | pending |

## Attestation

| ID | Scheme | Result | 構成 | 状態 | 有効性 | 人確認 |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## 未実施事項

- AST-DENAN-0001: status=candidate
- AST-CSPSA-0001: status=candidate

> Evidence Itemが0件またはAssessment Resultがnot_performedの場合、適合・認証・市場投入承認を意味しません。
