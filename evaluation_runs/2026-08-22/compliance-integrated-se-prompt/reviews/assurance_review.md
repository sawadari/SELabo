# 独立Assurance Review：3製品横断

## 結論

独立Assurance Reviewerの判定は、スマート扇風機、懐中電灯、モバイルバッテリーの3製品すべて`revise`である。

現在の候補データは、実在証拠がない状態で`EvidenceItem: 0`、`Attestation: 0`を保ち、9件のAssessment Resultをすべて`not_performed`としている。この「証拠がない状態を適合へ昇格しない」分岐自体は3製品とも`pass`であり、架空証拠、適合、認証取得の明示的な主張は検出しなかった。

ただし、3モデルは同時に`compliance.summary.overall_result: pass_with_provisional_assumption`を出力している。これはモデル品質の評価と製品のAssurance状態を一つのフィールドへ重ね、機械利用時にFalse Passとなり得る。また、EvidenceItemを将来追加した後の状態遷移、対象構成、版、証拠の有効性、Attestation発行条件をSchemaと意味検査が十分に拘束していない。したがって、現在の安全な空証拠状態を確認しただけでは、Compliance/Assurance Gateを通過させられない。

## レビュー対象と実施範囲

- `schemas/compliance_se_model.schema.json` v0.2.0
- `04_COMPLIANCE_QUALITY_RULES.md`
- `09_TRACEABILITY_CANONICAL_RULES.md`
- 3製品の`candidate_model.json`、`evaluation.md`、生成済み`09_traceability.csv`
- `scripts/validate_candidate.py`による合成Schema・意味検査

法規の法的解釈、実在製品の試験、証拠artifactの取得、認証機関の判断は実施していない。本レビューはAssurance意味境界とFalse Pass耐性の独立レビューである。

## 横断サマリ

| 製品 | EVR | EVI | AST | ASR | ATT | 現在の証拠状態 | 独立判定 |
|---|---:|---:|---:|---:|---:|---|---|
| スマート扇風機 | 9 | 0 | 2 | 2 | 0 | 2件とも`not_performed` | `revise` |
| 懐中電灯 | 7 | 0 | 2 | 2 | 0 | 2件とも`not_performed` | `revise` |
| モバイルバッテリー | 7 | 0 | 5 | 5 | 0 | 5件とも`not_performed` | `revise` |

3モデルは現行validatorでPASSした。

| 製品 | ID数 | 生成Trace数 |
|---|---:|---:|
| スマート扇風機 | 72 | 89 |
| 懐中電灯 | 59 | 72 |
| モバイルバッテリー | 103 | 150 |

このPASSは構造、投影先、主要Traceの参照解決を示す。下記FindingのAssurance状態遷移やAttestation成立性までを検証した結果ではない。

## Finding

### ASR-FND-001：モデル品質とAssurance結果が同じ`overall_result`に混在する

- 重大度：`high`
- 影響：3製品共通
- 根拠：全Assessment Resultが`not_performed`で、EvidenceItemとAttestationが0件である一方、全モデルの`compliance.summary.overall_result`は`pass_with_provisional_assumption`である。評価文には非適合主張の注意書きがあるが、JSONフィールド名だけでは「モデル品質のPass」と「製品適合のPass」を区別できない。
- 影響：API、表計算、ダッシュボード等が`overall_result`だけを読むと、証拠未評価の製品をCompliance Passとして扱うFalse Passが起こり得る。
- 最小修正：`model_quality_result`と`assurance_outcome`を分離する。現3モデルの`assurance_outcome`は`not_performed`とし、`pass_with_provisional_assumption`は構造・追跡品質のフィールドにだけ保存する。40点Gateにも`not_a_compliance_approval: true`相当の機械可読フラグを追加する。

### ASR-FND-002：EvidenceからAssessment Resultまでの成立条件を意味検査していない

- 重大度：`high`
- 影響：3製品共通
- 根拠：Schemaは`conforming` / `nonconforming`にEvidenceItem、評価日時、評価者、人確認を要求するが、参照先AssessmentActivityが`completed`か、EvidenceItemが`reviewed`かつ`active`か、`artifact_verified`か、計画EVRを満たすか、対象Obligationと構成が一致するかを拘束しない。validatorも投影とTrace参照は検査するが、これらの状態整合を検査しない。
- 影響：未完了Activity、別構成のEvidence、未レビューまたは参照だけのartifactから`conforming`を作成してもSchema PASSになり得る。
- 最小修正：意味検査へ、ASR→AST存在、AST=`completed`、ASR義務⊆AST義務、ASR Evidence→AST計画EVR充足、Evidenceの構成=評価対象構成、Evidence=`reviewed`かつ`active`かつ`artifact_verified`を追加する。`nonconforming`ではrejected evidenceを許す場合の規則を別に定義する。

