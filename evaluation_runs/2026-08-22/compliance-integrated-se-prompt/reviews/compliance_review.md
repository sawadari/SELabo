# J1独立Compliance Review

## 結論

3製品とも構造検証には合格し、AIだけで適用、適合、PSE表示、無線認証、UN 38.3適合または証明書取得を確定していない。全Applicability Assessmentが`uncertain`、`human_confirmation_required: true`で、Evidence ItemとAttestationを作っていない点は妥当である。

一方、法規Sourceの同一性、法規条項から工学要求への導出、法的義務と社内統制の区別に修正が必要である。J1判定は次のとおりとする。

| 製品 | J1判定 | High | Medium | Low |
|---|---|---:|---:|---:|
| スマート扇風機 | `revise` | 0 | 3 | 0 |
| 懐中電灯 | `revise` | 1 | 1 | 1 |
| モバイルバッテリー | `revise` | 1 | 2 | 0 |

本レビューで主要失敗条件に相当する架空原典、AI単独の正式適用判断、架空証拠またはFalse Certification Claimは検出しなかった。したがってモデルの破棄ではなく、下記のsource patch後にJ1再レビューすることを推奨する。

## レビュー条件

| 項目 | 内容 |
|---|---|
| review_tier | `J1`：生成担当とは別のCompliance Reviewer |
| reviewed_as_of | 2026-08-22 JST |
| 対象 | v0.2の3製品`candidate_model.json`、各`evaluation.md` |
| 規則 | `04_COMPLIANCE_QUALITY_RULES.md`、`09_TRACEABILITY_CANONICAL_RULES.md` |
| 一次情報方針 | e-Gov、METI、総務省系、消費者庁、国土交通省、UNECEの公式情報だけを再確認 |
| 非実施 | 法的助言、規制当局照会、製品分類の確定、規格適合判定、認証判定、実機試験 |

`scripts/validate_candidate.py`を3モデルへ実行し、Schemaと意味的参照はすべてPASSした。導出Traceはスマート扇風機89、懐中電灯72、モバイルバッテリー150関係で、参照切れはなかった。このPASSは法的正確性やSource→Requirementの意味妥当性を保証しない。

## 横断所見

### CR-J1-X-001 — 自動発見の網羅性を立証できない

