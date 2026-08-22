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
| EVR-FL-SE-01 | FLREQ-0001<br>FLREQ-0008 | test_report | 対象構成<br>操作入力<br>観測照明状態<br>候補合否基準 | true | first_party | planned |
| EVR-FL-SE-02 | FLREQ-0002 | test_report | 対象構成<br>放電条件<br>電池状態<br>通知開始時点 | true | first_party | planned |
| EVR-FL-SE-06 | FLREQ-0006 | test_report | 対象構成<br>通知開始時点<br>消灯時点<br>光出力履歴<br>停止原因 | true | first_party | planned |
| EVR-FL-SE-04 | FLREQ-0004 | test_report | 対象構成<br>監視部位<br>温度履歴<br>状態遷移時刻<br>光出力履歴 | true | unknown | planned |
| EVR-FL-DENAN-TECH-01 | OBL-FL-DENAN-01 | traceability_report | 人が確定した対象区分<br>適用技術基準と版<br>対象構成<br>基準項目ごとの判定<br>根拠証拠参照<br>レビュー者とレビュー日 | true | unknown | planned |
| EVR-FL-DENAN-INSPECT-01 | OBL-FL-DENAN-02 | inspection_record | 電気用品の品名と型式区分<br>構造、材質および性能の概要<br>検査年月日と場所<br>検査実施者<br>検査数量<br>検査方法<br>検査結果 | true | first_party | planned |
| EVR-FL-CSPSA-REPORT-01 | OBL-FL-CSPSA-01 | audit_record | 対象製品と型式<br>重大製品事故該当性の判断記録<br>事業者が事故を知った日<br>報告日<br>提出内容または提出先参照<br>責任者レビュー | true | unknown | planned |

## 存在を確認した証拠（Evidence Item）

| ID | EVR | 構成 | 版 | 検証状態 | 有効性 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 評価活動候補 / Assessment Result / Findingと是正

| Activity | 構成 | 状態 | Result | Outcome | Finding | 有効性 | 人確認 |
|---|---|---|---|---|---|---|---|
| AST-FL-DENAN-01 | CFG-FL-01 | candidate | ASR-FL-DENAN-01 | not_performed | — | active | pending |
| AST-FL-CSPSA-01 | CFG-FL-01 | candidate | ASR-FL-CSPSA-01 | not_performed | — | active | pending |

## Attestation

| ID | Scheme | Result | 構成 | 状態 | 有効性 | 人確認 |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## 未実施事項

- AST-FL-DENAN-01: status=candidate
- AST-FL-CSPSA-01: status=candidate

> Evidence Itemが0件またはAssessment Resultがnot_performedの場合、適合・認証・市場投入承認を意味しません。