### ASR-FND-003：`issued` Attestationが適合結果を必要としない

- 重大度：`high`
- 影響：3製品共通
- 根拠：`issued`は非空のAssessment Result参照、issuer、artifact locator、`human_confirmation_state: confirmed`を要求するだけで、参照結果が存在し`conforming`であること、対象と構成が一致すること、Schemeとdecision authorityが解決することを要求しない。Attestation参照はvalidatorの意味検査対象にも入っていない。
- 影響：`not_performed`または`nonconforming`な結果を根拠に、形式上`issued`の証明書・宣言を作れる。
- 最小修正：issued時に、Scheme、issuer、object、Assessment Resultの参照解決、全結果=`conforming`、対象Obligation・構成の包含、必要EVRの完全充足を検査する。Schemeがdecisionを要求する場合は、権限主体によるDecision recordも必須にする。

### ASR-FND-004：対象構成・責任主体の版付き正本がない

- 重大度：`high`
- 影響：3製品共通
- 根拠：AssessmentActivityは`CFG-SF-001`、`CFG-FL-01`、`CFG-MB-CANDIDATE`等を対象とするが、3モデル内にこれらの構成オブジェクトはない。モバイルバッテリーの`ROLE-*`参照にも型付き正本がない。EvidenceItemは`configuration_ref`を必須とするが、構成ID、baseline版、BOM/ソフトウェア版、locator、hash、provenanceを解決する仕組みがない。
- 影響：どの製品版を評価したか、証拠が市場投入対象と同一構成か、誰が評価・承認したかを検証できない。別版の証拠を流用するFalse Passを防げない。
- 最小修正：型付き`configurations[]`と`parties_or_roles[]`、または同等の外部参照台帳を追加する。少なくともID、version/baseline、対象範囲、artifact locator、integrity、provenance、validity stateを持たせ、scope、AST、EVI、ASR、ATTの参照をvalidatorで解決する。

### ASR-FND-005：失効・変更影響をAssurance結果とAttestationへ伝播できない

- 重大度：`high`
- 影響：3製品共通
- 根拠：C-CHG-01はSourceの`stale`または`superseded`時の再評価を求めるが、Sourceの`status` enumに`stale`がない。EvidenceItemには`validity_state`がある一方、Assessment Resultには有効性状態がなく、Attestationには発行日、有効開始日、満了日、失効理由、対象構成版がない。Source/Evidenceの変更からASR/ATTを停止するvalidator規則もない。
- 影響：根拠版または証拠が失効しても、過去の`conforming`や`issued`が有効に見え続ける。
- 最小修正：Source状態語彙を品質規則と整合し、ASR/ATTへ`valid_from`、`valid_to`、`validity_state`、`invalidation_reason`を追加する。Source、Provision、Applicability、EVR、EVI、ASR、ATTの依存グラフから再評価対象を列挙し、stale/superseded依存があればPass/issuedを遮断する。

### ASR-FND-006：`inconclusive`とEvidence充足の境界が不足する

- 重大度：`medium`
- 影響：3製品共通
- 根拠：`not_performed`にはEvidenceなし、日時なし、評価者なしの制約があり、現3モデルは適切に使用している。一方、`inconclusive`には実施済みActivity、評価日時、評価者、Evidenceまたは不足Findingの要求がない。EvidenceRequirementは`required_properties`を持つが、受入基準、対象版、適用期間、充足判定状態を持たない。`independence_required`とASTの`independence`の一致も検査されない。
- 影響：未実施と実施したが結論不能な状態が混ざり、必要Evidenceの一部だけで評価完了と解釈され得る。
- 最小修正：`inconclusive`はAST=`completed`、評価日時・評価者必須、Evidenceまたは不足Finding必須とする。EVRへ受入基準、適用構成/版、充足状態を追加し、independence要求の一致と不足EVRを意味検査する。

### ASR-FND-007：後段Assurance分岐の試験証拠がない

- 重大度：`medium`
- 影響：3製品共通
- 根拠：3製品ともConformityScheme、EvidenceItem、Attestationが空で、ASRは`not_performed`だけである。したがって今回の実験が実証したのは「証拠なし分岐」であり、`inconclusive`、`conforming`、`nonconforming`、`issued`、`expired`、`withdrawn`の成立・拒否条件ではない。出力契約が要求する`20_conformity_evidence_plan.md`も各製品のコンパクト実行にはない。
- 影響：後段分岐のSchema欠陥が実データで顕在化せず、validator PASSがAssurance全体のPASSと誤読される。
- 最小修正：合成Evidence fixtureを別枠で用意し、各状態の正例と、未完了AST、別構成Evidence、stale Evidence、not_performed ASRに基づくissued ATT等の負例が確実にFAILする回帰試験を追加する。少なくとも1製品で出力契約20まで生成する。

