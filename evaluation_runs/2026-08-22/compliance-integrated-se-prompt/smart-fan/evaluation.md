# C1評価：スマート扇風機

## 結論

- Generator内の初回Gateは`reviewable_40_candidate`だったが、独立J1はCompliance・SE・Assuranceとも`revise`である。v0.3修正後の`meta_judge`も再レビュー完了までは`revise`とする。
- Compliance Layerの構造品質候補は`pass_with_provisional_assumption`、製品の`assurance_outcome`は`not_performed`であり、両者を別フィールドへ分離した。
- 3件のApplicability Assessmentはすべて`uncertain`である。電源方式、定格、事業者区分、無線方式および無線モジュールが未決定であり、正式な法的適用、適合、PSE表示、技術基準適合証明、認証取得を主張しない。
- Evidence Requirementは9件を計画したが、実在証拠がないため`EvidenceItem: 0`、`AssessmentResult: not_performed`、`Attestation: 0`とした。

## v0.3 High Finding修正

- 5/5 Needへ独立したValidationCase候補を追加し、Requirement VerificationとStakeholder価値のValidationを分離した。
- 版未確認の`CFG-SF-001`と6つの責任ロール候補を正本へ登録した。
- 無線モジュール情報のSupplier要求に加え、製品責任者が免許要否・適合経路・表示を確認するProcess要求を追加した。
- 法第8条候補のObligationから、別根拠の「記録保持」を除外した。
- 「容易に転倒しない」から「転倒しない」への投影を`conservative_strengthening`として明示した。
- 電波法候補を第4条の免許、第38条の24の工事設計認証経路、第38条の25の認証工事設計同一性義務、第38条の26の表示権限へ分割した。
- v0.3.1 Schema・意味検証は`PASS`（98 ID、132 Trace）。独立再レビュー完了前のため総合Gateは`revise`のままである。

## 評価メタデータ

| 項目 | 内容 |
|---|---|
| run_id | `EVAL-2026-08-22-C1-SF-01` |
| condition | `C1`：`hierarchical-se-prompt` + `compliance-integrated-se-prompt` |
| target | スマート扇風機 |
| assessed_as_of | 2026-08-22（Asia/Tokyo） |
| input | `evaluation_runs/2026-08-21/smart-fan/chat_and_candidate.md` |
| B0 review | `evaluation_runs/2026-08-21/smart-fan/independent_review.md` |
| candidate | `candidate_model.json` |
| reviewer | C1生成を担当した独立サブエージェント。法務、規制当局、認証機関または設計承認者ではない |
| 未実施 | 実利用者確認、実機試験、法務・認証専門家レビュー、正式な適合性評価 |

## 確認した一次情報

調査には発行主体または政府の公開情報だけを使用した。規格本文、販売者の解説および二次情報は根拠にしていない。