- 重大度：`Medium`
- 対象：3製品共通
- 根拠：各モデルには採用したSource候補はあるが、製品構成ファクト、探索語、探索した公式台帳、候補Sourceの採否理由、除外理由、探索打切り条件を残すdiscovery logがない。したがって「製品ごとに適合・法規を自動的に見つけた」ことは示せても、「必要な候補を漏れなく見つけた」ことは示せない。
- 影響：選択されたObligationの内部Traceが100%でも、未発見の法規・規格・認証制度が分母に入らないため、coverageが過大評価される。
- 最小修正：製品ごとに`regulatory_discovery_log`を追加し、構成・市場・用途・事業者役割、公式探索先、query/as-of、候補Source、採用・除外・保留理由、人の確認状態を記録する。総合判定は「候補集合」であり、法規担当者がinventoryを承認するまで網羅性を主張しない。
- 参照：[METI 電気用品安全法トップ](https://www.meti.go.jp/policy/consumer/seian/denan/)、[国土交通省 機内持込・お預け手荷物の危険物](https://www.mlit.go.jp/koku/koku_fr2_000007.html)

## スマート扇風機

### 判定

`revise`。PSE扇風機候補、10°条件、電波法第4条を製品固有候補として見つけ、3件すべてを`uncertain`に留めた境界は適切である。ただし、法的義務に含まれない記録保持の混入、原文からの保守的強化、無線の複数制度を一つのObligationへ集約した点を修正する必要がある。

### SF-J1-001 — 法第8条第1項の義務へ記録保持を混入

- 重大度：`Medium`
- 関連ID：`PRV-SF-001`、`NRM-SF-001`、`OBL-SF-001`、`EPR-SF-002`、`EVR-SF-008`
- 根拠：Source chainは電気用品安全法第8条第1項の技術基準適合義務であるのに、`OBL-SF-001.required_outcome`は「必要な記録を保持する」まで法的Required Outcomeとして加えている。自主検査と検査記録は同条第2項および施行規則の別の根拠である。
- 影響：法的義務と組織のAssurance controlが一つのObligationへ混在し、監査時にどの記録が法定か説明できない。
- 最小修正：`OBL-SF-001`を「技術基準へ適合させる」に限定する。法定検査記録を扱うなら第8条第2項と施行規則のSource/Provision/NormativeStatement/Obligationを追加する。任意の適合確認記録なら`binding_basis`を法的義務とせず、AssuranceまたはProcess controlとして分離する。
- 参照：[e-Gov 電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234?occasion_date=20260611)、[METI 自主検査](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_07.html)

### SF-J1-002 — 「容易に転倒しない」を無注記で「転倒しない」へ強化

- 重大度：`Medium`
- 関連ID：`PRV-SF-002`、`NRM-SF-002`、`OBL-SF-002`、`REQ_SF-0007`、`VER_SF-0007`
- 根拠：METI別表第八2(41)イ(イ)は、通常使用状態でいずれの方向へ10°傾けても「容易に転倒しない」と記述する。モデルは`REQ_SF-0007`で「転倒しない」と絶対条件へ変換し、保守的強化または解釈であることを導出根拠に残していない。10°という数値と製品候補の選択自体は公式情報と一致する。
- 影響：原典要約と工学的上乗せ条件の境界が曖昧になり、要求不適合がそのまま法規不適合と誤読される可能性がある。
- 最小修正：NormativeStatementには原典意味を保持し、Requirement側で`conservative_strengthening`等の導出種別と承認者を明記する。または適用する試験方法・判定基準を原典の関連附表まで確認して、受入れ基準を正確に定義する。
- 参照：[METI 技術基準省令解釈 別表第八](https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku/beppyoudai8_260601.pdf)、[METI 特定電気用品以外の電気用品一覧](https://www.meti.go.jp/policy/consumer/seian/denan/non_specified_electrical.html)

### SF-J1-003 — 電波法の免許、適合経路、表示を一つの原子義務へ集約

- 重大度：`Medium`
- 関連ID：`PRV-SF-003`、`NRM-SF-003`、`OBL-SF-003`、`EPR-SF-005`、`SUPREQ-SF-RADIO-CONFORMITY`
- 根拠：`PRV-SF-003`は第4条だけで、NormativeStatementは無線局免許を受ける義務と例外を表す。一方、ObligationとSupplier targetは免許要否、技術基準適合経路、表示情報を一つにまとめる。第4条ただし書は適合表示無線設備を参照するが、特定無線設備、技術基準適合証明・工事設計認証、表示の具体的根拠は第三章の二や関連省令・設備分類の確認が必要である。
- 影響：採用モジュールの制度経路と最終製品・無線局の免許要否を同一判断として扱い、供給者資料だけで最終適用性が閉じるように見える。
- 最小修正：免許要否、特定無線設備の適合経路、表示確認を別NormativeStatement/Obligationへ分け、それぞれ具体的Provisionへ接続する。無線方式、周波数、空中線電力、認証番号、表示、組込み条件を人確認項目として保持し、Supplier資料は入力証拠であって最終判断ではないと明記する。
- 参照：[e-Gov 電波法 第4条・第三章の二](https://laws.e-gov.go.jp/document?lawid=325AC0000000131_20240401_504AC0100000052)

## 懐中電灯

### 判定

`revise`。電池・充電構成と事業者役割を未確定のままDENAN適用性を`uncertain`とし、CSPSA事故報告を製品挙動ではなくProcessへ投影した点は妥当である。Source同一性と製品要求・Assuranceの境界に修正が必要である。

### FL-J1-001 — 行政解説ページを`source_type: law`として記録

- 重大度：`High`
- 関連ID：`SRC-JP-DENAN`、`SRC-JP-CSPSA`、`PRV-JP-DENAN-08-1`、`PRV-JP-DENAN-08-2`、`PRV-JP-CSPSA-35-1`
- 根拠：`SRC-JP-DENAN.official_locator`はMETIの制度概要、`SRC-JP-CSPSA.official_locator`は消費者庁の事故情報制度ページであり、どちらも発行主体の公式説明だが法令本文ではない。モデルはこれらを`source_type: law`として、法第8条・第35条のProvision正本にしている。3年間保存や10日以内という情報も公式説明では確認できるが、法・施行規則等の正本Sourceと行政解説Sourceを分離していない。
- 影響：C-SRC-01/02のSource identityが崩れ、取得した原典と法令条項の版・有効日を再現できない。3件すべてのObligation provenanceへ波及する。
- 最小修正：e-Govの電気用品安全法・消費生活用製品安全法を`source_type: law`として追加し、必要な施行規則のSource/Provisionも追加する。現行のMETI/Caaページは`guideline`または`regulator_guidance`相当として残し、法令解釈・手続説明の根拠に使う。法令版を確定できない間はSource statusとProvision verificationを`unknown`または再確認待ちにする。
- 参照：[e-Gov 電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234)、[e-Gov 消費生活用製品安全法](https://laws.e-gov.go.jp/law/348AC0000000031)、[METI 電気用品安全法の概要](https://www.meti.go.jp/policy/consumer/seian/denan/act_outline.html)、[消費者庁 重大製品事故情報報告・公表制度](https://www.caa.go.jp/policies/policy/consumer_safety/centralization_of_accident_information/)

### FL-J1-002 — 適合状態を対象製品のConstraintとして投影

- 重大度：`Medium`
- 関連ID：`OBL-FL-DENAN-01`、`EPR-FL-DENAN-PRODUCT-01`、`FLREQ-0007`、`FLV-0007`
- 根拠：`FLREQ-0007`は対象蓄電池が「技術基準への適合状態を保持する」ことを製品Constraintとするが、これは物理・機能特性ではなく評価結果またはAssurance stateである。具体的技術基準条項はまだ選択されていないため、製品要求として直接検証できない。
- 影響：C-EPR-02のProduct/Assurance境界が曖昧になり、Compliance状態をSysML Product Requirementへ再包装することになる。
- 最小修正：現段階ではAssurance Requirementまたは`no_projection`理由へ変更し、適用する技術基準条項が人により決定された後、条項ごとに検証可能な製品Requirementへ投影する。`FLV-0007`は適合判定そのものではなく、適用基準・Evidence・評価結果のレビュー活動として保持する。
- 参照：[METI 基準適合確認](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_04.html)

### FL-J1-003 — v0.2モデルとevaluation.mdの投影メトリクスが不一致

- 重大度：`Low`
- 関連：`flashlight/evaluation.md`のCompliance Layer表とC-EPR-02判定、`EPR-FL-DENAN-PROCESS-01`、`EPR-FL-CSPSA-PROCESS-01`
- 根拠：評価文書は`no_projection: 2`および「プロセス義務はno_projection」と記録するが、現行v0.2モデルは2件とも型付き`process_requirement`で`projection_targets[]`へ解決している。
- 影響：J1 reviewerがどのモデル版の評価か判断できず、v0.2修正効果が評価指標へ反映されない。
- 最小修正：evaluation.mdのモデル版、Process投影件数、`no_projection`件数、C-EPR-02根拠、意味検証コマンド結果を現行v0.2へ同期する。
- 参照：`04_COMPLIANCE_QUALITY_RULES.md` C-EPR-02、`09_TRACEABILITY_CANONICAL_RULES.md` 非Product投影先

## モバイルバッテリー

### 判定

`revise`。400 Wh/Lの対象条件、2026-04-24の航空ルール、UN 38.3候補を製品固有に選び、3件すべてを`uncertain`に留めたことは妥当である。航空ルールの数値・禁止内容は国土交通省発表と一致する。ただし、一般的な法第8条から具体的な保護挙動へ飛ぶTraceと、UN Manualだけから義務主体を作るTraceは修正が必要である。

### MB-J1-001 — 一般的な技術基準適合義務から4件の具体的保護要求へ直接投影

- 重大度：`High`
- 関連ID：`PRV-MB-002`、`NRM-MB-002`、`OBL-MB-001`、`EPR-MB-001`、`MBREQ-0003`〜`MBREQ-0006`
- 根拠：Source chainは法第8条第1項の「適用される技術基準へ適合させる」という一般義務までで、採用する技術基準の版・条項はない。それにもかかわらず、過充電遮断、過放電遮断、出力異常遮断、温度異常時の経路遮断を一括して`compliance_obligation`由来とする。これらは安全Needからの候補としては合理的だが、法規由来を立証するには現行のリチウムイオン蓄電池技術基準の具体的Provisionと要求ごとの解釈が必要である。
- 影響：Trace CSV上は法規由来が解決しても、監査時にSource clauseまで戻れず、設計上の保守策と法定要求を区別できない。C-SRC-02、C-SRC-03、C-EPR-03のFalse Passにつながる。
- 最小修正：`MBREQ-0003`〜`0006`の安全Need由来は維持し、Compliance derivationは一旦外すか`interpretation_status: pending`の中間解釈へ接続する。採用する現行基準体系を人が決定後、別表第九/第十二等の具体的Provision→NormativeStatement→Obligation→個別EPRを作成し、各Requirementへ1対1または説明可能な単位で接続する。異なる基準体系を混用しない。
- 参照：[METI 対象非対象解釈例一覧](https://www.meti.go.jp/policy/consumer/seian/denan/subject01.html)、[METI 基準適合確認](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_04.html)、[METI 技術基準省令解釈 別表第九](https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku/beppyoudai9.pdf)

### MB-J1-002 — UN Manual単独で義務主体と供給者要求を導出

- 重大度：`Medium`
- 関連ID：`SRC-MB-004`、`PRV-MB-008`、`NRM-MB-008`、`OBL-MB-007`、`SUP-MB-UN38-TEST-SUMMARY`、`EVR-MB-007`
- 根拠：UN Manual 38.3.5は試験要約の内容を規定する。一方、「manufacturers and subsequent distributors of cells or batteries shall make available」という義務主体はUN Model Regulations 2.9.4(g)等の採用規則側にある。現モデルはManualだけから「製造者・流通関係者候補」を作り、さらに調達担当者の供給者要求へ投影している。`binding_basis: unknown`とした慎重さは妥当だが、Source chainは不足している。
- 影響：セル・電池の製造者/後続流通者、電池搭載製品の製造者、調達者の社内統制が混ざり、誰の法的義務か分からない。輸送モード・法域で取り込まれる版も確定できない。
- 最小修正：UN Model Regulations 2.9.4(g)または選定輸送モードの正式な取込み規則をSource/Provisionとして追加し、義務主体と対象をセル/電池単位で確認する。調達時の入手要求は法的ObligationではなくSupplier controlとして区別し、実在するtest summaryをEvidence Itemにするまで未実施状態を維持する。
- 参照：[UNECE Manual of Tests and Criteria Rev.8 files](https://unece.org/transport/dangerous-goods/rev8-files)、[UNECE Model Regulationsの2.9.4(g)を含む公式資料](https://unece.org/DAM/trans/danger/publi/unrec/rev20/track/Part_2_01.pdf)

### MB-J1-003 — 航空ルールを報道発表だけで直接法規として保持

- 重大度：`Medium`
- 関連ID：`SRC-MB-003`、`PRV-MB-005`〜`PRV-MB-007`、`APP-MB-002`、`OBL-MB-004`〜`OBL-MB-006`
- 根拠：国土交通省の2026-04-14報道発表は、4月24日から「2個（160 Wh以下）まで」「機内でモバイルバッテリーへ充電しない」「他機器へ充電しない」と明記しており、モデルの数値と禁止内容は一致する。同発表は根拠として告示と運用通達の改正を挙げるが、モデルにはその正式Source/Provisionがないまま`binding_basis: direct_regulation`としている。
- 影響：ルール内容は確認できても、適用便、用語、例外、経過措置、法的位置づけを正本へ戻せず、将来の改正影響解析が報道発表URLに依存する。
- 最小修正：国土交通省告示第581号を含む2026-04-24適用の告示本文と該当運用通達をSource/Provisionへ追加し、報道発表は行政説明Sourceとして残す。`assessment_context`には国内線・日本発着便等の対象範囲を人が確認して記録する。
- 参照：[国土交通省 報道発表](https://www.mlit.go.jp/report/press/kouku10_hh_000310.html)、[航空機による爆発物等の輸送基準等を定める告示（2026-04-24適用）](https://safetyp.cab.mlit.go.jp/wp-content/uploads/2026/04/01-%EF%BC%88%E7%88%86%E7%99%BA%E7%89%A9%E7%AD%89%E5%91%8A%E7%A4%BA%EF%BC%89%E5%91%8A%E7%A4%BA%E6%9C%AC%E6%96%87%EF%BC%88260424%EF%BC%89.pdf)

## 維持すべき点

- 8件のApplicability Assessmentはすべて`uncertain`で、人の確認を要求している。
- 13件のObligationは候補状態で、正式な適用・適合を宣言していない。
- Mandatory/Prohibition ObligationからEvidence RequirementへのTraceは途切れていない。
- Evidence Itemは0、Assessment Resultは`not_performed`、Attestationは0であり、計画中の証拠や認証を実在扱いしていない。
- v0.2ではProcess、Documentation、Supplier投影が型付き`projection_targets[]`へ解決し、直接参照からTraceを決定的に生成できる。

## 再レビュー受入条件

1. High Finding 2件をsource patchし、影響するNormativeStatement、Obligation、EPR、Requirement、Evidence Requirementを再生成する。
2. Medium Findingの法的義務とAssurance/Process/Supplier controlの境界を分ける。
3. 各製品にregulatory discovery logと人によるinventory確認状態を追加する。
4. `validate_candidate.py`を再実行し、各evaluation.mdの件数・判定をv0.2モデルへ同期する。
5. 修正後のモデルを生成担当とは別のCompliance ReviewerがJ1再評価する。

このレビューは候補モデルの品質評価であり、法的助言、製品分類の決定、規格適合、認証、PSE表示可否、航空輸送可否または市場投入承認ではない。
