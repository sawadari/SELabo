# v0.3.1 Independent Assurance Closure Review

## 結論

v0.3.1のAssurance source-patch Closure Gateは`pass`とする。前回High `ASR-V03-FND-011`と、この再レビュー中に独立再現したdefinitive outcome／issued Attestationの全High bypassは、Schema、意味検査、正例4件・負例65件の統合回帰で遮断された。新規Highは0件である。

3製品のモデルは、Applicability、Source版、Obligation、構成、Evidenceの未確定状態を保持し、全Assessment Resultを`not_performed`、Attestationを0件としている。このデータ境界は3製品とも`pass`である。ただし、これは製品適合のPassではない。実在Evidence、正式な適用性判断、法務・認証専門家レビューが未実施であるため、製品の適合・認証・市場投入Gateは3製品とも`revise / not_authorized`、`assurance_outcome`は`not_performed`のままとする。

残るMediumは、外部URL原典の本文をローカルartifactと同じ方法では暗号学的に取得検証していないことと、export checkerがoutput contractから独立していないことである。いずれも今回3製品の安全側状態をFalse Passへ変えないが、実Evidenceを使うC2前に対処または統制受入が必要である。

別runのstrict-blind評価でCompliance J1が`fail / revise`となった事実は、生成時の法規探索・適用性品質に関する独立した実験結果である。本レビューの対象であるv0.3.1 Assurance package source-patchの成立性とは混同しない。strict-blind製品の総合Gateは`revise`を維持しつつ、共通Assurance source-patch Closureは下記の機械検証結果に基づき`pass`とする。

## 対象

- `schemas/compliance_se_model.schema.json`
- `scripts/validate_candidate.py`
- `scripts/test_assurance_semantics.py`
- `scripts/validate_assurance_fixture.py`
- `scripts/export_compliance_views.py`
- `examples/representative_model.json`
- `examples/assurance_inconclusive_fixture.json`
- 合成Evidence artifact
- `04_COMPLIANCE_QUALITY_RULES.md`
- `09_TRACEABILITY_CANONICAL_RULES.md`
- 3製品の`candidate_model.json`、`evaluation.md`、`09_traceability.csv`、17〜21出力
- 前回`reviews/assurance_review.md`、`reviews/assurance_closure_review_v03.md`

モデル本体と実験ファイルは編集していない。本レビュー文書だけを更新した。

## 最終実行結果

| 検査 | 結果 |
|---|---|
| Assurance統合回帰 | `PASS assurance integrated regression positives=4 negatives=65` |
| 合成Assurance fixture | `PASS`、artifact SHA-256一致、`inconclusive`、`active → stale` |
| スマート扇風機validator | `PASS`、98 ID、132 Trace |
| 懐中電灯validator | `PASS`、75 ID、88 Trace |
| モバイルバッテリーvalidator | `PASS`、146 ID、197 Trace |
| 3製品`09_traceability.csv`再導出比較 | 132 / 88 / 197行、3/3 `exact=true`、未解決参照0、重複relation ID 0 |
| 追加成果物17〜21 `export --check` | 3/3製品、各5ファイル`PASS checked files=5` |
| v0.3.1版識別 | Schema const、profile、contract、代表モデル、3製品モデルが`0.3.1` |
| package manifest | `version: 0.3.1`、manifest自身と`__pycache__`を除くpackage全19ファイルについて、記載19件／現物19件、size・SHA-256一致、欠落・未記載0件 |

## 3製品の安全側状態

| 製品 | Applicability | Source適用版 | Obligation | 構成 | EVI / ASR / ATT | モデル境界 | 製品適合Gate |
|---|---|---|---|---|---|---|---|
| スマート扇風機 | 3/3 `uncertain`、全件`pending` | 3/3 `unconfirmed` | 6/6 `candidate` | `outside_baseline` | 0 / 2件`not_performed` / 0 | `pass` | `revise / not_authorized` |
| 懐中電灯 | 2/2 `uncertain`、全件`pending` | 6/6 `unconfirmed` | 3/3 `candidate` | `outside_baseline` | 0 / 2件`not_performed` / 0 | `pass` | `revise / not_authorized` |
| モバイルバッテリー | 4/4 `uncertain`、全件`pending` | 8/8 `unconfirmed` | 7/7 `candidate` | `outside_baseline` | 0 / 5件`not_performed` / 0 | `pass` | `revise / not_authorized` |

3製品とも`model_quality_result: pass_with_provisional_assumption`、`assurance_outcome: not_performed`、`not_a_compliance_approval: true`を別フィールドに保持する。Generator、Compliance、SE、Assurance、Meta-Judge Gateも分離され、独立レビュー完了前の値を`revise`へ維持している。モデル品質候補を製品適合または認証取得へ読み替えるFalse Passはない。

## 前回Finding Closure

