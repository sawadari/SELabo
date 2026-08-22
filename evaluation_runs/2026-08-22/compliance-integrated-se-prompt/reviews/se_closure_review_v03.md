# v0.3 Source Patch後 独立SE Closure Review（J1）

## 結論

v0.3は、初回SE ReviewのHigh Findingへ実質的な修正を加えた。全製品でNeed→ValidationのID経路、構成・役割レジストリ、Reviewer Gateが追加され、スマート扇風機の無線確認Processとモバイルバッテリーの運用プロセス構造も追加された。

ただし、初回12 FindingのClosureは`closed: 5`、`partially_closed: 5`、`open: 2`であり、3製品とも最終判定は`revise`を維持する。新規High Findingはない。新規Medium Findingは3件である。

| 製品 | 初回Finding Closure | v0.3 SE判定 | 主な残件 |
|---|---|---|---|
| スマート扇風機 | closed 2 / partially_closed 1 | `revise` | Validationの代表シナリオ・成功尺度が弱い |
| 懐中電灯 | closed 2 / partially_closed 1 / open 1 | `revise` | `FLREQ-0001`の開始／停止条件が未修正 |
| モバイルバッテリー | closed 1 / partially_closed 3 / open 1 | `revise` | 運用要求の配分参照、温度要求、航空運用投影 |

3モデルの`reviewer_gates.meta_judge`はすべて`revise`であり、現行成果物は残件を総合Passとして扱っていない。この保守的なGate制御は妥当である。

## レビューメタデータ

| 項目 | 内容 |
|---|---|
| Review Tier | `J1 Closure Review` |
| Reviewer | 初回`se_review.md`を作成した独立SE Reviewer |
| レビュー日 | 2026-08-22（Asia/Tokyo） |
| 比較元 | `reviews/se_review.md`の12 Finding |
| 比較先 | Compliance Schema v0.3.0、最新`validate_candidate.py`、3製品のJSON・CSV・`evaluation.md` |
| 編集範囲 | 本Closure Reviewのみ。モデル本体と評価本文は編集していない |

## Closure状態の定義

- `closed`：初回Findingの根拠が解消され、要求した最小修正を成果物で確認できる。
- `partially_closed`：主要な構造修正はあるが、意味、別の正本フィールドまたは再発防止検査に残件がある。
- `open`：初回Findingの根拠が現行成果物に残る。

## v0.3機械再検証

`validate_candidate.py`を再実行し、保存CSVを同じJSONから再生成した一時CSVとSHA-256で比較した。

| 製品 | v0.3 Schema・意味検証 | 収集ID | 派生関係 | 保存CSVとの完全一致 | Need→Validation |
|---|---|---:|---:|---|---:|
| スマート扇風機 | `PASS` | 87 | 103 | `true` | 5/5 |
| 懐中電灯 | `PASS` | 67 | 77 | `true` | 3/3 |
| モバイルバッテリー | `PASS` | 125 | 172 | `true` | 6/6 |

全Verificationの`responsible_role_ref`と`configuration`、全`projection_targets[].responsible_role_ref`は、現行モデル内の`parties_or_roles[]`と`configurations[]`へ解決した。これは初回モデルからの明確な改善である。

## 初回Finding Closure Matrix

