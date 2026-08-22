# 独立SE Coherence Review（J1）

## 結論

3製品とも、合成Schema、主要ID解決および`09_traceability.csv`の決定的生成は`PASS`した。一方、SEの意味Gateは3製品とも`revise`と判定する。共通理由は、全Needの`success_measure_refs`と`validation_case_refs`が空で、`validation_cases`も0件であるにもかかわらず、Requirementに対するVerificationの網羅だけでV&Vを`sufficient`としているためである。これはStakeholder価値の妥当性確認を含まないFalse Pass候補である。

| 製品 | Schema・主要ID | 非Product投影の型 | SE意味判定 | 現行Gateの扱い |
|---|---|---|---|---|
| スマート扇風機 | `pass` | 2/2一致 | `revise` | `reviewable_40_candidate`を未承認とする |
| 懐中電灯 | `pass` | 2/2一致 | `revise` | `reviewable_40_candidate`を未承認とする |
| モバイルバッテリー | `pass` | 4/4一致 | `revise` | `reviewable_40_candidate`を未承認とする |

この判定は法的適用性、規格適合、安全性または認証を判断するものではない。

## レビューメタデータ

| 項目 | 内容 |
|---|---|
| Review Tier | `J1` |
| Reviewer | 生成担当とは別の独立SE Reviewerサブエージェント |
| モデル | Codex（GPT-5系。正確なデプロイ識別子はReviewerから取得不能） |
| レビュー日 | 2026-08-22（Asia/Tokyo） |
| 基準 | `hierarchical-se-prompt/04_QUALITY_RULES.md`、`17_FORTY_POINT_GATE.md`、`18_AI_EVALUATION_PROTOCOL.md`、Compliance Schema v0.2.0、`04_COMPLIANCE_QUALITY_RULES.md`、`09_TRACEABILITY_CANONICAL_RULES.md` |
| 独立性 | モデル本体を編集せず、他Reviewerとの事前協議を行わずに判定した |

## 機械検査と意味検査の分離

`validate_candidate.py`を各モデルへ実行し、保存済みCSVを同じJSONから再生成した一時CSVとSHA-256で比較した。

| 製品 | Schema・意味参照検査 | 収集ID | 派生関係 | 保存CSVとの完全一致 | Need→Validation | Requirement→Verification |
|---|---|---:|---:|---|---:|---:|
| スマート扇風機 | `PASS` | 72 | 89 | `true` | 0/5 | 7/7 |
| 懐中電灯 | `PASS` | 59 | 72 | `true` | 0/3 | 5/5 |
| モバイルバッテリー | `PASS` | 103 | 150 | `true` | 0/6 | 8/8 |

CSVの全`source_id`と`target_id`は正本内で解決し、型付き直接参照からの再生成結果も一致した。したがって、以下のFindingは文字列IDの欠落ではなく、関係の意味、要求品質、V&V範囲または評価記録の問題である。ただし、Verificationの役割・構成参照はCSV対象外であり、別途Findingとしている。

## スマート扇風機

### 判定

`revise`。Need→Requirement→Behavior／Structure→Verificationの文字列経路は解決するが、Needの妥当性確認経路がなく、無線法規候補の投影も義務主体の内部確認責任を保持していない。

| Finding ID | 重大度 | 規則 | 根拠 | 影響 | 最小修正 |
|---|---|---|---|---|---|
| `SEJ1-SF-001` | high | Q-STK-03、Q-VV-02、40点Gate Hard Blocker | `NEED_SF-0001`～`0005`は`success_measure_refs=[]`、`validation_case_refs=[]`で、`validation_cases`は0件。一方、`quality_summary`と`evaluation.md`はVerification 7/7をV&V `sufficient`としている。 | 利用者が送風操作を理解できるか、静音が就寝価値を満たすか、保守状態が作業価値を満たすかを確認できない。重要評価軸の欠落を見逃すFalse Passになる。 | 主要Needごとに成功尺度または代表運用シナリオを対象にするValidationCase候補を接続し、未確定基準は人確認事項として残す。CSVとGate計数を再生成する。 |
| `SEJ1-SF-002` | high | C-EPR-01、C-EPR-02、Q-REQ-01 | `OBL-SF-003`の義務主体は「無線機能の設計および市場投入責任者候補」で、必要結果は免許要否、適合経路、表示情報の確認である。現在の非Evidence投影は、供給者から情報を得る`SUPREQ-SF-RADIO-CONFORMITY`だけである。 | Supplier情報の入手を、設計・市場投入責任者による免許／免許不要条件の判断と誤同一視し、mandatory候補の工学投影を完全と数えてしまう。 | Supplier投影を残し、責任者が対象構成について免許要否・適合経路・表示を確認する型付き`process_requirement`を追加する。両者を同じObligationへ戻し、EvidenceRequirementを判断記録へ接続する。 |
| `SEJ1-SF-003` | medium | Q-VV-04、Q-TRC-02、Q-BEH-03 | Verificationの`responsible_role_ref`は「試験担当者（未決定）」等の自由文字列で、`CFG-SF-001`も正本内要素へ解決しない。2件の`projection_targets[]`は`responsible_role_ref=null`である。 | 誰が、どの構成を、どの責任で検証・法規確認するかを機械的に追跡できず、引継ぎ時に責任境界を失う。 | 役割と構成を正本または明示した外部レジストリへ登録し、安定IDで参照する。非Product投影にも責任役割候補を割り当てる。 |

