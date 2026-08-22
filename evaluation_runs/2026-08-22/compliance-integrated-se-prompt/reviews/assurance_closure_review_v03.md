# v0.3 Assurance Closure Review

## 結論

v0.3 source patchは、初回Assurance Reviewの8対象Findingのうち3件を`closed`、5件を`partially_closed`とした。3製品の現データは引き続き、EvidenceItem 0、Attestation 0、全Assessment Result `not_performed`を正しく保持しており、Schema・意味検査・Trace CSV整合もPASSした。

ただし、新規High Finding `ASR-V03-FND-011`を検出した。現行の正例回帰モデルは、Applicability Assessmentが`uncertain`、Obligationが`candidate`のままでも`assurance_outcome: conforming`をSchema・意味検査ともエラー0件で通過する。適用性を人が確定していない製品を製品Assuranceの`conforming`へ昇格できるため、v0.3のAssurance Closure Gateは`revise`とする。

## 対象

- `schemas/compliance_se_model.schema.json` v0.3.0
- `scripts/validate_candidate.py`
- `scripts/test_assurance_semantics.py`
- `schemas/assurance_fixture.schema.json`
- `examples/assurance_inconclusive_fixture.json`
- `examples/evidence/synthetic_thermal_test_report.json`
- 3製品の`candidate_model.json`、`evaluation.md`、`09_traceability.csv`
- 初回`reviews/assurance_review.md`

モデル本体、Schema、validator、fixtureは変更せず、本Closure Reviewだけを追加した。

## 実行結果

| 検査 | 結果 |
|---|---|
| Assurance意味回帰 | `PASS assurance semantic regression cases=7` |
| 合成Assurance fixture | `PASS`、artifact SHA-256一致、`inconclusive`、`active → stale` |
| スマート扇風機v0.3 | `PASS`、87 ID、103 Trace |
| 懐中電灯v0.3 | `PASS`、67 ID、77 Trace |
| モバイルバッテリーv0.3 | `PASS`、125 ID、172 Trace |
| 3製品CSV再導出比較 | 3/3 `exact_match: true` |

この機械PASSは構造と実装済み意味規則への適合を示す。法的適用、製品適合または認証取得を示さない。

## 初回Finding Closure判定

| Finding | 判定 | v0.3で確認した修正 | 残件 |
|---|---|---|---|
| `ASR-FND-001` モデル品質とAssurance結果の混在 | `closed` | `model_quality_result`、`assurance_outcome`、`not_a_compliance_approval`を分離。3製品は`assurance_outcome: not_performed` | なし |
| `ASR-FND-002` Evidence→Assessment Result成立条件 | `closed` | AST完了、義務範囲、同一構成、計画EVR充足、reviewed/active/artifact_verified Evidence、評価者・日時、独立性を意味検査 | artifactの実体検証範囲はFND-004/007で扱う |
| `ASR-FND-003` issued Attestation成立条件 | `partially_closed` | Scheme、issuer、ASR参照解決、active conforming、同一構成、Scheme EVR充足を意味検査。非適合結果からのissued負例はPASS | issuerとScheme decision authorityの一致、object解決、Scheme obligation網羅、発行Decision recordを未検査 |
| `ASR-FND-004` 版付き構成・責任主体正本 | `partially_closed` | `configurations[]`と`parties_or_roles[]`を追加し、scope/EVI/AST/ASR/ATT参照を解決。別構成Evidence負例はPASS | definitive outcomeでも構成のversion、baseline、locator、hash、active状態、およびassessor/issuerの`confirmed`・権限状態を必須にしていない |
| `ASR-FND-005` 失効・変更影響伝播 | `partially_closed` | Source版確認状態、ASR/ATT有効期間・状態・失効理由を追加。stale Evidenceと未確認Source版をdefinitive outcomeで拒否。fixtureで`active → stale`を確認 | `valid_to`経過判定、ATT statusとvalidity整合、Source状態語彙の`stale`不一致、影響対象の自動列挙を未実装 |
| `ASR-FND-006` inconclusiveとEvidence充足境界 | `partially_closed` | performed outcomeに完了AST・評価者・日時を要求。空のinconclusiveを拒否。definitive outcomeのEVR充足・独立性を検査 | EVRの受入基準、対象構成版、適用期間、個別充足判定を型付きで保持していない |
| `ASR-FND-007` 後段Assurance分岐の試験 | `partially_closed` | hash検証付きinconclusive/stale fixture、conforming正例、7負例を追加 | issued正例、nonconforming正例、expired/withdrawn/suspended、期限経過、Schemaと意味検査を一体化した負例、製品出力20を未試験 |
| `ASR-FND-010` 製品GateとReviewer Gate分離 | `closed` | generator/compliance/se/assurance/meta_judgeを別フィールド化。3製品はgenerator=`pass`、独立3役とMeta-Judge=`revise`。評価文も初回Generator GateとJ1を分離 | 再レビュー結果の反映は本Closure Review後の運用作業 |

補足として、今回の指定範囲外だった`ASR-FND-008`は、モバイルバッテリーの版未確認Sourceを`status: unknown`かつ`applicability_version_state: unconfirmed`へ変更しており、`closed`相当である。`ASR-FND-009`も、懐中電灯評価をProcess投影2、`no_projection: 0`へ同期しており、`closed`相当である。

## 7負例回帰の評価

| # | 負例 | 期待した拒否 | 結果 |
|---:|---|---|---|
| 1 | 未完了Assessment Activity | performed outcomeを拒否 | `PASS` |
| 2 | 別構成Evidence | configuration mismatchを拒否 | `PASS` |
| 3 | stale Evidence | definitive outcomeを拒否 | `PASS` |
| 4 | `reference_only` artifact | definitive outcomeを拒否 | `PASS` |
| 5 | 未確認Source版 | definitive outcomeを拒否 | `PASS` |
| 6 | EvidenceもFindingもない`inconclusive` | 空のinconclusiveを拒否 | `PASS` |
| 7 | `nonconforming`結果から`issued` | Attestation発行を拒否 | `PASS` |

