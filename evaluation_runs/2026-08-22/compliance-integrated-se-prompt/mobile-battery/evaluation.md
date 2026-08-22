# C1評価：モバイルバッテリー

## 結論

Generator内の初回判定は`reviewable_40_candidate`だったが、独立J1はCompliance・SE・Assuranceとも`revise`である。v0.3修正後のMeta-Judge Gateも再レビュー完了までは`revise`とする。

ただし、これは設計承認、法的適用判断、PSE認証取得、規格適合、航空輸送可否の判定ではない。製品仕様、事業者役割、採用基準および実在証拠がないため、適用性4件はすべて`uncertain`、EvidenceItemは0件、AssessmentResult 5件はすべて`not_performed`とした。

## v0.3 High Finding修正

- 6/6 NeedへValidationCase候補を追加し、Requirement VerificationとStakeholder価値のValidationを分離した。
- `CFG-MB-CANDIDATE`と5つの責任ロール候補を正本へ登録した。
- 法第8条の一般義務から4つの具体的保護要求への直接Compliance導出を除き、技術基準選定のAssurance Requirementへ変更した。製品保護要求は安全Need由来として維持した。
- 損傷品隔離行動を物理製品構造から分離し、運用プロセス構造へ再配分した。
- 航空の個数・容量、機内充電禁止、機内での他機器への給電回避推奨を別要求へ分割し、法定禁止と非法定の安全要請を区別した。
- 報道発表と告示候補、UN ManualとModel Regulations候補を分離した。
- UN Model RegulationsをRevision 24（2025）の`recommendation`として登録し、2.9.4(g)の主体をセル・電池製造者および後続流通業者候補へ限定した。
- 温度監視の対象部位と入出力遮断経路をdesign traceで一意化し、航空旅客運用の3要求をBehavior、運用Structure、Verificationへ接続した。
- v0.3.1 Schema・意味検証は`PASS`（146 ID、197 Trace）。独立再レビュー完了前のため総合Gateは`revise`のままである。

## 評価メタデータ

|項目|内容|
|---|---|
|run_id|EVAL-2026-08-22-MB-C1-01|
|条件|C1：`hierarchical-se-prompt` + `compliance-integrated-se-prompt`|
|対象|`candidate_model.json`|
|評価日|2026-08-22|
|評価Tier|J0（生成担当内の規則検査）。B0のJ1独立Review Findingを入力として再利用|
|基準|`17_FORTY_POINT_GATE.md`、`04_COMPLIANCE_QUALITY_RULES.md`、`05_EXPERIMENT_PLAN.md`|
|正式判定|未実施。専門家・法務・認証機関・規制当局による確認が必要|

## 正式一次情報と確認範囲

