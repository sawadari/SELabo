# VSE概念モデル・型付き関係仕様（v1.0.0）

## 1. 対象境界
VSEは**事業の価値創造に関する意思決定支援システム**の情報モデルである。自社が制御できるもの（施策、提供体制、資源配分、情報の管理）と自社が制御できないもの（顧客の購買判断、競合の行動、市場・法規）を切り分ける。市場や顧客を企業の設計部品として扱わない。

## 2. V0～V7は独立した視点
| View | 内容 | 主要要素 |
|---|---|---|
| V0 | 事業・機会 | Objective, Problem |
| V1 | 関係者・エコシステム | Actor, Capability |
| V2 | 顧客・業務文脈 | Actor, Problem, Value |
| V3 | 市場・価値仮説 | Hypothesis, Evidence, Value |
| V4 | 価値提供構想 | Value, Capability, Alternative |
| V5 | 戦略・意思決定 | Alternative, Decision, Risk |
| V6 | 実行・営業 | Intervention, Capability, Actor |
| V7 | 検証・学習 | Experiment, Evidence, Outcome |

V0→V7は固定された工程・上位下位の分解ではない。視点は同一の要素に複数付けられる。顧客ライフサイクル、対象市場、技術、組織、地域は別軸で管理する。

## 3. 13種の要素
中心JSONにはobjectives, actors, problems, values, hypotheses, alternatives, capabilities, decisions, interventions, evidence, outcomes, risks, experimentsを持つ。各要素は識別子・名称・説明・origin・claim_state・decision_state・validity_state・confidence・source_refs・viewpoints・rationale・human_confirmation_requiredを共通属性として持つ。

`Hypothesis`はprediction、falsification_condition、verification_plan、alternative_explanationsを持つ。`Decision`はdecision_authority_actor_id、chosen_alternative_id、criteria、revisit_triggerを持つ。`Experiment`はtarget_hypothesis_ids、method、primary_measure、decision_rule、confounders、statusを持つ。

## 4. 関係型の方向
下表は主要な例。全許可型と型の契約は`schemas/relation_type_contract.json`。
| Relation | source → target | 意味 |
|---|---|---|
| `addresses` | Alternative → Problem | この案がどの問題を解く候補か |
| `experiences` | Actor → Problem | 誰が問題を経験するかという仮説/観測 |
| `offers` | Alternative → Value | 案がどの価値を提供しようとするか |
| `supports` | Evidence → Hypothesis | 情報が仮説を支持する。実証ではない場合がある |
| `contradicts` | Evidence → Hypothesis | 情報が仮説に反する |
| `tests` | Experiment → Hypothesis | どの仮説を検証するか |
| `implements` | Intervention → Alternative | どの案を実行する行動か |
| `measures` | Outcome → Objective | 何の成果を測る計画/観測か |
| `selected_over` | Alternative → Alternative | どの案との比較選択か（決定が未承認なら仮） |
| `causally_influences` | Intervention → Outcome | 施策が成果へ影響するという**因果仮説**。statusが必須 |

**重要**：`supports`は出自・説明上の支持であり、`causally_influences`は因果を主張する。`derived_from`は情報の導出経路であり、因果は含まない。`causal_status=experimentally_estimated`であっても、妥当な研究設計の審査なしに因果を確定できない。

## 5. 安定IDと更新
正本IDは`OBJ-0001`、`HYP-0001`等とし、表示順や視点を変更しても再採番しない。`change_log`に変更を記録し、過去の意思決定・根拠を保持する。新情報が仮説を反証した場合は`stale` / `superseded`とし、関連案や施策に影響フラグを立てる。

## 6. 意味モデルの限界
JSON Schemaは構文・要素型の一部を検査するが、実際の顧客価値・戦略の優劣・因果関係は検証しない。要素の量や接続密度が高くても、内容の正しさを意味しない。