非Product投影について、`projection_kind`と`target_kind`の文字列型は2件とも一致し、参照IDも解決した。`SEJ1-SF-002`は型エラーではなく、Supplier投影だけでは義務の意味を保存できないという分類・網羅性のFindingである。

## 懐中電灯

### 判定

`revise`。主要IDは解決し、v0.2のProcess投影型も正しい。しかしNeedの妥当性確認がなく、1要求1義務の自己判定と評価文書のv0.2整合に修正が必要である。

| Finding ID | 重大度 | 規則 | 根拠 | 影響 | 最小修正 |
|---|---|---|---|---|---|
| `SEJ1-FL-001` | high | Q-STK-03、Q-VV-02、40点Gate Hard Blocker | `FLNEED-0001`、`0002`、`0004`は成功尺度・Validation参照が空で、`validation_cases`は0件。5件あるのはRequirement Verificationだけである。 | 片手操作、低電池時の予測可能性、異常発熱からの保護というStakeholder価値を代表利用環境で確かめられず、V&V `sufficient`は過大判定になる。 | 3 Needを対象に、片手操作シナリオ、低電池通知後の利用者判断シナリオ、保護状態の危害低減シナリオのValidationCase候補または成功尺度を追加し、双方向参照とCSVを更新する。 |
| `SEJ1-FL-002` | medium | Q-REQ-03、Q-REQ-04、JA-REQ-02、JA-REQ-03 | `FLREQ-0001`は同じ条件「スイッチを操作したとき」に対し「開始または停止する」とし、事前状態と選択規則を示さない。`evaluation.md`は5/5を1要求1義務としている。 | 開始と停止のどちらが期待結果かを試験入力だけから一意に決められず、`FLV-0001`の合否判定が状態依存で曖昧になる。 | 開始要求と停止要求へ分割するか、現在状態と操作種別から次状態を一意に定める単一の切替要求・状態表へ修正し、BehaviorとVerificationを追従させる。 |
| `SEJ1-FL-003` | medium | Q-OUT-03、C-EPR-02 | `evaluation.md`のComplianceメトリクスには`no_projection: 2`が残るが、現行JSONでは`EPR-FL-DENAN-PROCESS-01`と`EPR-FL-CSPSA-PROCESS-01`が型付きProcess投影であり、文書末尾にもv0.2移行済みと記載される。 | 同一評価文書がv0.1とv0.2の相反する投影状態を報告し、ReviewerがProcess Requirementの有無を誤認する。 | メトリクス表、C-EPR-02根拠、結論を現行JSONから再投影し、`no_projection=0`、Process投影2件へ統一する。 |
| `SEJ1-FL-004` | medium | Q-VV-04、Q-TRC-02、Q-BEH-03 | Verificationの役割文字列と`CFG-FL-01`は正本内要素へ解決せず、2件のProcess投影は`responsible_role_ref=null`である。 | 検証責任と事業者プロセス責任をIDで割り当てられず、プロセス投影の実行主体を自動検査できない。 | 役割・構成の正本または外部レジストリを定義し、VerificationとProcess投影を安定IDへ接続する。 |

非Product投影は2件とも`process_requirement`として型一致し、製品要求への偽装もない。型分類そのものは`pass`である。

## モバイルバッテリー

### 判定

`revise`。機械Traceは最も豊富だが、製品構造が人の運用行動を実行・充足するという意味矛盾がCSVへ正規に投影されている。Need Validation欠落と合わせて、現在の`reviewable_40_candidate`は受け入れられない。

