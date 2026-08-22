# Compliance Layer品質規則

元実験の[04_QUALITY_RULES.md](../hierarchical-se-prompt/04_QUALITY_RULES.md)へ、次の規則を追加します。結果状態は元実験と同じ`pass`、`pass_with_provisional_assumption`、`fail`、`not_applicable`、`not_performed`を使用します。

## 1. 原典と意味の境界

### C-SRC-01 AuthorityとSource

- Sourceには識別子、版または版の未確認状態、発行主体参照、原典位置、入手状態がある。
- Sourceの種類から拘束力を推測していない。

### C-SRC-02 Provision

- ProvisionはSourceへ戻れ、条・項・節・表・附属書などの位置を一意に説明できる。
- 取得していない原典の条項番号や引用をAIが作っていない。

### C-SRC-03 原典と解釈

- 原典断片、NormativeStatement、ApplicabilityAssessment、Obligationを別オブジェクトとしている。
- 一つのProvisionと一つのNormativeStatementを1:1へ固定していない。
- 著作物は保存方針に従い、不要な全文複製をしていない。

## 2. 適用性

### C-APP-01 判断コンテキスト

各ApplicabilityAssessmentに、法域、市場、製品分類、意図する使用、対象構成、ライフサイクル、評価時点がある。不明値は空文字で隠さず`unknown`または参照可能な仮定として残す。

### C-APP-02 拘束根拠

`source_type`と`binding_basis`を分離し、直接法規、参照取込み、許容適合手段、認証スキーム、契約、社内規定、自主採用、不明を区別する。

### C-APP-03 人の権限

- AI生成の適用性候補は`human_confirmation_required=true`である。
- AI生成候補は`human_confirmation_state=pending`、`confirmed_by_ref=null`、`confirmed_at=null`である。正式確認値は権限を確認した責任主体IDと確認日時を伴う。
- 根拠不足時は`uncertain`である。
- AIだけの判断を正式な適用・非適用決定として記述していない。

### C-APP-04 再評価

市場、法域、製品分類、用途、構成、原典版、有効期間の変更を検知できる`review_trigger`がある。

## 3. ObligationとEngineering Projection

### C-OBL-01 Obligationの根拠

各ObligationはNormativeStatementとApplicabilityAssessmentへ戻れる。`not_applicable`だけを根拠に有効なObligationを作らない。

### C-EPR-01 投影完全性

applicable、partially_applicableまたはuncertainな対象Obligationには、一つ以上のEngineeringProjection、または明示的な`no_projection`理由がある。

### C-EPR-02 投影先の分離

- Product、Interface、Constraint、Operationalの投影は対応するSE要素を参照する。
- Process、Assurance、Organization、Documentation、Supplierの投影は`projection_targets[]`の型付き要素を参照する。
- `projection_kind`と`projection_targets[].target_kind`が一致する。
- Process、Assurance、Organization、Documentationの投影を対象システムの要求として扱っていない。
- Evidence投影はEvidenceRequirementへ接続する。

### C-EPR-03 要求の導出元

- 全requirementsに`derivation_sources[]`がある。
- Compliance由来の要求は`source_kind=compliance_obligation`、Obligation ID、EngineeringProjection IDを持つ。
- `requirement_type=regulatory_candidate`を使用していない。

### C-EPR-04 SysML境界

Authority、Source、Provision、NormativeStatement、ApplicabilityAssessment、Obligation、ConformitySchemeをSysML Requirementとして投影していない。SysML仕様はEngineeringProjection後の工学要素だけを対象にする。

## 4. Evidenceと適合性評価

### C-EVI-01 証拠要求と証拠

EvidenceRequirementとEvidenceItemを分離する。計画中の試験報告や監査記録をEvidenceItemとして作らない。

### C-EVI-02 証拠の追跡

EvidenceItemはEvidenceRequirement、対象構成、生成活動、版、生成日時、artifact locator、完全性情報を分かる範囲で追跡できる。不明値を架空値で補わない。

### C-EVI-03 Mandatory coverage

mandatoryなObligationにはEvidenceRequirementがあるか、証拠不要の理由と人の確認事項がある。

