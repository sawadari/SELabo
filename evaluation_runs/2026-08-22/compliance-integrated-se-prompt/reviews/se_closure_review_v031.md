# v0.3.1残件 独立SE Closure Review（J1・修正後再判定）

## 結論

今回修正された主要残件は閉鎖できる。

- スマート扇風機は、`OBL-SF-005`の認証工事設計同一性を、Supplier情報、内部Process、Evidence Required Propertiesへ具体的に投影した。
- 懐中電灯は、開始／停止要求の分離とScenario根拠を維持している。
- モバイルバッテリーは、thermal monitoring、受電遮断経路、給電遮断経路を安定IDのStructureへ分け、`MBREQ-0006`から相互参照した。航空機内給電回避も法的禁止から分離したrecommendationとして、Requirement、Behavior、Verification、Documentation、Evidenceで一貫した。
- Scenario validatorはActor解決、非空の主流、観測結果、事後条件を検査し、4種類の負例をすべて検出した。
- 3製品の`09_traceability.csv`と17～21は、最新の型付き直接参照正本からの再生成結果と一致した。

初回`se_review.md`の12 Findingはすべて`closed`、前回v0.3.1で追加した3 Findingもすべて`closed`とする。

現行ファイルだけを再点検した結果、未閉鎖のHigh／Medium Findingはない。モバイルバッテリーの現行40点GateもRequirement→Behavior／Structure、Requirement→V&V、1要求1義務をすべて11/11へ統一し、B0比較と分母説明を同じ定義へ更新した。

| 製品 | 現行モデル意味 | 出力同期 | 独立J1 Gate | 主な残余 |
|---|---|---|---|---|
| スマート扇風機 | `pass` | `pass` | `pass_with_provisional_assumption` | 法規適用・設計値・証拠は人確認待ち |
| 懐中電灯 | `pass` | `pass` | `pass_with_provisional_assumption` | 法規適用・安全境界は人確認待ち |
| モバイルバッテリー | `pass` | `pass` | `pass_with_provisional_assumption` | 法規適用、安全境界、証拠は人確認待ち |

独立J1の実験パッケージGateは`pass_with_provisional_assumption`とする。各モデル正本に保存された`reviewer_gates.se`／`meta_judge=revise`は、独立再レビュー前の保守的状態であり、本タスクはReviewだけを編集する指示のため変更していない。最終roll-up時に本Closure結果を基に更新する必要がある。

## レビューメタデータ

| 項目 | 内容 |
|---|---|
| Review Tier | `J1 v0.3.1 Closure Re-review` |
| Reviewer | 初回および前回Closure Reviewを行った独立SE Reviewer |
| レビュー日 | 2026-08-22（Asia/Tokyo） |
| 対象 | 最新Schema／validator、3製品の`candidate_model.json`、`evaluation.md`、09および17～21 |
| 重点 | Scenario根拠、開始／停止要求、thermal allocation、航空旅客運用責任、分割Obligation投影、直接参照と出力整合 |
| 編集範囲 | 本Reviewのみ。モデル、実験定義、評価本文、生成出力は編集していない |

## 機械再検証

最新モデルを対象に`validate_candidate.py --trace-csv`と`export_compliance_views.py --check`を再実行した。

| 製品 | Schema・意味検証 | 収集ID | 派生関係／09行 | Need→Validation | Scenario | 17～21 `--check` |
|---|---|---:|---:|---:|---:|---|
| スマート扇風機 | `PASS` | 98 | 132 | 5/5 | 2 | `PASS`（5/5） |
| 懐中電灯 | `PASS` | 75 | 88 | 3/3 | 2 | `PASS`（5/5） |
| モバイルバッテリー | `PASS` | 146 | 197 | 6/6 | 3 | `PASS`（5/5） |

全14 ValidationCaseが代表Scenarioを参照し、全7 ScenarioにActor、前提、Trigger、非空の主流、代替または異常流、回復、事後条件、観測結果がある。現行モデルのScenario Actor、Validation Stakeholder、Verification Role／Configuration、Requirement allocation candidateはすべて正本内で解決する。

### validator負例

| 変異 | エラー | 判定 |
|---|---:|---|
| `SCN_SF-0001.actor_refs=STK-NOT-FOUND` | 1 | `unresolved actor`を検出 |
| `SCN_SF-0001.main_flow=[]` | 1 | 非空主流違反を検出 |
| `SCN_SF-0001.observable_results=[]` | 1 | 観測結果欠落を検出 |
| `SCN_SF-0001.postconditions=[]` | 1 | 事後条件欠落を検出 |
| `VER_SF-0001.responsible_role_ref=ROLE-NOT-FOUND` | 1 | 未解決Roleを検出 |
| `MBREQ-0007.allocation_candidate_refs=MBSTR-0001` | 1 | Requirement／Structure配分不一致を検出 |
| `MBBEH-0009.performer_candidate_refs=STK-NOT-FOUND` | 2 | 未解決performerとStructure owner不一致を検出 |
| `MBSTR_OPS-0002.owner_ref=MBSTK-0003` | 2 | 航空旅客Behavior 2件とのowner不一致を検出 |
| `MBSTR_OPS-0002.owner_ref=STK-NOT-FOUND` | 3 | 未解決ownerとBehavior owner不一致を検出 |

