# v0.3.1 Compliance Closure Review

## 結論

v0.3.1の残件修正は、初回J1 Finding 10件のうち9件を`closed`、1件を`partially_closed`にした。`open`は0件である。v0.3で追加したDiscovery Log意味検証Findingも`closed`と判定する。

| 状態 | 件数 |
|---|---:|
| 初回Finding `closed` | 9 |
| 初回Finding `partially_closed` | 1 |
| 初回Finding `open` | 0 |
| v0.3新規Finding `closed` | 1 |
| v0.3.1新規High | 0 |
| v0.3.1新規Medium | 1（`closed`） |

懐中電灯の3年保存・10日報告、スマート扇風機の電波法分割、モバイルバッテリーの航空告示locatorと法的禁止／行政要請の分離は成立した。UN Model Regulations Rev.24についても`source_type: recommendation`、版、義務主体に加え、2.9.4(g)の適用範囲を限定する組込みボタン電池の例外と2003-06-30後という製造条件がNormative Statement、Obligation、Supplier Requirement、Evidence Requirementへ反映された。3製品のsource-patch Closure Gateはすべて`pass`とする。

3製品のApplicabilityは引き続き`uncertain`で、人による製品分類、版選定、輸送制度への取込み、対象構成および義務主体の確認を要する。本レビューの`pass`はsource-patchの閉鎖判定であり、PSE適合、電波法適合、UN 38.3適合、航空輸送可否、認証または市場投入承認を意味しない。

## 再レビュー条件

| 項目 | 内容 |
|---|---|
| review_tier | `J1 closure review`：v0.3.1修正担当とは独立 |
| reviewed_as_of | 2026-08-22 JST |
| 対象 | 初回・v0.3 Compliance Review、共通Schema/validator/exporter、3製品`candidate_model.json`、`evaluation.md`、`09_traceability.csv`、17–21投影 |
| 一次情報 | e-Gov、METI、国土交通省、UNECEの公式情報のみ確認 |
| 非実施 | 法的助言、規制当局照会、正式製品分類、規格適合判定、認証判定、実機試験 |

## 機械検証

最終スナップショットに対して`validate_candidate.py`を実行した。`09_traceability.csv`は一時出力へ再生成して既存CSVとSHA-256を比較し、`export_compliance_views.py --check`で17–21投影を検査した。

| 製品 | validator | ID | Trace | `09_traceability.csv` | 17–21 `--check` |
|---|---|---:|---:|---|---|
| スマート扇風機 | PASS | 98 | 132 | SHA-256完全一致 | PASS（5 files） |
| 懐中電灯 | PASS | 75 | 88 | SHA-256完全一致 | PASS（5 files） |
| モバイルバッテリー | PASS | 141 | 193 | SHA-256完全一致 | PASS（5 files） |

したがって、以下のFindingはcanonical JSONと投影の不一致ではなく、最新モデルの意味内容に対する判定である。

## 初回Finding Closure Matrix

| Finding | 初回重大度 | v0.3.1 Closure | 判定要旨 |
|---|---|---|---|
| `CR-J1-X-001` | Medium | `partially_closed` | Discovery Logの構造・意味検証は成立したが、legacy runの原始query・除外候補・人のinventory確認は復元されていない |
| `SF-J1-001` | Medium | `closed` | 法第8条第1項候補と記録保持を分離した状態を維持 |
| `SF-J1-002` | Medium | `closed` | 転倒要求の工学上乗せを`conservative_strengthening`として維持 |
| `SF-J1-003` | Medium | `closed` | 免許、工事設計認証、認証工事設計合致、表示権限を別Provision/Statement/Obligationへ分割 |
| `FL-J1-001` | High | `closed` | 3年保存と10日報告の下位法令Source/Provisionを追加し、数値のClause-level provenanceを回復 |
| `FL-J1-002` | Medium | `closed` | 未確定の適合状態をProduct Requirementへ戻していない |
| `FL-J1-003` | Low | `closed` | Process投影2件・`no_projection` 0件という初回残件は再発していない |
| `MB-J1-001` | High | `closed` | 一般的な法第8条から4保護要求へのFalse Traceは再発していない |
| `MB-J1-002` | Medium | `closed` | Rev.24、Recommendation種別、cells/batteries主体、2.9.4(g)の例外・製造日限定を分離して反映 |
| `MB-J1-003` | Medium | `closed` | 告示第27条／別表第18と行政要請を別Source/Provision/Obligationへ分離 |