### C-AST-01 評価活動

AssessmentActivityは対象Obligation、対象物、方法、責任者、独立性、予定EvidenceRequirementを区別する。SE verificationで扱えない監査や認証レビューをVerificationCaseへ無理に入れない。

### C-ASR-01 評価結果

- `conforming`または`nonconforming`には実在するEvidenceItem、対象構成、評価活動、評価者、評価日時がある。
- 証拠未評価時は`inconclusive`または`not_performed`である。
- Findingと是正が必要な場合、関連IDを残す。

### C-ATT-01 Attestation

証明書、承認、宣言などを`issued`とする場合、発行主体、対象、根拠となるAssessmentResult、実在するartifact locator、人の確認状態がある。候補や計画を取得済みと表現しない。

## 5. 変更影響と複数規格

### C-CHG-01 Source変更

Sourceが`stale`または`superseded`になった場合、関連Provision、NormativeStatement、ApplicabilityAssessment、Obligation、EngineeringProjection、EvidenceRequirementを再評価対象として列挙する。

### C-MAP-01 Mapping

複数原典またはObligation間の関係はMappingとして記録し、`equivalent`、`subset`、`superset`、`intersection`、`related`、`conflict`、`unknown`を区別する。AI候補のMappingは人が確認するまで重複排除や適合主張の根拠にしない。

## 6. Traceability正本

### C-TRC-01 型付き直接参照

- Need、Requirement、Behavior、Structure、Verification、Complianceの関係は、意味を所有する要素の型付き直接参照を正本とする。
- `relations[]`は、型付きフィールドで表現できない補助関係だけに使用する。
- 同じsource、target、relation typeを直接参照と`relations[]`へ重複記録しない。

### C-TRC-02 CSV投影

- `09_traceability.csv`は型付き直接参照から決定的に生成する。
- `relations[]`が空でも主要TraceをCSVへ投影する。
- CSVのsource IDとtarget IDはすべて正本内で解決する。
- オフラインQAではSchema検証に加え、`scripts/validate_candidate.py`の意味的参照検査を通す。ChatGPTのプロンプト専用回帰ではスクリプトを実行せず、10_CHATGPT_PROMPT_ONLY_REGRESSION.mdの期待不変条件を人が判定する。

### C-VAL-01 Need Validation分離

- 各NeedはValidation Case候補またはSuccess Measureを少なくとも1件参照する。
- 各Validation Caseは対象Needから逆参照でき、代表ScenarioまたはSuccess Measureを少なくとも1件持つ。Scenario、代表Stakeholder、構成、責任ロールの参照は正本内で解決する。
- Requirement Verificationの網羅率をNeed Validationの網羅率として報告しない。
- Behaviorの`performer_candidate_refs`はStructureまたはStakeholderとして解決し、Behaviorを保持するStructure自身またはその`owner_ref`と一致する。異なる人の運用責任を1つのStructure ownerへ混在させない。

### C-CTX-01 構成・責任主体正本

- Scope、Assessment Activity、Evidence Item、Assessment Result、Attestationの構成参照は`configurations[]`で解決する。
- 責任者、評価者、発行者のIDは`parties_or_roles[]`で解決する。

### C-DISC-01 法規候補探索ログ

- 製品構成、法域、市場、公式探索先、query、実行時点、候補Sourceの採用・除外・保留理由を記録する。
- 実行時queryの有無を`query_log_state`で明示する。原始queryを保存しなかった過去runは`unavailable_legacy_run`とし、後から再構成した検索語を実行時queryとして扱わない。
- 法規担当者がinventoryを確認するまで、自動探索結果を完全または網羅的と表現しない。

### C-GATE-01 Gate分離

- モデル構造品質`model_quality_result`と製品評価状態`assurance_outcome`を別フィールドにする。
- `not_a_compliance_approval=true`とReviewer別Gateを必須にし、Meta-Judgeが未承認なら総合Passにしない。

### C-ASR-02 実施済み評価の成立条件