| ID | 正式情報 | 確認した範囲 | 制約 |
|---|---|---|---|
| `SRC-SF-001` | [e-Gov：電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234?occasion_date=20260611)、[METI：基準適合確認](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_04.html) | 法第8条第1項に関する届出事業者の技術基準適合義務候補 | 対象製品の給電方式、定格、事業者区分が未確認 |
| `SRC-SF-002` | [METI：特定電気用品以外の電気用品一覧](https://www.meti.go.jp/policy/consumer/seian/denan/non_specified_electrical.html)、[METI：技術基準省令解釈 別表第八（2026-06-01）](https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku/beppyoudai8_260601.pdf) | 定格消費電力300 W以下の扇風機という分類候補、および別表第八2(41)イ(イ)の通常使用時転倒防止候補 | 技術基準省令解釈は性能規定を満たす基準の一つであり、採用する適合経路を未決定 |
| `SRC-SF-003` | [e-Gov：電波法](https://laws.e-gov.go.jp/law/325AC0000000131) | 第4条の無線局免許と例外、第38条の24の工事設計認証、第38条の25の認証工事設計同一性義務、第38条の26の表示権限 | 評価時点のRevision ID、無線仕様、免許不要条件および特定無線設備分類を確定していない |

原典の長文は保存せず、識別子、位置および工学的要約だけを候補モデルへ記録した。電波法の評価時点版を確定できなかったため、`edition: null`、`status: unknown`とし、適用性を`uncertain`に保った。

## 標準化メトリクス

### SE初稿

| 指標 | 結果 |
|---|---:|
| Stakeholder | 3 |
| Need | 5 |
| Requirement | 7 |
| Behavior | 7 |
| Structure | 1 |
| Verification Case | 7 |
| 主要Stakeholder → Need | 5/5 = 100% |
| 主要Need → Requirement | 5/5 = 100% |
| 主要Requirement → Behavior / Structure | 7/7 = 100% |
| 主要Requirement → V&V候補 | 7/7 = 100% |
| 主要要素の`origin` / `claim_state` / `decision_state` | 32/32 = 100% |
| 1要求1義務 | 7/7 = 100% |
| 未管理の重大矛盾 | 0 |

`REQ_SF-0004`と`REQ_SF-0005`では、B0の「停止または再開」を2要求へ分割した。`REQ_SF-0001`と`BEH_SF-0001`では、運転モード集合を手動、自動、静音の3候補へ合わせた。静音性能値と安全停止時間は創作せず、人の確認待ちとしている。

### Compliance Layer

| 指標 | 結果 |
|---|---:|
| Authority / Source / Provision | 2 / 3 / 6 |
| Normative Statement / Applicability / Obligation | 6 / 3 / 6 |
| `uncertain` Applicability | 3/3 |
| Engineering Projection | 7 |
| Product・Constraint投影 | 1 |
| Process投影 | 2 |
| Supplier投影 | 1 |
| Evidence投影 | 3 |
| SourceからEvidence Requirementまで到達するObligation経路 | 6/6 |
| Evidence Requirement | 9（Compliance直接対象3、SE V&V候補6） |
| 投影のないObligation | 0 |
| MandatoryだがEvidence RequirementのないObligation | 0 |
| Evidence Item | 0 |
| 架空Evidence Item | 0 |
| Assessment Activity / Result | 2 / 2（全件`not_performed`） |
| Attestation | 0 |
| False applicability / conformity / certification claim | 0 |

## Compliance品質規則

| 規則 | 判定 | 根拠 |
|---|---|---|
| C-SRC-01 | `pass_with_provisional_assumption` | AuthorityとSourceを分離した。電波法の評価時点版だけ未確定として明示した。 |
| C-SRC-02 | `pass` | 6 Provisionを取得済みSourceと位置へ接続し、未確認条項を作っていない。 |
| C-SRC-03 | `pass` | Provision、NormativeStatement、ApplicabilityAssessment、Obligationを別オブジェクトにした。 |
| C-APP-01 | `pass` | 3評価すべてに法域、市場、分類、用途、構成、ライフサイクル、評価日を記録した。 |
| C-APP-02 | `pass` | 直接法規と許容適合手段を区別した。 |
| C-APP-03 | `pass` | 全件`uncertain`かつ`human_confirmation_required: true`である。 |
| C-APP-04 | `pass` | 電源、定格、役割、無線仕様、原典版の変更をreview triggerにした。 |
| C-OBL-01 | `pass` | 6 ObligationがNormativeStatementとApplicabilityAssessmentへ戻る。 |
| C-EPR-01 | `pass` | 6 Obligationすべてに1件以上のEngineering Projectionがある。 |
| C-EPR-02 | `pass` | 製品制約は`REQ_SF-0007`、事業者活動はProcess、無線調達はSupplier、証拠はEvidence Requirementへ分離した。 |
| C-EPR-03 | `pass` | 全Requirementに`derivation_sources`があり、Compliance由来要求はObligationとProjectionへ戻る。`regulatory_candidate`はない。 |
| C-EPR-04 | `pass` | SysML候補へ投影するのはEngineering Projection後の製品制約だけである。 |
| C-EVI-01 | `pass` | Evidence Requirement 9件とEvidence Item 0件を分離した。 |
| C-EVI-02 | `not_applicable` | 実在Evidence Itemがないためprovenance評価対象がない。 |
| C-EVI-03 | `pass` | 4 mandatory ObligationすべてにEvidence Requirementがあり、2 permissionも証拠要求へ追跡できる。 |
| C-AST-01 | `pass` | 製品法規レビューと無線法規経路レビューを別Assessment Activityにした。 |
| C-ASR-01 | `pass` | 証拠未評価のため全Assessment Resultを`not_performed`とした。 |
| C-ATT-01 | `not_applicable` | Attestationを作成していない。 |
| C-CHG-01 | `pass_with_provisional_assumption` | Source版変更をreview triggerにした。実際のSource変更影響解析は未発生である。 |
| C-MAP-01 | `not_applicable` | 重複排除または等価性を主張するMappingを作成していない。 |

主要失敗条件である、原典・条項の捏造、AIだけの正式適用判断、意味層の潰し込み、Process義務の製品挙動化、架空証拠、重大Obligationの追跡断は確認されなかった。

## 40点Gate

| 評価軸 | 判定 | 根拠 |
|---|---|---|
| Stakeholder → Need | `sufficient` | 5/5の主要Needが定義済みIDとStakeholder参照を持つ。 |
| Need → Requirement | `sufficient` | 5/5の主要Needから少なくとも1件のRequirementへ到達する。 |
| Requirement → Behavior / Structure | `sufficient` | 7/7のRequirementに個別Behaviorがあり、共通Structureにも参照される。 |
| Requirement → V&V candidate | `sufficient` | 7/7にVerification CaseとEvidence Requirementがある。 |
| provenance / status | `sufficient` | 主要32要素で100%。 |
| 1要求1義務 | `sufficient` | 7/7。停止と再開を分割した。 |
| 過剰詳細化 | `sufficient` | 部品型番、公差、詳細アルゴリズムまたは実装クラスを作っていない。 |
| 数値、安全、法規 | `weak` | 10°は取得済み一次情報を根拠にした適用性未確定候補。停止時間、音圧、風量は未決定のまま人へ送った。 |

Hard Blockerは0件である。`reviewable_40_candidate`と判定するが、`semantic_validity: unknown_with_reason`であり、正式な設計承認または法規適合を意味しない。

## B0比較（初回C1-remediated生成時）

| 指標 | B0（2026-08-21独立レビュー） | C1 | 差分 |
|---|---|---|---|
| Gate | `below_reviewable` | `reviewable_40_candidate` | Need IDと主要要素属性を修復 |
| Hard Blocker | 2件 | 0件 | HB-01、HB-02を解消 |
| Need → Requirement | 0/5明示 | 5/5 | ID参照を定義 |
| Requirement → Behavior / Structure | 3/5 sufficient | 7/7 | モード集合を整合し、要素属性を追加 |
| Requirement → V&V | 2/5 sufficient | 7/7 | V&VとEvidence RequirementをID化 |
| 主要要素provenance | 不足 | 32/32 | Behavior、Structure、V&Vを含め100% |
| 1要求1義務 | 4/5 | 7/7 | 停止と再開を分割 |
| Source → Evidence Requirement | 0 | 3 | Compliance chainを追加 |
| Process義務の製品要求化 | 評価対象なし | 0 | Process投影を独立保持 |
| 架空証拠 | 0 | 0 | 増加なし |
| 法的適用・適合・認証の誤主張 | 0 | 0 | 増加なし |

C1ではCompliance Layer追加と同時にB0 Findingの最小修正も行ったため、Gate改善のすべてをCompliance Layer単独の効果とは帰属できない。一方、B0に存在しなかった原典、適用性、Obligation、工学投影、証拠要求の意味境界と3本のend-to-end traceは、Compliance拡張による追加効果である。

## 人の確認バックログ

1. 法規担当者は、給電方式、定格消費電力、同梱ACアダプター、製造・輸入・販売の役割を基に、電気用品安全法上の分類と義務主体を確認する。
2. 法規担当者と安全設計者は、技術基準省令解釈別表第八を採用するか、`REQ_SF-0007`の対象構成、通常使用状態、傾斜試験方法を確認する。
3. 通信設計者と法規担当者は、無線方式、周波数、空中線電力、モジュールの技術基準適合証明または工事設計認証、表示方法、免許要否を確認する。
4. 安全設計者は、`REQ_SF-0002`の危険状態集合と停止時間閾値を決める。
5. 製品企画、利用者代表および試験担当者は、`REQ_SF-0003`の音圧、風量、測定位置、環境条件および受入れ範囲を決める。

## 検証結果

| 検査 | 結果 |
|---|---|
| JSON構文解析 | `PASS`（Python 3.11 `json` / `json.tool`） |
| 元Schema + Compliance拡張Schema | `PASS`、エラー0件（`jsonschema` Draft 2020-12、正式な`$id`をRegistryへ登録） |
| `requirement_type: regulatory_candidate` | 0件 |
| Compliance RequirementのObligation / Projection参照 | `REQ_SF-0007`で解決 |
| Obligation without projection | 0件 |
| Mandatory without Evidence Requirement | 0件 |
| Evidence Item / Attestation | 0 / 0 |

## 実験判断

この1事例では、重大な虚偽を増やさず、B0よりレビュー可能なTraceとCompliance意味境界を追加できたため、Pilot判断は`継続候補`とする。次段階はC2として、専門家が確認した市場、製品分類、電源・無線構成および適用原典一覧を入力し、3件の`uncertain`を人が採用、修正または却下した件数とレビュー時間を測定することである。

本評価は法的助言、PSE適合、電波法適合、技術基準適合証明、工事設計認証、製品認証、安全認証または市場投入承認ではない。

## v0.2残件修正（履歴）

Meta Review後、Schema v0.2へ移行した。`PROC-SF-PSE-TECH-CHECK`と`SUPREQ-SF-RADIO-CONFORMITY`を型付き`projection_targets[]`へ格納し、EngineeringProjectionの参照先種別を意味検証した。

`validate_candidate.py`による合成Schema・ID参照・投影種別・Evidence到達検査は`PASS`で、型付き直接参照から132関係の[09_traceability.csv](09_traceability.csv)を決定的に生成した。`relations[]`は補助関係専用のため空のままでよい。