Behavior performer candidate、保持Structure、Structure ownerの解決と意味一致を負例で確認できた。

## 初回12 Findingの最終Closure

| Finding ID | 初回重大度 | 最終状態 | 修正後の根拠 |
|---|---|---|---|
| `SEJ1-SF-001` | high | `closed` | 5 Needすべてが、通常利用または異常・保守の具体的Scenarioを持つValidationCaseへ到達する。 |
| `SEJ1-SF-002` | high | `closed` | Supplier情報入手と、法規担当者による免許要否・認証経路・同一性・表示条件の内部確認Processを分離した。 |
| `SEJ1-SF-003` | medium | `closed` | ConfigurationとRoleは正本内IDへ解決し、Verification参照検査も有効である。 |
| `SEJ1-FL-001` | high | `closed` | 3 Needが暗所片手操作または異常温度時安全側移行のScenarioへ到達する。 |
| `SEJ1-FL-002` | medium | `closed` | `FLREQ-0001`は停止中の短押しによる開始、`FLREQ-0008`は照明中の長押しによる停止として分離され、個別Verificationを持つ。 |
| `SEJ1-FL-003` | medium | `closed` | JSON、09、17～21、`evaluation.md`はProcess投影2件、`no_projection=0`で整合する。 |
| `SEJ1-FL-004` | medium | `closed` | ConfigurationとRoleは正本内で解決し、非Product投影にも責任Roleがある。 |
| `SEJ1-MB-001` | high | `closed` | 6 Needが日常給電、保護・隔離、法規レビューの具体的Scenarioへ到達する。 |
| `SEJ1-MB-002` | high | `closed` | 損傷品隔離は`MBSTR_OPS-0001`へ配分され、物理製品`MBSTR-0001`から人の隔離行動を除外した。 |
| `SEJ1-MB-003` | medium | `closed` | `MBREQ-0006`は`MBSTR-0002`温度監視境界、`MBSTR-0003`受電遮断経路、`MBSTR-0004`給電遮断経路をallocation candidateとして参照し、各StructureからRequirementへ逆参照する。`MBVER-0006`も3 IDと承認済み安全分析に基づく遮断・記録を合否候補にした。個別監視点と閾値の確定は詳細設計・人確認へ残してよい。 |
| `SEJ1-MB-004` | medium | `closed` | 航空の3行動は個別DocumentationとOperational Requirementへ投影された。給電回避は`MBBEH-0011`へ分離され、recommendationと組織採用条件を保持する。 |
| `SEJ1-MB-005` | medium | `closed` | Configurationと5 Roleは正本内で解決し、Verificationと非Product投影から安定IDで参照する。 |

集計は`closed: 12`、`partially_closed: 0`、`open: 0`である。

## v0.3追加Findingの最終Closure

| Finding ID | 重大度 | 最終状態 | 修正後の根拠・残余 |
|---|---|---|---|
| `SEJ1-V03-X-001` | medium | `closed` | 実データに具体的Scenarioがあり、validatorもActor解決、非空主流、観測結果、事後条件を検査する。4負例をすべて検出した。 |
| `SEJ1-V03-X-002` | medium | `closed` | Verification Role／Configuration、Requirement allocationとStructure側逆参照、Behavior performer candidate、保持Structure／ownerの一致、Structure owner解決を検査する。未定義performer、誤owner、未定義ownerの変異をすべて検出した。 |
| `SEJ1-V03-MB-001` | medium | `closed` | `mobile-battery/evaluation.md`の機械検証は現行146 ID・197関係、正本内Configuration／Role、末尾197関係へ更新された。旧版の相反は解消した。 |

集計は`closed: 3`、`partially_closed: 0`、`open: 0`である。

## 前回v0.3.1新規Findingの最終Closure

### `SEJ1-V031-SF-001`：`closed`

`SUPREQ-SF-RADIO-CONFORMITY`は認証識別子・管理版、モジュール個体、HW・SW・アンテナ構成、表示情報、変更通知条件を要求する。`PROC-SF-RADIO-ROUTE-CHECK`は認証工事設計と`CFG-SF-001`を照合して同一性を記録し、構成差分と再評価要否を変更管理する。`EVR-SF-009`も照合結果、差分処置、再評価、表示権限を必要属性にした。`OBL-SF-005`のmandatoryな同一性と`OBL-SF-006`の表示permissionを、共有Projection先でも区別してレビューできる。

### `SEJ1-V031-MB-001`：`closed`