| 初回Finding ID | 初回重大度 | Closure | v0.3で確認した修正 | 残件・判定理由 |
|---|---|---|---|---|
| `SEJ1-SF-001` | high | `partially_closed` | 5 Needすべてに双方向参照可能なValidationCaseを追加し、CSVにも`validates`関係を生成した。 | 全5件で`scenario_refs=[]`、`success_measure_refs=[]`であり、運用Contextと受入れ基準はNeedの`expected_value`を定型文へ移した水準である。軸は`missing`から`weak`へ改善したが、代表シナリオと成功判定方法は未閉鎖である。残留重大度はmedium。 |
| `SEJ1-SF-002` | high | `closed` | `PROC-SF-RADIO-ROUTE-CHECK`と`EPR-SF-006`を追加し、Supplier情報入手と製品責任者の免許要否・適合経路確認を分離した。`AST-SF-002`も`ROLE-SF-COMPLIANCE`へ割り当てた。 | 初回Findingが要求した内部確認Processを確認できる。法的判断自体は引き続き人確認待ちである。 |
| `SEJ1-SF-003` | medium | `closed` | `CFG-SF-001`と6 Roleを正本化し、7 Verificationと3非Product投影へ安定IDを割り当てた。 | 現行モデル内の参照は全件解決した。validatorの再発防止範囲は新規Finding `SEJ1-V03-X-002`で扱う。 |
| `SEJ1-FL-001` | high | `partially_closed` | 3 NeedすべてにValidationCaseを追加し、CSVへ投影した。 | 3件とも具体的`scenario_refs`と`success_measure_refs`がなく、暗所条件、利用者特性、低電池時の判断成功、安全Validationの妥当な尺度が未定義である。残留重大度はmedium。 |
| `SEJ1-FL-002` | medium | `open` | なし。 | `FLREQ-0001`は依然として同一条件で「開始または停止する」と記述され、現在状態または操作種別から期待次状態を一意に決めない。`evaluation.md`も1要求1義務を5/5 `sufficient`としている。 |
| `SEJ1-FL-003` | medium | `closed` | `evaluation.md`の現行メトリクスをProcess投影2件、`no_projection=0`へ更新した。 | v0.2の記述は「履歴」として分離され、現行JSONとの相反は解消した。 |
| `SEJ1-FL-004` | medium | `closed` | `CFG-FL-01`と3 Roleを正本化し、4 Verificationと3非Product投影へ安定IDを割り当てた。 | 現行モデルの役割・構成参照は解決した。validator範囲は新規Findingで扱う。 |
| `SEJ1-MB-001` | high | `partially_closed` | 6 NeedすべてにValidationCaseを追加し、CSVへ投影した。 | 6件すべてでScenario・Success Measure参照が空である。特に安全NeedのValidationが「保護動作を試験できること」のStakeholder受入れに留まり、危害低減の妥当性確認とRequirement Verificationを十分に分離できていない。残留重大度はmedium。 |
| `SEJ1-MB-002` | high | `partially_closed` | `MBSTR-0001`から`MBBEH-0006`と`MBREQ-0007`を除外し、`MBSTR_OPS-0001`へ人の運用BehaviorとRequirementを配分した。CSVの`performs`／`satisfies`方向も修正した。 | `MBREQ-0007.allocation_candidate_refs`は依然として`MBSTR-0001`を参照する。Structure側の正本関係は直ったが、Requirement側の配分候補に物理製品への矛盾が残る。残留重大度はmedium。 |
| `SEJ1-MB-003` | medium | `open` | なし。 | `MBREQ-0006`は「電池セルまたは電力変換部」と「受電経路または給電経路」の対応を定めないままで、`evaluation.md`も1要求1義務を8/8 `sufficient`としている。 |
| `SEJ1-MB-004` | medium | `partially_closed` | 航空の3 Obligationを`EPR-MB-008A/B/C`と3 Documentation Requirementへ1対1で分割した。 | 原子性は改善したが、義務主体である航空旅客の運用行動についてOperational投影または境界外とする`no_projection`理由がない。Documentationは通知責任を表すが、旅客の禁止行動そのものの責任を表さない。 |
| `SEJ1-MB-005` | medium | `closed` | `CFG-MB-CANDIDATE`と5 Roleを正本化し、8 Verificationと7非Product投影の参照を解決した。 | 現行モデルの参照は解決した。validator範囲は新規Findingで扱う。 |

## 新規Finding

### `SEJ1-V03-X-001`：Validationの存在検査が意味品質を保証しない