- 経済産業省の[対象非対象解釈例一覧](https://www.meti.go.jp/policy/consumer/seian/denan/subject01.html)で、リチウムイオン蓄電池の対象条件として単電池1個当たり400 Wh/L以上と用途除外が示されていることを確認した。対象構成の値と用途は未確認である。
- 経済産業省の[電気用品安全法 法令業務実施ガイド](https://www.meti.go.jp/policy/consumer/seian/denan/tetsuduki_annai/guide/denan_guide.pdf)および[制度概要](https://www.meti.go.jp/policy/consumer/seian/denan/act_outline.html)で、法第8条の技術基準適合・検査記録、法第10条・第27条の表示・販売制限の説明を確認した。ガイドの版表示は抽出できなかったため版は未確認とした。法令正本は[e-Govの電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234)で人が再確認する必要がある。
- 国土交通省の[告示別表第18](https://www.mlit.go.jp/common/001388681.pdf)で、2個まで、各160 Wh以下、機内充電禁止を確認した。[航空局からのお知らせNo.111](https://www.mlit.go.jp/koku/content/001998054.pdf)では、他機器への給電回避は法律に基づく禁止ではない安全要請として分離した。航空旅客利用、定格Wh、航空会社追加条件は未確認である。
- UNECEの[UN Manual of Tests and Criteria Rev.8およびAmendment 1](https://unece.org/transport/dangerous-goods/rev8-files)と[UN Model Regulations Revision 24](https://unece.org/sites/default/files/2025-09/ST_SG_AC10_1_Rev24e_Vol%20I_1.pdf)を分離し、Manual 38.3.5とModel Regulations 2.9.4(g)を対応付けた。対象輸送モードに採用される版と法的取込みは未確認である。

規格本文の長文転載は行わず、識別子、位置、要約候補だけを保存した。

## C-品質規則

|規則|結果|根拠|
|---|---|---|
|C-SRC-01|`pass_with_provisional_assumption`|Authority、Source、公式URL、取得状態を分離。METIガイド版は未確認|
|C-SRC-02|`pass`|8 ProvisionにSourceと公式ページ内位置があり、未取得引用を作成していない|
|C-SRC-03|`pass`|Provision、NormativeStatement、Applicability、Obligationを別オブジェクト化|
|C-APP-01|`pass_with_provisional_assumption`|法域、市場、分類、用途、構成、段階、評価日を記録。不明点は制約に明示|
|C-APP-02|`pass`|`source_type`と`binding_basis`を分離。UN 38.3の拘束根拠は`unknown`|
|C-APP-03|`pass`|Applicability 4件は全件`uncertain`、`human_confirmation_state=pending`かつ`human_confirmation_required=true`|
|C-APP-04|`pass`|市場、構成、版、輸送条件の変更トリガーを記録|
|C-OBL-01|`pass`|7 ObligationがNormativeStatementとApplicabilityへ戻る|
|C-EPR-01|`pass`|7/7 ObligationにEngineeringProjectionあり|
|C-EPR-02|`pass`|Product、Process、Documentation、Supplier、Evidenceを分離|
|C-EPR-03|`pass`|全Requirementに`derivation_sources`あり。Compliance由来はOBL/EPRへ戻る|
|C-EPR-04|`pass`|Authority等をSysML Requirementへ直接投影していない|
|C-EVI-01|`pass`|EvidenceRequirement 7件とEvidenceItem 0件を分離|
|C-EVI-02|`not_applicable`|実在EvidenceItemなし|
|C-EVI-03|`pass`|mandatory/prohibition Obligation 6/6がEvidenceRequirementへ到達し、recommendation 1件も証拠要求へ追跡できる|
|C-AST-01|`pass`|製品試験、検査、文書ReviewをVerificationCaseと区別|
|C-ASR-01|`pass`|5結果は全件`not_performed`。適合・不適合を主張していない|
|C-ATT-01|`not_applicable`|Attestationなし|
|C-CHG-01|`not_applicable`|stale/superseded Sourceなし。変更トリガーは登録済み|
|C-MAP-01|`not_applicable`|規格間同等性Mappingを主張していない|

Compliance総合結果は`pass_with_provisional_assumption`である。主要失敗条件に該当する、架空条項、AI単独の適用・適合決定、Process義務の製品挙動化、架空EvidenceまたはFalse Certification Claimは検出しなかった。

## 40点Gate

|評価軸|結果|計算|
|---|---|---:|
|Stakeholder → Need|`sufficient`|6/6 NeedでStakeholder参照が解決（100%）|
|Need → Requirement|`sufficient`|主要Need 6/6が1件以上の主要Requirementへ到達（100%）|
|Requirement → Behavior / Structure|`sufficient`|Requirement 11/11がBehaviorまたはStructureへ到達（100%）|
|Requirement → V&V候補|`sufficient`|Requirement 11/11がVerificationCaseへ到達（100%）|
|主要要素のorigin/status|`sufficient`|Stakeholder、Need、Requirement、Behavior、Structure、VerificationCaseの必須由来・状態属性100%|
|1要求1義務|`sufficient`|11/11。数値境界は創作せず「承認済み境界」参照として人確認へ送付し、航空旅客の義務・禁止・推奨も別要求とした|
|重大Findingの確認方法|`sufficient`|下記4項目すべてに確認者・必要情報・再評価トリガーあり|
|未管理の重大矛盾|`sufficient`|0件|
|過剰詳細化|`sufficient`|部品型番、正確な閾値・公差、認証済み状態の創作なし|

Hard Blockerは0件と判定する。不確実な法規適用を隠さずCompliance chainと人確認へ送っているため、重要評価軸の`missing`にはしない。

### 人が確認する重大事項

1. 電池化学系、セル・パック構成、単電池の体積エネルギー密度および用途除外を確認し、電安法上の対象分類を決定する。
2. 製造・輸入・販売主体、販売経路、販売時点で有効な技術基準と検査・表示義務を法規担当が確認する。
3. 過充電、過放電、短絡、過電流、異常電圧、温度保護の境界値と試験方法を、電池仕様およびハザード分析に基づいて安全担当が承認する。
4. 定格Wh、航空旅客利用、輸送モード、運送事業者条件、UN 38.3採用版および実在する試験要約を物流・法規担当が確認する。

## B0比較（初回C1-remediated生成時）

|指標|B0（2026-08-21）|C1（本実行）|変化|
|---|---:|---:|---|
|Gate|`below_reviewable`|`reviewable_40_candidate`|Hard Blockerを修復|
|使用可能なNeed → Requirement Trace|0/5（0%）|6/6（100%）|未定義MB-NEED IDを独立Needへ修復|
|Requirement → Behavior / Structure|3/5（60%）|11/11（100%）|充電・放電・温度・損傷・表示・航空旅客責任を分離|
|Requirement → V&V候補|0/5（0%）|11/11（100%）|境界値の承認前提と必要Evidenceを明示|
|安全・法規・輸送境界|`missing`|`sufficient`（候補）|Source→Applicability→Obligation→Projection→Evidenceを追加|
|Hard Blocker|2件|0件|Need欠落と電池安全軸欠落を解消|
|EvidenceRequirement / EvidenceItem|区別なし|7件 / 0件|将来必要な証拠と実在証拠を分離|
|正式適合・認証主張|0件|0件|増加なし|

分母はB0の主要Trace 5行に対し、C1では独立Need 6件・Requirement 11件へ分解したため異なる。比較は行数ではなく、参照解決と意味接続を満たす項目だけを数えた。

## 標準化メトリクス

|項目|値|
|---|---:|
|Authority / Source / Provision|3 / 8 / 9|
|NormativeStatement / Applicability / Obligation|8 / 4 / 7|
|`uncertain` Applicability|4/4（100%）|
|EngineeringProjection|16|
|Product系投影|1（constraint 1）|
|Process系投影|1|
|Assurance系投影|1|
|Operational系投影|3|
|Documentation系投影|4|
|Supplier系投影|1|
|Evidence系投影|5|
|SourceからEvidenceRequirementへ到達するObligation経路|7/7（100%）|
|投影のないObligation|0|
|mandatory/prohibitionだがEvidenceRequirementのないObligation|0|
|EvidenceRequirement / EvidenceItem|7 / 0|
|AssessmentActivity / `not_performed`結果|5 / 5|
|架空EvidenceItem|0|
|False Certification Claim|0|
|人による採用・修正・却下|未実施|
|初稿生成時間・専門家Review時間・SE Review時間|未計測|
|False Pass|人の校正未実施のため判定不能|

## 機械検証

|検査|結果|詳細|
|---|---|---|
|JSON構文|PASS|PowerShell `ConvertFrom-Json -Depth 100`|
|合成Schema|PASS|Python `jsonschema` 4.26.0、Draft 2020-12。元SchemaをRegistryへ登録してCompliance Schemaを評価|
|内部参照整合性|PASS|146 ID、197導出関係。構成・責任ロール・適用性・探索ログを含む未解決参照0件|
|`regulatory_candidate`禁止|PASS|使用0件|
|EvidenceItem実在性|PASS|配列は空|

この検証はJSON構造と候補Traceの整合だけを示す。法的正確性、技術基準適合、PSE表示可否、UN 38.3適合、航空機内持込み可否、安全性または認証取得を示さない。

## v0.2残件修正

Meta Review後、Schema未定義だった独自`projection_targets[]`をv0.2の型付き定義へ移行し、Process、Documentation、Supplierの各対象へ必須のstatement、lifecycle、provenance、人確認状態を追加した。

`validate_candidate.py`による合成Schema・ID参照・投影種別・Evidence到達検査は`PASS`で、型付き直接参照から197関係の[09_traceability.csv](09_traceability.csv)を決定的に生成した。`relations[]`は補助関係専用のため空のままでよい。