| Finding | 判定 | 根拠 | 残件 |
|---|---|---|---|
| `ASR-FND-001` 品質とAssurance結果の混同 | `closed` | `model_quality_result`、`assurance_outcome`、`not_a_compliance_approval`を分離 | なし |
| `ASR-FND-002` EVI→AST→ASR成立条件 | `closed` | 同一completed AST、同一構成、`produced_at <= verified_at <= assessed_at`、reviewed/active/artifact_verified、実在local artifactとSHA-256一致、権限者、EVR属性別`satisfied`を要求 | なし |
| `ASR-FND-003` issued Attestation前提 | `closed` | active conforming ASR、非空Scheme scope、全Obligation/EVR、confirmed Scheme、decision authority、object/output一致、独立性、実在artifact、期限を要求 | なし |
| `ASR-FND-004` 構成・責任主体正本 | `closed` | baselined/active構成、版、locator、SHA-256、権限確認済みverifierと時刻をdefinitive outcomeで要求 | 外部repository artifactは現在definitiveに使用不可という安全側制限 |
| `ASR-FND-005` 失効・変更影響 | `partially_closed` | Source/Provision/ASR/ATTの有効期間、時刻順序、future/expired、不正Format、inactive ATT、EVI staleを検査。fixtureで`active → stale`を確認 | 外部変更の自動監視と依存artifactの有効期限上限伝播は未実装 |
| `ASR-FND-006` inconclusiveとEVR充足 | `closed` | empty inconclusiveを拒否。definitiveではprovided=planned、全EVRの人確認、対象Obligation coverage、evidence type、required property全件の個別判定を要求 | なし |
| `ASR-FND-007` 後段Assurance回帰 | `closed` | Schema+意味検査を統合し、正例4件、負例65件、製品出力、fixtureを同一source patchで実行 | 実製品EvidenceによるC2は実験範囲外 |
| `ASR-FND-010` Reviewer Gate分離 | `closed` | Reviewer別Gateを分離し、Meta-Judge未承認を製品Passへ昇格しない | なし |
| `ASR-V03-FND-011` 未確定Applicabilityからconforming | `closed` | APP決定・権限者・確認時刻、Source/Provision版とverifier、user-confirmed OBL/EVR、全scope coverageを要求。pending/uncertain/not-applicable候補をconforming summaryから除外できない | なし |

## 状態境界の確認

### EvidenceRequirement → EvidenceItem → AssessmentActivity / Result

definitiveな`conforming`または`nonconforming`は次をすべて満たす。

- `assessed_obligation_refs`が1件以上あり、各Obligationがuser-confirmedかつ権限者・確認時刻を持つ。
- 実際に消費したEVRとASTのplanned EVRが一致し、全EVRがuser-confirmedである。
- 各評価対象Obligationを、消費したEVRが直接coverする。
- EvidenceItemは同じcompleted ASTで生成され、同じ構成を参照する。
- Evidence typeがEVRと一致し、`required_properties[]`全件について権限者が`satisfied`を記録する。
- Evidence artifactと構成baselineはローカルに実在し、`sha256:<64 hex>`が実内容と一致する。
- EVI生成、artifact検証、属性判定、ASR評価の時刻順序が成立する。

別のplanned ASTが生成したEvidence、評価後生成Evidence、未確認EVR、planned外EVR、対象Obligationに紐づかないEVR、架空file URI、偽hash、未充足propertyはすべて負例で拒否された。

### `not_performed` / `inconclusive`

3製品はEvidenceItemが0件で、全ASRを`not_performed`へ維持する。合成fixtureは実在artifactがあっても判定材料不足なら`inconclusive`とし、構成変更後にEvidenceを`stale`へ遷移させる。`inconclusive`でEvidenceもFindingも空の状態は拒否する。証拠がない状態をdefinitiveへ昇格する経路はない。

### Source、Provision、Applicability、Obligation

definitive outcomeは、activeで版識別を持つSource、canonical locatorを持つ有効なProvision、双方の権限確認済みverifierと検証時刻を要求する。Applicabilityは`applicable`または`partially_applicable`、権限者のconfirmed状態、確認時刻、構成・市場一致が必要である。Obligationもuser-confirmedかつ`assessed`でなければならない。

さらに、summaryを`conforming`とする場合は、関連Applicabilityがすべて権限者confirmedで、全applicable/partially applicable Obligationがactive conforming ASRによりcoverされる。未確認、`uncertain`、pending、AI候補`not_applicable`、評価漏れObligationを隠してglobal conformingにする経路を負例で拒否した。

### issued Attestation

issued時は次を検査する。

- Scheme owner、decision authority、object、Obligation、EVRの全参照が解決する。
- Schemeがuser-confirmedで、確認者・確認時刻を持ち、Obligation、EVR、assessment methodが非空である。
- 全参照ASRが同一構成のactive conformingで、Scheme全Obligationと全EVRをcoverする。
- Scheme required EVRも全件user-confirmedである。
- issuerがScheme decision authorityと同一で、権限確認済みである。
- ATT objectとScheme object、ATT output kindとScheme output kindが一致する。
- Scheme independenceと根拠AST independenceが一致する。
- Attestation artifactが実在し、version、SHA-256、権限verifier、検証時刻を持つ。
- ASR評価、Scheme確認、発行、artifact検証、validityの時刻順序が成立し、評価基準日で有効である。

