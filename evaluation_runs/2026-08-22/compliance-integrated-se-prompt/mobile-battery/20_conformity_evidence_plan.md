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
| EVR-MB-001 | MBREQ-0001<br>MBREQ-0002 | test_report | 対象構成を識別できる<br>互換性集合と状態定義の版を識別できる<br>入力条件、観測値、合否候補を記録する | true | first_party | planned |
| EVR-MB-002 | MBREQ-0007 | review_record | 損傷判定例を識別できる<br>隔離、再使用防止、引渡し責任を記録する | true | independent_internal | planned |
| EVR-MB-003 | OBL-MB-001<br>MBREQ-0003<br>MBREQ-0004<br>MBREQ-0005<br>MBREQ-0006 | test_report | 対象構成、セル・電池型式および適用基準版を識別できる<br>過充電、過放電、出力異常および温度条件の試験境界を記録する<br>測定値、合否基準、結果および異常を記録する<br>試験方法の由来を識別できる | true | unknown | planned |
| EVR-MB-004 | OBL-MB-002<br>PROC-MB-PSE-INSPECTION | inspection_record | 対象構成、検査日および検査実施者を識別できる<br>現行施行規則で確認した検査項目と結果を記録する<br>現行法令で確認した保存期間と保存責任を記録する | true | first_party | planned |
| EVR-MB-005 | OBL-MB-003<br>MBREQ-0008<br>DOC-MB-PSE-MARKING | inspection_record | 対象分類と義務主体の確認記録を参照できる<br>承認済み表示仕様の版を識別できる<br>対象構成の表示内容、位置および耐久方法を記録する | true | independent_internal | planned |
| EVR-MB-006 | OBL-MB-004<br>OBL-MB-005<br>OBL-MB-006<br>MBREQ-0009<br>MBREQ-0010<br>MBREQ-0011<br>DOC-MB-AIR-QUANTITY-CAPACITY<br>DOC-MB-AIR-CHARGING-PROHIBITION<br>DOC-MB-AIR-POWERING-AVOIDANCE | review_record | 定格Whの根拠を参照できる<br>2026年4月24日適用ルールと航空会社追加条件の確認日を記録する<br>取扱情報の対象市場、版および承認者を識別できる<br>法定の機内充電禁止と非法定の給電回避推奨を区別し、APP-MB-004の組織採用判断を記録する | true | independent_internal | planned |
| EVR-MB-007 | OBL-MB-007<br>SUP-MB-UN38-TEST-SUMMARY | supplier_declaration | セルまたは電池型式と対象製品構成の対応を識別できる<br>製造時点が2003年6月30日後であること、または対象外となる根拠を識別できる<br>機器または回路基板へ組み込まれたボタン電池の例外該当性を識別できる<br>試験報告識別子、試験所、試験日、試験結果および参照したManual版を識別できる<br>署名者または発行責任者を識別できる | true | unknown | planned |

## 存在を確認した証拠（Evidence Item）

| ID | EVR | 構成 | 版 | 検証状態 | 有効性 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 評価活動候補 / Assessment Result / Findingと是正

| Activity | 構成 | 状態 | Result | Outcome | Finding | 有効性 | 人確認 |
|---|---|---|---|---|---|---|---|
| AST-MB-001 | CFG-MB-CANDIDATE | candidate | ASR-MB-001 | not_performed | — | active | pending |
| AST-MB-002 | CFG-MB-CANDIDATE | candidate | ASR-MB-002 | not_performed | — | active | pending |
| AST-MB-003 | CFG-MB-CANDIDATE | candidate | ASR-MB-003 | not_performed | — | active | pending |
| AST-MB-004 | CFG-MB-CANDIDATE | candidate | ASR-MB-004 | not_performed | — | active | pending |
| AST-MB-005 | CFG-MB-CANDIDATE | candidate | ASR-MB-005 | not_performed | — | active | pending |

## Attestation

| ID | Scheme | Result | 構成 | 状態 | 有効性 | 人確認 |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## 未実施事項

- AST-MB-001: status=candidate
- AST-MB-002: status=candidate
- AST-MB-003: status=candidate
- AST-MB-004: status=candidate
- AST-MB-005: status=candidate

> Evidence Itemが0件またはAssessment Resultがnot_performedの場合、適合・認証・市場投入承認を意味しません。