## 横断Finding

### CR-J1-X-001 — `partially_closed`

- 成立した修正：3製品のDiscovery Recordは、すべての現行Sourceを`candidate_source_refs`で覆い、`configuration_ref`とmarketも解決する。`query_log_state: unavailable_legacy_run`、`queries: []`、`disposition: on_hold`、`human_inventory_confirmation_state: pending`として、存在しない探索履歴や網羅性を作っていない。
- 意味検証：Schemaは`query_log_state`を`complete`または`unavailable_legacy_run`へ限定する。validatorはConfiguration/market/Source参照、Source coverage、`complete`なのにqueryが空、legacyなのにqueryを記録する矛盾を検出する。
- 残余：原始query、除外候補、探索時点の製品構成ファクトは未保存で、人のinventory確認も未実施である。したがって自動発見の再現性と網羅性は証明されない。
- 最小修正：次回runから探索開始前にRecordを生成し、実行query、公式台帳、候補Sourceごとの採用・除外・保留理由を保存する。人がinventoryを確認するまで現在の`on_hold`を維持する。
- 公式探索先例：[METI 電気用品安全法](https://www.meti.go.jp/policy/consumer/seian/denan/)、[国土交通省 危険物手荷物情報](https://www.mlit.go.jp/koku/koku_fr2_000007.html)、[UNECE Dangerous Goods](https://unece.org/transport/dangerous-goods)

### V03-J1-NEW-001 — `closed`

v0.3で指摘した「Discovery Logの参照整合をvalidatorが検査しない」は閉鎖した。validatorは未定義Configuration、ComplianceScope外market、未定義candidate Source、Disposition RecordのないSource、query state矛盾を検出する。3製品のvalidator PASSと21投影のexport check PASSにより、現行Recordの構造・参照・投影一致も確認した。

## スマート扇風機

### SF-J1-001 — `closed`

`OBL-SF-001`は技術基準適合候補に限定され、法第8条第1項へ検査記録保持を混入していない。v0.3.1での再発はない。

参照：[e-Gov 電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234?occasion_date=20260611)

### SF-J1-002 — `closed`

`REQ_SF-0007`の「転倒しない」は、原典候補の「容易に転倒しない」に対する`conservative_strengthening`のままで、採用・判定方法を人確認へ残している。

参照：[METI 技術基準省令解釈 別表第八](https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku/beppyoudai8_260601.pdf)

### SF-J1-003 — `closed`

電波法候補は次の4段階へ原子化された。

| Provision | Normative Statement / Obligation | 法的モダリティ |
|---|---|---|
| 第4条 `PRV-SF-003` | 免許または法定例外の確認 `NRM/OBL-SF-003` | obligation / mandatory |
| 第38条の24 `PRV-SF-004` | 工事設計認証経路 `NRM/OBL-SF-004` | permission |
| 第38条の25 `PRV-SF-005` | 認証工事設計との合致 `NRM/OBL-SF-005` | obligation / mandatory |
| 第38条の26 `PRV-SF-006` | 義務履行後の表示権限 `NRM/OBL-SF-006` | permission |

第38条の24の認証申請可能性、第38条の25の合致義務、第38条の26の条件付き表示を同一の「認証済み」主張に潰していない。`APP-SF-003`は4 Statementを参照しつつ`uncertain`、全対象はlow confidenceかつ人確認必須である。Supplier情報取得、製品責任者の制度経路確認、Evidence Requirementにも4 Obligationが到達し、17–20投影とcanonical JSONは一致する。

参照：[e-Gov 電波法 第4条・第38条の24～26](https://laws.e-gov.go.jp/document?lawid=325AC0000000131_20240401_504AC0100000052)

## 懐中電灯

### FL-J1-001 — `closed`

`SRC-JP-DENAN-REG`（電気用品安全法施行規則）と`PRV-JP-DENAN-REG-11-3`（第11条第3項）を追加し、`NRM-JP-DENAN-INSPECT-01`の「検査の日から3年間」を法第8条第2項と施行規則の両方へ接続した。

`SRC-JP-CSPSA-ORDER`（重大事故報告等に関する内閣府令）と`PRV-JP-CSPSA-ORDER-03-1`（第3条第1項）も追加し、`NRM-JP-CSPSA-REPORT-01`の「知った日から10日以内」を法第35条第1項と内閣府令の両方へ接続した。公式一次情報の期限と一致する。法令Sourceは`regulation`、行政解説は`guideline`として分離され、適用性・版・対象区分は未確定のままである。

参照：[e-Gov 電気用品安全法施行規則](https://laws.e-gov.go.jp/document?lawid=337M50000400084)、[METI 自主検査](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_07.html)、[e-Gov 重大事故報告等に関する内閣府令](https://laws.e-gov.go.jp/law/421M60000002047/)

### FL-J1-002 — `closed`

未確定の技術基準適合状態を対象製品のProduct Requirementへ置かず、`ASSURE-FL-DENAN-CONFORMITY`へのAssurance投影として保持している。Applicability 2件は引き続き`uncertain`である。

### FL-J1-003 — `closed`

初回Findingの対象だった自主検査・事故報告のProcess投影は2件、`no_projection`は0件の状態を維持する。最新の09 Traceと17–21投影も決定的に再生成できる。

## モバイルバッテリー

### MB-J1-001 — `closed`

`MBREQ-0003`～`MBREQ-0006`は安全Need由来のままで、一般的な電安法第8条を具体的な過充電・過放電・出力・温度保護挙動の直接根拠に戻していない。技術基準体系の選定はAssurance Requirementへ分離されている。

参照：[METI 対象・非対象の解釈事例](https://www.meti.go.jp/policy/consumer/seian/denan/subject.html)、[METI 基準適合確認](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_04.html)

### MB-J1-002 — `closed`

- 成立した修正：`SRC-MB-006`は`ST/SG/AC.10/1/Rev.24`、`edition: Revision 24 (2025)`、`source_type: recommendation`になった。`PRV-MB-009`は2.9.4(g)を指し、`NRM-MB-008.bearer`は「セルまたは電池の製造者および後続流通業者候補」へ限定された。製品製造者一般へ拡張せず、調達側は`SUP-MB-UN38-TEST-SUMMARY`という内部Supplier controlへ分離している。
- 適用範囲：`NRM-MB-008`は2003-06-30後に製造されたcells/batteriesを`condition`と`limit`へ記録し、機器または回路基板へ組み込まれたbutton cellを`exceptions`へ記録した。`OBL-MB-007`にも同じ条件と例外が伝播する。
- 下流境界：`SUP-MB-UN38-TEST-SUMMARY`は、調達担当者が製造時点と組込みbutton cell例外を確認してから、適用される場合に試験要約を入手する候補である。`EVR-MB-007`も、製造時点または対象外根拠と例外該当性をEvidence propertyとして要求する。
- 人確認境界：`APP-MB-003.binding_basis: unknown`、decision `uncertain`で、採用輸送モード、法域への取込み、対象型式、供給者責任を確定していない。
- 機械確認：mobile validatorは141 ID・193 TraceでPASS、既存09 Traceと再生成CSVはSHA-256完全一致、17–21 export checkもPASSした。
- 参照：[UNECE Model Regulations Rev.24](https://unece.org/transport/dangerous-goods/un-model-regulations-rev-24)、[UNECE Rev.24 Volume I §2.9.4(g)](https://unece.org/sites/default/files/2025-09/ST_SG_AC10_1_Rev24e_Vol%20I_0.pdf)、[UNECE Manual of Tests and Criteria Rev.8](https://unece.org/transport/dangerous-goods/rev8-files)

### MB-J1-003 — `closed`

法的禁止候補は`SRC-MB-007`（告示別表第18）へ接続され、個数・容量は`PRV-MB-005`（告示第27条／別表第18の備考2・パワーバンク行）、機内でモバイルバッテリー自体を充電しない条件は`PRV-MB-006`（備考7）へ接続された。両者は`OBL-MB-004/005: prohibition`である。

他の電子機器への給電回避は`SRC-MB-008`（航空局No.111）と`PRV/NRM/OBL-MB-007/006`へ分離され、`modality`と`obligation_kind`は`recommendation`である。公式資料の「法律に基づく禁止事項ではない」という注記と一致し、`APP-MB-004`も別Assessmentとして`uncertain`を維持する。Documentation targetと`MBREQ-0011`の本文・`normative_level`も非法定要請と推奨を明示している。

参照：[国土交通省 2026-04-14報道発表](https://www.mlit.go.jp/report/press/kouku10_hh_000310.html)、[告示本文（第27条）](https://safetyp.cab.mlit.go.jp/wp-content/uploads/2026/04/01-%EF%BC%88%E7%88%86%E7%99%BA%E7%89%A9%E7%AD%89%E5%91%8A%E7%A4%BA%EF%BC%89%E5%91%8A%E7%A4%BA%E6%9C%AC%E6%96%87%EF%BC%88260424%EF%BC%89.pdf)、[告示別表第18（2026-04-24適用）](https://www.mlit.go.jp/common/001388681.pdf)、[航空局からのお知らせ No.111](https://www.mlit.go.jp/koku/content/001998054.pdf)

## v0.3.1新規Finding

### V031-J1-NEW-001 — `closed`：UN 2.9.4(g)の例外・製造日条件

- 重大度：`Medium`
- 対象：`NRM-MB-008`、`OBL-MB-007`、および18投影
- Closure根拠：公式Rev.24 2.9.4(g)の組込みbutton cell例外と2003-06-30後という製造条件を`NRM-MB-008`へ追加し、`OBL-MB-007`、`SUP-MB-UN38-TEST-SUMMARY`、`EVR-MB-007`まで意味を伝播した。正式適用は`APP-MB-003: uncertain`と人確認必須のままである。
- 機械確認：validator、09 Trace SHA-256一致、17–21 export checkはすべてPASSした。

新規Highはない。

## 文書同期観察

前回のLow観察は未閉鎖である。3製品の`evaluation.md`はv0.3.1 source patch後の最新件数を反映していない。

| 製品 | evaluationの旧記録 | 最新validator / Compliance件数 |
|---|---|---|
| スマート扇風機 | 87 ID / 103 Trace、Provision・Statement・Obligation各3 | 98 ID / 132 Trace、Provision・Statement・Obligation各6 |
| 懐中電灯 | 67 ID / 77 Trace | 75 ID / 88 Trace、Source 6 / Provision 5 |
| モバイルバッテリー | 125 ID / 172 Trace、Source 4 / Provision 8 / Applicability 3 | 141 ID / 193 Trace、Source 8 / Provision 9 / Applicability 4 |

重大度は`Low`。既存の初回C1・v0.2・v0.3履歴は上書きせず、v0.3.1 Closure節として最新件数、Source追加、残余Findingおよび本Gateを追記するのが最小修正である。

## 最終Gate

| 対象 | Gate | 理由 |
|---|---|---|
| スマート扇風機 source-patch closure | `pass` | 電波法の免許・認証経路・合致義務・表示権限を分離し、投影も一致 |
| 懐中電灯 source-patch closure | `pass` | 3年・10日の下位法令provenanceを追加し、投影も一致 |
| モバイルバッテリー source-patch closure | `pass` | 航空分離、UN 2.9.4(g)の主体・版・種別・例外・製造条件を反映し、下流投影も一致 |
| Compliance J1総合 | `revise` | v0.3.1新規Mediumは閉鎖したが、`CR-J1-X-001`のDiscovery completenessと全Applicabilityの人確認が残る |
| Meta-Judge推奨 | `revise` | Discovery inventoryを人確認し、evaluationを同期してから再判定 |

次の最小閉鎖順は、(1) 3製品`evaluation.md`へv0.3.1差分を追記、(2) 現在のDiscovery inventoryを人が確認、(3) 次回runで原始Discovery queryと候補別Dispositionを保存、(4) 製品構成確定後にApplicabilityを人が判定、である。