`EPR-MB-009C`、`MBREQ-0011`、新規`MBBEH-0011`、`MBVER-0011`、`DOC-MB-AIR-POWERING-AVOIDANCE`、`EVR-MB-006`は、いずれもAPP-MB-004の組織採用条件と非法定の給電回避recommendationを明示する。`MBBEH-0009`から給電回避を除外し、法的な機内充電禁止との混同を解消した。

### `SEJ1-V031-X-001`：`closed`

スマート扇風機の`evaluation.md`は98 ID・132 Trace、懐中電灯は75 ID・88 Traceへ統一された。各末尾の直接参照由来関係数も132／88で一致する。モバイルバッテリーの機械計数も146／197へ更新された。

集計は`closed: 3`、`partially_closed: 0`、`open: 0`である。

## 現行ファイルからの新規Finding

### `SEJ1-V031-MB-002`：`closed`

`MBSTR_OPS-0001`は損傷品隔離専用となり、owner `MBSTK-0003`、Requirement `MBREQ-0007`、Behavior `MBBEH-0006`だけを保持する。新規`MBSTR_OPS-0002`は航空旅客専用となり、owner `MBSTK-0001`、Requirement `MBREQ-0009/0010/0011`、Behavior `MBBEH-0009/0011`を保持する。各Requirementの`allocation_candidate_refs`も対応Structureへ更新された。validatorはBehavior performer candidateの解決、保持Structureまたはownerとの一致、Structure ownerの解決を検査し、未定義performer、誤owner、未定義ownerの負例を検出する。

### `SEJ1-V031-MB-003`：`closed`

| 項目 | 内容 |
|---|---|
| 重大度 | medium |
| 対象 | `mobile-battery/evaluation.md` |
| 規則 | Q-OUT-03、Q-TRC-02、C-VAL-01 |
| Closure | `closed` |
| 根拠 | 現行JSONのRequirement 11件について、`evaluation.md`はRequirement→Behavior／Structure 11/11、Requirement→V&V 11/11、1要求1義務11/11を報告する。B0比較の現行値も11/11、分母説明も「独立Need 6件・Requirement 11件」へ更新された。追加した`MBREQ-0009/0010/0011`はBehavior、Structure、Verificationへ実在Traceを持つ。 |
| 判定 | 正本、09、現行Gate指標、B0比較の分母が一致し、前回の退行検出漏れは解消した。 |

前回新規Finding 2件の最終状態は`closed: 2`、`partially_closed: 0`、`open: 0`である。現行再レビューで追加するHigh／Medium Findingはない。

## 製品別SE再判定

### スマート扇風機：`pass_with_provisional_assumption`

Need→Validation、Requirement→Behavior／Structure→Verification、Role／Configuration、Obligation分割、非Product投影、直接参照と09・17～21の同期にSE残件はない。適用性、認証経路、対象構成、実在証拠は引き続き人確認待ちであり、正式適合や設計承認を意味しない。

### 懐中電灯：`pass_with_provisional_assumption`

開始／停止要求、Scenario Validation、Process投影、構成・Role、正本・生成出力は整合する。法規適用と安全境界は候補であり人確認待ちだが、40点初稿としてSE意味Gateを妨げる残件はない。

### モバイルバッテリー：`pass_with_provisional_assumption`

thermal allocation、recommendation分離、運用Structure owner境界を閉鎖した。Requirement 11件はBehavior／Structure、Verificationへ到達し、1要求1義務も11/11である。法規適用、安全境界、実在証拠、航空会社条件は人確認待ちだが、40点初稿のSE意味Gateを妨げる残件はない。

## Gate再判定

| Gate軸 | スマート扇風機 | 懐中電灯 | モバイルバッテリー |
|---|---|---|---|
| Stakeholder→Need | `sufficient` | `sufficient` | `sufficient` |
| Need→Validation | `sufficient` | `sufficient` | `sufficient` |
| Scenario意味検査 | `sufficient` | `sufficient` | `sufficient` |
| Requirement原子性・一意性 | `sufficient` | `sufficient` | `sufficient` |
| Requirement→Behavior／Structure | `sufficient` | `sufficient` | `sufficient` |
| Requirement→Verification | `sufficient` | `sufficient` | `sufficient` |
| Compliance Projection意味 | `sufficient` | `sufficient` | `sufficient` |
| 09・17～21の正本同期 | `sufficient` | `sufficient` | `sufficient` |
| `evaluation.md`同期 | `sufficient` | `sufficient` | `sufficient` |
| 独立J1製品Gate | `pass_with_provisional_assumption` | `pass_with_provisional_assumption` | `pass_with_provisional_assumption` |

## 残余

未閉鎖のSE High／Medium Findingはない。対象構成、要求値、法規適用性、認証経路、試験証拠、責任者の正式決定は、候補モデルの外で権限を持つ人が確認する。

本レビューはSEモデル候補の意味整合を判定したものであり、法的適用性、安全境界、規格適合、認証取得または市場投入を承認するものではない。