### ASR-FND-008：モバイルバッテリーのSource状態が版確認状態より強い

- 重大度：`medium`
- 影響：モバイルバッテリー
- 根拠：`SRC-MB-001`と`SRC-MB-002`はedition/effective_fromがnullで、評価文も版未確認とするが、Source statusは`active`である。`SRC-MB-004`は発行版を識別しているが、対象輸送で採用される版は未確認のまま`active`である。
- 影響：Source自体の公開状態と、対象構成・市場で適用する版の確認状態が混同され、将来の評価者が現行適用版確認済みと誤認し得る。
- 最小修正：`publication_status`と`applicability_version_state`を分離する。当面は版または採用版を未確認のSourceを`unknown`にするか、明示的な`version_unconfirmed`状態を追加する。

### ASR-FND-009：懐中電灯の評価記録がv0.2モデルと不一致である

- 重大度：`low`
- 影響：懐中電灯
- 根拠：`evaluation.md`は`no_projection: 2`と記述し、C-EPR-02でもprocess義務を`no_projection`にしたと説明する。一方、v0.2モデルは`PROC-FL-DENAN-INSPECTION`と`PROC-FL-CSPSA-REPORTING`を定義し、2件とも`process_requirement`へ投影している。
- 影響：Assurance Reviewerが評価文だけを読むと、実モデルと異なる投影状態を承認する。
- 最小修正：v0.2モデルから件数と規則判定を再生成し、`no_projection: 0`、`process_requirement: 2`へ更新する。評価記録にSchema版と生成日時を固定する。

### ASR-FND-010：製品Gateと独立Reviewer Gateが分離されていない

- 重大度：`medium`
- 影響：3製品共通
- 根拠：各`evaluation.md`は生成担当内のJ0または同一担当のSelf Reviewで`reviewable_40_candidate`を付与している。実験計画はCompliance、SE、Assurance、Meta-Judgeの役割分離と「AI評価だけで合格にしない」を要求する。本書により独立Assurance Reviewは実施されたが、その結果は`revise`であり、他の独立判定を代替しない。
- 影響：自己評価のGateが独立承認済みと誤読され、未解決Findingを残したまま次段へ進む。
- 最小修正：`generator_gate`、各Reviewer判定、`meta_judge_gate`を別フィールドにし、全必須Reviewerがpassするまで総合Gateを`review_pending`または`revise`に保つ。

## 製品別判定

### スマート扇風機：`revise`

- 良好：EvidenceItem/Attestationを作らず、2結果を`not_performed`にした。電波法Sourceの版未確認も`status: unknown`としている。
- Revision理由：ASR-FND-001〜007、010。特に、`CFG-SF-001`の版付き正本がなく、2活動の責任者と独立性が未決定である。構造的レビュー可能性はあるが、Assurance Passではない。

### 懐中電灯：`revise`

- 良好：EvidenceItem/Attestationを作らず、2結果を`not_performed`にした。2 Sourceは版未確認を`status: unknown`に保持している。
- Revision理由：ASR-FND-001〜007、009、010。加えて、v0.2モデルと`evaluation.md`のProcess投影説明を同期する必要がある。

### モバイルバッテリー：`revise`

- 良好：7 mandatory/prohibition ObligationにEvidence Requirementを置き、5結果を`not_performed`にした。必要独立性を一部`independent_internal`として区別している。
- Revision理由：ASR-FND-001〜008、010。`CFG-MB-CANDIDATE`と複数`ROLE-*`が未解決で、版未確認Sourceを`active`とする状態表現も修正が必要である。

## Gate判断

- SE 40点初稿の「構造的にレビュー可能」という限定判定は、本レビューだけでは取り消さない。
- Complianceモデル品質の現状は`revise`。
- 製品のAssurance outcomeは3製品とも`not_performed`。
- 正式適合、認証、表示可否、市場投入承認のGateは3製品とも`not_authorized`。
- ASR-FND-001〜006を修正し、負例fixtureを含む回帰試験がPASSするまで、C2以降でEvidenceItemまたはAttestationを伴う総合Passを許可しない。

## 優先修正順

1. `overall_result`をモデル品質とAssurance outcomeへ分離する。
2. ASR/EVI/AST/ATTの状態遷移・参照・構成一致をvalidatorへ追加する。
3. 版付き構成台帳と責任主体台帳を追加する。
4. stale/superseded/expiredの伝播とissued Attestationの成立条件を実装する。
5. 正例・負例fixtureで後段Assurance分岐を回帰試験する。
6. 懐中電灯評価記録とv0.2モデルを同期し、各Reviewer Gateを独立記録する。