owner/object/Obligation/EVRの参照切れ4ケース、空Scheme scope、Scheme未確認EVR、別object、別output kind、誤decision authority、nonconforming result、期限切れ・不正日時・未来発行を含む負例を拒否した。

## 統合回帰の評価

正例4件は`conforming`、`nonconforming`、`issued`、`expired`である。負例65件は、前回要求された主要7ケースを包含し、次のカテゴリを横断する。

- 未完了／別Activity、別構成、stale・未検証・架空・hash不一致Evidence
- 未確認Source/Provision版、未来・失効Source/Provision、権限のないverifier
- uncertain／pending Applicability、権限のない確認者、未来確認
- candidate／空scope／未評価Obligation、global conformingのscope欠落
- candidate／planned外／対象外EVR、type・property・independence不一致
- candidate assessor、未baseline・架空・hash不一致構成
- empty inconclusive、期限切れ・不正日時・時間順序違反ASR
- issued前提、Scheme参照、scope、authority、object、output、independence、artifact、期限の違反

意味負例は先にSchema-validであることを確認してから期待する意味エラーを検査し、Format違反はSchemaまたは意味検査の拒否を確認する。Schemaだけ、または`semantic_errors()`だけを直接試す構造ではなく、実validatorと同じFormatChecker付き統合経路である。

## 再レビュー中に閉じたHigh bypass

| 攻撃経路 | 最終状態 |
|---|---|
| candidate confirmer、自己宣言Source版、AI由来assessed OBL | `closed` |
| Scheme objectと異なる解決済みATT object | `closed` |
| 不正date-time、同日内期限切れ、未来ASR/ATT | `closed` |
| 架空EVI/構成/ATT artifact、偽SHA-256 | `closed` |
| 別の未完了AST生成Evidence、評価後生成Evidence | `closed` |
| planned／未確認／対象外EVRによるdefinitive result | `closed` |
| AI候補Scheme、空Scheme scope、output kindすり替え | `closed` |
| 未確認Provision、未来Applicability確認 | `closed` |
| 空ASR scope、未評価／uncertain Obligationを隠すglobal conforming | `closed` |

## 残存Finding

### ASR-V031-FND-018：外部原典本文の取得真正性は人の検証記録に依存する

- 重大度：`medium`
- 状態：`open / accepted limitation for C1`
- 根拠：SourceとProvisionは権限確認済み`verified_by_ref`と`verified_at`を必須化した。一方、外部URLをローカルEvidenceと同様に取得して本文hashを照合する処理はない。架空のSource識別子・版・URL・Provision locatorでも、確認済みverifierが検証済みと記録すれば機械検査はその人の判断を信頼する。
- 影響：確認者の誤認、取得時本文と後日本文の差、URL差し替えを機械的には検知できない。
- 最小修正：許諾と保存方針の範囲で、取得receipt、取得時刻、最終URL、版識別、content hashまたは署名を別artifactとして保存する。本文保存不可の場合は、公式版IDと取得メタデータを署名付きverification recordへ残し、再取得・再確認期限を定義する。
- Gate影響：現3製品はSource版`unconfirmed`かつ`not_performed`なのでsource-patch Closureを阻害しない。実適合を扱うC2では人の法規レビューと取得証跡を必須にする。

### ASR-V031-FND-017：`export --check`はoutput contractから独立していない

- 重大度：`medium`
- 状態：`open`
- 根拠：`--check`は同じexporterが生成する期待byte列と既存出力を比較する。`03_COMPLIANCE_OUTPUT_EXTENSION.json`のrequired section／required columnを独立に読み、exporter自身の欠落を検知する検査ではない。
- 影響：exporterと成果物が同じ意味項目を欠落した場合、byte一致だけでは検出できない。
- 最小修正：output contractを別入力としてMarkdown sectionとCSV columnを検査し、必須項目を1つ欠く負例を追加する。
- Gate影響：今回の17〜21は3製品とも再生成byteと一致し、Assurance状態も正しく投影しているため非blockingとする。

## 最終Gate

| Gate | 判定 |
|---|---|
| v0.3.1 Assurance source-patch Closure | `pass` |
| 新規High | 0件 |
| 残存Medium | 2件（外部原典取得真正性、export contract独立検査） |
| スマート扇風機 Assuranceモデル境界 | `pass` |
| 懐中電灯 Assuranceモデル境界 | `pass` |
| モバイルバッテリー Assuranceモデル境界 | `pass` |
| 3製品の実適合・認証・表示・市場投入 | `revise / not_authorized` |
| 3製品`assurance_outcome` | `not_performed`を維持 |
| Meta-Judge総合 | Compliance/SE残件、人のApplicability確認、実Evidence評価が完了するまで`revise` |

次の段階は、法規担当者がSource版とApplicabilityを確認し、対象構成baselineと実在Evidenceを準備したC2である。C2ではFND-018の取得証跡を必須入力とし、同じvalidatorでdefinitive outcomeとAttestationの負例回帰を再実行する。