- `inconclusive`、`conforming`、`nonconforming`は完了済みAssessment Activity、評価者、評価時点を必要とする。
- definitive outcomeは、1件以上の評価対象Obligation、版・artifact locator・integrityを持つユーザー確認済みベースライン構成、同一構成のreviewed・active・artifact_verified Evidence、Activity計画集合と一致する全EVR、そのRequired Propertyの生成後確認、権限確認済み評価者、assessed状態のObligation、権限確認済みの人が確認したdefinitiveなApplicabilityを必要とする。
- definitive outcomeが参照するSourceとProvisionは、公式取得またはユーザー提供の状態だけでなく、権限確認済みの確認者IDと評価以前の確認時刻を持つ。Sourceは識別子と版または発効日、Provisionは正規位置を必要とする。
- `assurance_outcome=conforming`は、scope内のApplicabilityがすべて権限者により確認済みでuncertainを含まず、applicable／partially applicableな全Obligationをactiveなconforming Assessment Resultが覆う場合だけ成立する。

### C-ATT-02 Attestation発行条件

- `issued`は同一構成のactiveな`conforming`結果、Schemeの全Obligationと必要Evidence、Schemeの適合対象と一致する解決可能な対象、Scheme decision authorityと一致する権限確認済み発行者、人確認および有効期限内であることを必要とする。日時Formatと時刻順序を検査し、不正値、評価前の発行、評価時点より後のvalid_from、発行後のvalid_toを有効として扱わない。
- `not_performed`、`inconclusive`、`nonconforming`またはstaleな結果から`issued`を作らない。

## 7. 主要な失敗条件

次のいずれかがある場合、Compliance Layerの総合結果を`fail`とします。

- 原典または条項を捏造した。
- AIだけで法的適用、非適用、適合、認証取得を確定した。
- 原典、適用性、Obligation、工学要求を一つのRequirementへ潰した。
- ProcessまたはOrganizationへの義務を対象システムの挙動要求として記述した。
- 存在しない証拠または証明書を実在するEvidenceItemとして記録した。
- applicableまたはuncertainな重大Obligationが投影も人の確認事項もなく途切れた。
- 非Product投影が未定義IDまたはSchema外の自由形式オブジェクトを参照した。
- 空の`relations[]`を完全なTrace CSVとして出力した。

## 8. 品質報告への追加項目

`13_quality_report.md`に次を追加します。

- Compliance規則IDごとの判定、証拠、影響ID
- 取得・検証できなかった原典
- `uncertain`なApplicabilityAssessment
- 投影のないObligation
- EvidenceRequirementのないmandatory Obligation
- 実施していないAssessmentActivity
- 人が決定すべき適用性、解釈、適合、認証事項

## 9. ChatGPT・プロンプト専用回帰

### C-PT-01 ツール不使用

- `10_CHATGPT_PROMPT_ONLY_REGRESSION.md`の回帰テストは、外部検索、Web、Python、コード実行、コネクタ、その他のツールを呼び出さない。
- ツール呼出しがあったケースは必ず`FAIL`とし、ツール結果を混ぜた再実行を同一ケースの合格としない。

### C-PT-02 固定入力と期待不変条件

- ケース入力、プロンプト版、モデル、実行日時、判定者を記録する。
- 文言やIDの完全一致ではなく、各ケースの期待不変条件の充足で`PASS`/でない場合は`FAIL`とする。
- 合格はプロンプトの安全側の振る舞いを示すだけであり、法的正確性や適合判定を保証しない。

### C-PT-03 安全側の格下げ

- 未提供の原典、条項、版、日付、証拠、証明書、人の確認を補完しない。
- 適用性根拠不足は`uncertain`/未確認、証拠不足は`not_performed`/未実施または`inconclusive`/証拠不十分に格下げする。
- 不明な情報をツール検索で補わず、人の確認バックログへ並べる。

### C-PT-04 プロンプト回帰とオフラインQAの分離

- `scripts/validate_candidate.py`、`scripts/test_assurance_semantics.py` のPASSを、ChatGPTの回答が期待不変条件を満たした証拠としない。
- オフラインQAは構造・意味検証の任意補助であり、ChatGPTの回帰テストの必須ツールではない。