| 項目 | 内容 |
|---|---|
| 重大度 | medium |
| 対象 | Schema／validator、3製品 |
| 規則 | Q-STK-03、Q-VV-02、C-VAL-01 |
| 根拠 | `semantic_errors()`はNeedにValidationCaseまたはSuccess Measureが存在することと双方向参照だけを確認する。全14 ValidationCaseは`scenario_refs=[]`、`success_measure_refs=[]`だが検査を通る。受入れ基準を「受入可否を判定できる」へ弱めた変異ケースもエラー0件だった。 |
| 影響 | 空に近いValidationCaseを追加するだけでNeed Validation率を100%にでき、Requirement Verificationと異なるStakeholder価値確認が実質的にない状態を閉鎖扱いできる。 |
| 最小修正 | 少なくとも`operational_context`の具体性、代表Stakeholder、ScenarioまたはSuccess Measure、観測可能な受入れ基準候補のいずれを必須にするか規則化する。安全NeedではRequirement再試験だけをValidationとして数えない意味検査を追加する。 |

### `SEJ1-V03-X-002`：Verification責任・構成と配分候補がvalidatorの検査外

| 項目 | 内容 |
|---|---|
| 重大度 | medium |
| 対象 | Schema／validator、3製品 |
| 規則 | Q-VV-04、Q-STR-03、Q-TRC-02、C-CTX-01 |
| 根拠 | 現行モデルのRole・Configurationは解決するが、validatorは`verification_cases[].responsible_role_ref`と`.configuration`を検査しない。`VER_SF-0001`を未定義`ROLE-NOT-FOUND`／`CFG-NOT-FOUND`へ変異してもエラー0件だった。`requirements[].allocation_candidate_refs`も検査せず、現行`MBREQ-0007`の`MBSTR-0001`参照を見逃す。 |
| 影響 | v0.3で人が修正した責任・構成・配分の整合が、次の生成で退行しても`PASS`する。 |
| 最小修正 | VerificationのRole／Configuration解決、Requirementのallocation target解決、Structure側`requirement_refs`との整合、Behavior performerとStructure performerの整合を意味検査へ追加する。 |

### `SEJ1-V03-MB-001`：モバイルバッテリー評価文書の機械検証値がv0.2のまま

| 項目 | 内容 |
|---|---|
| 重大度 | medium |
| 対象 | `mobile-battery/evaluation.md` |
| 規則 | Q-OUT-03 |
| 根拠 | 文書冒頭はv0.3を125 ID・172 Traceと報告する一方、「機械検証」表は103 IDと「CFG／ROLEを外部プレースホルダーとして除外」と記述する。現行JSONでは構成と役割は正本内要素である。 |
| 影響 | Closure後の参照解決状態を同じ評価文書が相反して説明し、Reviewerがv0.3の検証範囲を誤認する。 |
| 最小修正 | 機械検証表をv0.3結果へ再投影するか、v0.2履歴節へ移して現行結果と明確に分離する。 |

## 製品別Closure判定

### スマート扇風機

`partially_closed / revise`。無線のSupplier情報入手と内部制度判断の分離、構成・Role解決は閉鎖した。Need ValidationはID経路として成立したが、具体的な代表シナリオと成功尺度が弱いため、SE GateをPassへ変更しない。

### 懐中電灯

`partially_closed / revise`。Need Validation、Process投影、構成・Roleは構造上改善した。`FLREQ-0001`の開始／停止の曖昧性と自己評価の5/5判定が残るため、Closure未完了である。

### モバイルバッテリー

`partially_closed / revise`。人の隔離行動は運用Structureへ移されたが、`MBREQ-0007`の配分候補が物理製品を参照する。`MBREQ-0006`の代替条件と航空旅客のOperational投影も残る。

## 次回再レビューの最小条件

1. ValidationCaseに代表ScenarioまたはSuccess Measureを追加し、特に安全NeedでVerificationとの差を説明する。
2. `FLREQ-0001`と`MBREQ-0006`を分割するか、状態・入力と期待応答の一意な対応を定義する。
3. `MBREQ-0007.allocation_candidate_refs`を`MBSTR_OPS-0001`へ修正する。
4. 航空旅客の3義務へOperational投影または境界外理由を個別に記録する。
5. validatorへVerification Role／Configurationと配分意味検査を追加し、評価文書を最新結果から再投影する。

法的適用、安全境界、規格適合、認証または市場投入判断は、引き続き権限を持つ人による確認対象である。