| Finding ID | 重大度 | 規則 | 根拠 | 影響 | 最小修正 |
|---|---|---|---|---|---|
| `SEJ1-MB-001` | high | Q-STK-03、Q-VV-02、40点Gate Hard Blocker | `MBNEED-0001`～`0006`は成功尺度・Validation参照が空で、`validation_cases`は0件。`evaluation.md`はVerification 8/8だけでV&Vを`sufficient`としている。 | 給電状態を利用者が理解できるか、損傷品隔離手順が再使用防止価値を満たすか、販売責任者が判断可能かを妥当性確認できない。 | 6 Needを代表利用・保守・販売判断シナリオのValidationCaseまたは成功尺度へ接続し、Verification率とValidation率を別指標で再判定する。 |
| `SEJ1-MB-002` | high | Q-BEH-03、Q-STR-03、Q-TRC-03、Q-REQ-02 | `MBREQ-0007`の主体と`MBBEH-0006.performer_candidate_refs`は`MBSTK-0003`である一方、`MBSTR-0001`は`MBBEH-0006`と`MBREQ-0007`を参照する。CSVは`MBSTR-0001 performs MBBEH-0006`および`MBSTR-0001 satisfies MBREQ-0007`を出力する。 | 物理製品が保守・廃棄担当者の隔離行動を実行・充足する矛盾した責任配分となり、IDが解決するほど誤ったTraceが強化される。 | `MBSTR-0001`から人の運用Behavior／Requirement参照を外し、運用者または運用プロセスのStructure候補へ配分する。CSVを再生成し、performerとStructureの一致検査を追加する。 |
| `SEJ1-MB-003` | medium | Q-REQ-03、Q-REQ-04、JA-REQ-02、JA-REQ-03 | `MBREQ-0006`は「電池セルまたは電力変換部」の温度条件と「受電経路または給電経路」の遮断を1文に持つが、入力部位と遮断対象の対応を定めない。自己評価は8/8を1要求1義務としている。 | 4通りに読め、どの経路を遮断すれば合格かが`MBVER-0006`で一意にならない。 | 部位・運転状態ごとの原子要求へ分割するか、温度異常源から遮断対象への一意な対応表を要求の参照対象として定義する。 |
| `SEJ1-MB-004` | medium | C-EPR-01、C-EPR-02、Q-REQ-03 | `EPR-MB-008`は、持込み個数・容量、機内充電禁止、機内給電禁止という3 Obligationを、1件の`DOC-MB-AIR-USE-RESTRICTIONS`の「適用可能な制限と確認事項」へ集約する。型はDocumentationで一致するが、3つのprohibitionの個別結果と利用者運用責任を保存しない。 | 1件の曖昧な文書要求が3義務の投影完了として数えられ、各禁止事項の欠落を検出できない。 | 3義務を個別のDocumentation要件または追跡可能な3節へ分ける。製品境界外の旅客行動にはOperational投影を置くか、対象外なら`no_projection`理由を義務ごとに記録する。 |
| `SEJ1-MB-005` | medium | Q-VV-04、Q-TRC-02、Q-BEH-03 | Verificationの`ROLE-*`と`CFG-MB-CANDIDATE`は正本内要素へ解決せず、4件の非Product投影は`responsible_role_ref=null`である。 | 安全試験、法規検査、文書作成、Supplier情報入手の責任分界を機械的に確認できない。 | 役割・構成の正本または外部レジストリを追加し、Verificationと全非Product投影を安定IDへ接続する。 |

非Product投影はProcess 1件、Documentation 2件、Supplier 1件の全4件で文字列型と参照IDが一致した。`SEJ1-MB-004`は構造上の型不一致ではなく、3つの異なる義務を1つの一般化文書へ縮約した意味欠落である。

## Gate再判定

| Gate軸 | スマート扇風機 | 懐中電灯 | モバイルバッテリー |
|---|---|---|---|
| Stakeholder→Need | `sufficient` | `sufficient` | `sufficient` |
| Need→Requirement | `sufficient` | `sufficient` | `sufficient` |
| Requirement→Behavior／Structure | `weak` | `weak` | `fail`（`MBREQ-0007`責任矛盾） |
| Requirement→Verification | `sufficient` | `sufficient` | `sufficient` |
| Need→Validation／成功尺度 | `missing` | `missing` | `missing` |
| 1要求1義務 | `sufficient` | `weak` | `weak` |
| 非Product投影型 | `sufficient` | `sufficient` | `sufficient` |
| 非Product投影意味 | `weak` | `sufficient` | `weak` |
| 独立J1結論 | `revise` | `revise` | `revise` |

Requirement→Behavior／Structureをスマート扇風機と懐中電灯で`weak`とした理由は、各モデルが1件のシステム境界Structureだけを持ち、全Requirementを同じStructureへ接続しているためである。これは初稿の過剰詳細化を避ける点では妥当だが、現行評価の「100%接続」を、責任配分や実現方法まで十分であるという意味には使用できない。

## 修正後の再レビュー条件

1. `SEJ1-*-001`を修正し、Need→Validationまたは成功尺度の実在Traceと別建ての計数を示す。
2. `SEJ1-SF-002`、`SEJ1-MB-002`および`SEJ1-MB-004`を修正し、投影と責任主体の意味を保存する。
3. 要求文の分割または状態・対応表によって`SEJ1-FL-002`と`SEJ1-MB-003`を解消する。
4. JSONから`09_traceability.csv`と`evaluation.md`を再投影し、Schema／意味検査を再実行する。
5. 法規適用、安全境界、認証または適合の判断は、引き続き権限を持つ人へ残す。