7件はいずれも、意図したエラーメッセージを`semantic_errors()`から検出している。単に「何らかのエラーがあった」ことをPASSとしていない点は妥当である。

ただし、`test_assurance_semantics.py`は`semantic_errors()`を直接呼び、各caseのJSON Schema検証は実行していない。正例モデルは別途Closure ReviewでSchemaエラー0件を確認したが、今後は回帰runner内でも「正例はSchema+意味ともPASS、負例はSchema適合後に狙った意味規則でFAIL」を確認する方がよい。

## Gate分離の妥当性

3製品のv0.3 summaryは、次を明示的に分離している。

- `model_quality_result: pass_with_provisional_assumption`
- `assurance_outcome: not_performed`
- `not_a_compliance_approval: true`
- `reviewer_gates.generator: pass`
- `reviewer_gates.compliance/se/assurance/meta_judge: revise`

この表現は「Generator内の構造的レビュー可能性」と「独立Reviewerの未承認」を機械可読に区別し、初回`ASR-FND-001`と`ASR-FND-010`のFalse Pass経路を閉じている。3製品の評価文も同じ境界へ更新されている。

本Closure ReviewはAssurance source patchを`revise`と判定するため、`reviewer_gates.assurance`と`meta_judge`を現時点で`pass`へ変更してはならない。

## 新規High Finding

### ASR-V03-FND-011：未確定適用性から`conforming`へ昇格できる

- 重大度：`high`
- 状態：`open`
- 影響：v0.3 Schema、validator、Assurance正例回帰、将来の3製品C2/C3評価
- 根拠：`test_assurance_semantics.py`の`positive_model()`はSourceを`active`かつ版確認済みにし、AST/EVI/ASRを整えるが、代表モデルのApplicability Assessment `APP-0001`は`decision: uncertain`、`human_confirmation_required: true`のままである。Obligation `OBL-0001`も`compliance_status: candidate`のままである。それでも合成Schemaエラー0件、`semantic_errors: []`、`assurance_outcome: conforming`となり、正例回帰がPASSする。
- 影響：法規が対象製品に適用されるか人が決定していない状態でも、製品Assuranceを`conforming`にできる。FND-003の残件と組み合わさると、未確定適用性に基づくAttestation発行へ進み得る。
- 最小修正：Applicability Assessmentへ候補生成者とは別の`human_confirmation_state`と確認者・確認日時を追加する。`conforming`および`issued`では、対象Obligationが参照する全Applicability Assessmentについて、`decision`が`applicable`または`partially_applicable`、人確認済み、評価構成と市場が一致することを意味検査する。`uncertain`または未確認の間は`assurance_outcome`を`not_performed`または`inconclusive`に限定する。
- 必須回帰：現行positive modelの`uncertain`状態を負例化してFAILさせ、正例では適用性を人確認済み`applicable`へ変更してから`conforming`を許可する。

## 残存リスクの詳細

### FND-003残件：発行権限と対象の拘束

存在する`PARTY/ROLE`なら、`status: candidate`や`verification_status: ai_candidate`でもissuerにできる。Conformity Schemeの`decision_authority_ref`とAttestation issuerの一致、`object_ref`の解決、Scheme obligation_refsがASRで網羅されることも検査しない。非適合結果から直接発行する経路は閉じたが、権限のない候補ロールによるFalse Certification Claimはまだ防げない。

### FND-004残件：候補構成からのdefinitive outcome

3製品の構成台帳は正しく「版未確認・outside baseline・artifact/hashなし」の候補として登録されている。現3製品は`not_performed`なので問題ない。しかしvalidatorは、同じ状態の構成を使う`conforming`正例を拒否しない。definitive outcomeでは少なくとも構成がactive、版特定済み、対象範囲確認済みであることをGateにすべきである。

### FND-005残件：時間による失効

Schemaへ`valid_to`を追加したが、validatorは現在時刻または評価基準日に対する満了を検査しない。過去日を`valid_to`に持つactive conforming ASRまたはissued ATTも通り得る。`expired` / `withdrawn` / `suspended`と`validity_state`・`invalidation_reason`の整合も回帰対象にする必要がある。

## 製品別Closure判定

| 製品 | 現モデルの安全な空証拠境界 | v0.3 Closure判定 | 理由 |
|---|---|---|---|
| スマート扇風機 | `pass` | `revise` | Source patchは機械PASSだが、APP 3/3 uncertainでありFND-011修正前にdefinitive outcomeを許可できない |
| 懐中電灯 | `pass` | `revise` | Source patchは機械PASSだが、APP 2/2 uncertain。FND-011と残存Attestation/構成Gateが未解決 |
| モバイルバッテリー | `pass` | `revise` | Source patchは機械PASSだが、APP 3/3 uncertain。版状態修正は妥当だがdefinitive outcome Gateは未完了 |

## 最終Gate

- v0.3 Assurance source patch：`revise`
- 3製品の現在のAssurance outcome：`not_performed`のまま妥当
- 3製品の正式適合・認証・市場投入Gate：`not_authorized`
- `reviewer_gates.assurance`：`revise`を維持
- `reviewer_gates.meta_judge`：少なくともFND-011修正と再レビュー完了まで`revise`を維持

次の最優先修正はFND-011である。その後、FND-003/004/005の残存Highリスクを閉じ、issued・expiredを含むSchema一体型回帰を追加して再Closure Reviewを行う。
