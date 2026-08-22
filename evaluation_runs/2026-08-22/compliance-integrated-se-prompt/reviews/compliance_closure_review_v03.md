# v0.3 Compliance Closure Review

## 結論

v0.3 source patchは、初回J1 Finding 10件のうち5件を`closed`、5件を`partially_closed`にした。`open`は0件、新規Highは0件である。

| 状態 | 件数 |
|---|---:|
| `closed` | 5 |
| `partially_closed` | 5 |
| `open` | 0 |
| 新規High | 0 |

High Findingは、`MB-J1-001`を`closed`、`FL-J1-001`を`partially_closed`と判定する。後者は法令Sourceと行政解説Sourceの分離を完了したためHigh相当のSource identity問題は解消したが、3年間保存と10日以内報告の数値を支える下位法令Provisionが未登録であり、残余をMediumとして扱う。

3製品ともSchema・意味参照・決定的Trace CSVはPASSした。ただし、法令・規格inventory、適用性、版、対象構成は人確認待ちであり、Compliance J1 Gateは`revise`を維持する。これはPSE適合、電波法適合、UN 38.3適合、航空輸送可否または市場投入承認を意味しない。

## 再レビュー条件

| 項目 | 内容 |
|---|---|
| review_tier | `J1 closure review`：v0.3修正担当とは独立 |
| reviewed_as_of | 2026-08-22 JST |
| 対象 | 最新Schema、validator、3製品`candidate_model.json`、`evaluation.md`、`09_traceability.csv`、初回`compliance_review.md` |
| 一次情報 | e-Gov、METI、国土交通省、UNECEの公式情報のみ再確認 |
| 非実施 | 法的助言、規制当局照会、正式製品分類、規格適合判定、認証判定、実機試験 |

## 機械検証

`scripts/validate_candidate.py`を再実行し、既存CSVと再生成CSVのSHA-256を比較した。

| 製品 | validator | ID | Trace | 既存CSVと再生成CSV |
|---|---|---:|---:|---|
| スマート扇風機 | PASS | 87 | 103 | SHA-256完全一致 |
| 懐中電灯 | PASS | 67 | 77 | SHA-256完全一致 |
| モバイルバッテリー | PASS | 125 | 172 | SHA-256完全一致 |

v0.3 Schemaは、Configuration、Party/Role、Assurance Requirement、Source版確認状態、Regulatory Discovery Log、Assessment Resultの構成・有効性を型付き化した。validatorは非Product投影先、責任Role、Assessment/Evidence/Attestationの整合性、Source版未確認時のdefinitive outcome禁止を検査している。全モデルのEvidence ItemとAttestationは0件、Assessment Resultは`not_performed`であり、正式適合を作っていない。

## 初回Finding Closure Matrix

| Finding | 初回重大度 | Closure | 判定要旨 |
|---|---|---|---|
| `CR-J1-X-001` | Medium | `partially_closed` | Discovery Logを追加したが、原始queryと除外候補は未保存で、網羅性は未証明 |
| `SF-J1-001` | Medium | `closed` | 法第8条第1項Obligationから記録保持を除外 |
| `SF-J1-002` | Medium | `closed` | 「転倒しない」を`conservative_strengthening`として明示 |
| `SF-J1-003` | Medium | `partially_closed` | Supplier情報と製品責任者判断は分離したが、法規義務自体は未分割 |
| `FL-J1-001` | High | `partially_closed` | Source identityは修正したが、3年・10日の下位法令Sourceが不足 |
| `FL-J1-002` | Medium | `closed` | 適合状態をProduct RequirementからAssurance Requirementへ移動 |
| `FL-J1-003` | Low | `closed` | Process 2件、`no_projection` 0件へevaluationを同期 |
| `MB-J1-001` | High | `closed` | 4保護要求のCompliance derivationを除去し、安全Need由来へ戻した |
| `MB-J1-002` | Medium | `partially_closed` | Model Regulations Sourceを追加したが、義務主体・版・社内Supplier controlの境界が未完 |
| `MB-J1-003` | Medium | `partially_closed` | 告示Sourceを追加したが、正確な条項位置・運用通達・対象便の確認が未完 |

## 横断Finding

### CR-J1-X-001 — `partially_closed`

- 成立した修正：3製品に`regulatory_discovery_log`が追加され、公式探索先、候補Source、探索時刻、Disposition、人確認状態を記録した。全レコードは`on_hold`、`human_inventory_confirmation_state: pending`であり、自動探索の網羅性を確定していない。
- 残余：3製品とも`queries: []`で、Disposition理由も「初回run後に再構成し、原始query logと除外候補が未保存」と明記する。したがって自動発見の再現性と未発見候補を含むcoverageは依然として証明できない。
- 最小追加修正：次回runから探索開始前にログを生成し、製品構成ファクト、実行query、公式台帳、採用・除外・保留をSourceごとに記録する。人のinventory確認前は現在の`on_hold`を維持する。
- 公式探索先例：[METI 電気用品安全法](https://www.meti.go.jp/policy/consumer/seian/denan/)、[国土交通省 機内持込・お預け手荷物の危険物](https://www.mlit.go.jp/koku/koku_fr2_000007.html)、[UNECE Dangerous Goods](https://unece.org/transport/dangerous-goods)

## スマート扇風機

### SF-J1-001 — `closed`

`OBL-SF-001.required_outcome`は「対象となる電気用品を、適用される技術基準へ適合させる」に限定され、法第8条第1項へ法定記録保持を混入していない。`PROC-SF-PSE-TECH-CHECK`と`EVR-SF-008`は候補のProcess/Evidence controlとして分離され、適用性・人確認境界を維持している。

参照：[e-Gov 電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234?occasion_date=20260611)、[METI 自主検査](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_07.html)

### SF-J1-002 — `closed`

`REQ_SF-0007.derivation_sources`は、原典候補の「容易に転倒しない」を「転倒しない」へ変換したことを`derivation_kind: conservative_strengthening`として明示し、採用可否と判定方法を人が承認するよう修正した。10°条件はMETI別表第八2(41)イ(イ)と一致し、原典意味と工学上乗せを区別できる。

参照：[METI 技術基準省令解釈 別表第八](https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku/beppyoudai8_260601.pdf)

### SF-J1-003 — `partially_closed`

- 成立した修正：`SUPREQ-SF-RADIO-CONFORMITY`によるSupplier情報取得と、`PROC-SF-RADIO-ROUTE-CHECK`による製品責任者の免許要否・制度経路判断を分離した。Supplier資料だけで最終判断を閉じない構造になった。
- 残余：NormativeStatementは第4条の免許義務1件、Obligationも`OBL-SF-003` 1件のままで、免許要否、特定無線設備の技術基準適合証明・工事設計認証、表示を別NormativeStatement/Obligationと具体的Provisionへ分けていない。初回Findingの法規意味分割は未完である。
- 最小追加修正：無線仕様を決定後、第4条の免許・例外、第三章の二の適合経路、関連省令の設備分類・表示を別Source/Provision/NormativeStatement/Obligationへ分割する。現在の`uncertain`を維持する。
- 参照：[e-Gov 電波法 第4条・第三章の二](https://laws.e-gov.go.jp/document?lawid=325AC0000000131_20240401_504AC0100000052)

## 懐中電灯

### FL-J1-001 — `partially_closed`（High残余なし、Medium残余あり）

- 成立した修正：METI制度概要と消費者庁制度説明を`source_type: guideline`へ変更し、e-Govの電気用品安全法と消費生活用製品安全法を別の`source_type: law`として追加した。3 Provisionは法令Sourceへ接続し、初回HighのSource identity混同を解消した。版を確定せず`status: unknown`、`applicability_version_state: unconfirmed`とした境界も妥当である。
- 残余：`NRM-JP-DENAN-INSPECT-01.limit`の3年間は電気用品安全法施行規則第11条第3項、`NRM-JP-CSPSA-REPORT-01.limit`の10日以内は「消費生活用製品安全法の規定に基づく重大事故報告等に関する内閣府令」第3条が直接根拠である。現モデルはこれらの下位法令Source/Provisionを持たず、法第8条第2項と法第35条第1項だけへ数値を接続している。
- 影響：Source種別の虚偽は解消したが、数値義務のClause-level provenanceは未完である。
- 最小追加修正：上記2下位法令をSource、該当条項をProvisionとして追加し、該当NormativeStatementを法と下位法令の両方へ接続する。行政解説は解釈・手続補助として保持する。
- 参照：[e-Gov 電気用品安全法施行規則 第11条](https://laws.e-gov.go.jp/document?lawid=337M50000400084)、[e-Gov 重大事故報告等に関する内閣府令 第3条](https://laws.e-gov.go.jp/law/421M60000002047/)

### FL-J1-002 — `closed`

`FLREQ-0007`は削除され、`EPR-FL-DENAN-PRODUCT-01`は`assurance_requirement`として`ASSURE-FL-DENAN-CONFORMITY`へ接続された。具体的技術基準が確定するまで、適合状態を対象製品のConstraintとして表現しない。C-EPR-02のProduct/Assurance境界を回復した。

### FL-J1-003 — `closed`

`evaluation.md`はProcess投影2件、`no_projection` 0件へ更新され、v0.3 validatorの67 ID・77 Traceも記録している。初回の投影メトリクス不一致は解消した。

## モバイルバッテリー

### MB-J1-001 — `closed`

`MBREQ-0003`〜`MBREQ-0006`から`compliance_obligation`由来を除去し、安全Needだけを導出元として保持した。`EPR-MB-001`は一般的な法第8条義務を`ASSURE-MB-TECH-CRITERIA-SELECTION`へ投影し、採用する技術基準体系と個別要求の導出根拠を人が管理する。一般条項から具体的な過充電・過放電・出力・温度保護挙動へ飛ぶFalse Traceは解消した。

Evidence Requirementは安全Need由来の要求と将来選択する技術基準の双方に使える計画証拠として残るが、具体的保護要求が法規条項由来であるとは記述していない。採用体系が確定するまでAssurance Requirementと`uncertain`を維持する判断は妥当である。

参照：[METI 対象非対象解釈例一覧](https://www.meti.go.jp/policy/consumer/seian/denan/subject01.html)、[METI 基準適合確認](https://www.meti.go.jp/policy/consumer/seian/denan/procedure_04.html)

### MB-J1-002 — `partially_closed`

- 成立した修正：UN Manual 38.3.5に加え、UN Model Regulations 2.9.4(g)候補を`SRC-MB-006` / `PRV-MB-009`として追加し、test summary内容と義務主体側Sourceを分離する構造を作った。版・輸送モード・法的取込みは未確認としている。
- 残余1：`NRM-MB-008.bearer`は「リチウム電池または製品の製造者・流通関係者候補」のままである。2.9.4(g)は少なくとも確認した公式文面では、cells or batteriesのmanufacturers and subsequent distributorsを対象としており、製品製造者一般へ広げるには別根拠が必要である。
- 残余2：`SRC-MB-006`は2017年のRev.20資料へ接続し、Editionは未記録である。2026-08-22時点でUNECEはRev.24を公開している。適用輸送制度が採用する版は別途確認が必要だが、候補Source自身の版識別は可能である。
- 残余3：UN Model Regulationsは各国・各輸送モードの規則の基礎となるRecommendationsであり、それ自体を`source_type: regulation`と確定するのは強すぎる。`binding_basis: unknown`は維持されているためFalse applicabilityではないが、Source種別をRecommendation相当へ修正し、取込み規則を別Sourceにする必要がある。
- 最小追加修正：義務主体をcells/batteriesのmanufacturer/subsequent distributorへ限定したNormativeStatement候補に修正し、調達担当者の入手行為は内部Supplier controlとして区別する。候補版をRev.24等の識別可能な公式版へ更新し、採用輸送モードの取込みSourceを人が確定する。
- 参照：[UNECE Model Regulations Rev.24](https://unece.org/transport/dangerous-goods/un-model-regulations-rev-24)、[UNECE Rev.24 Volume I](https://unece.org/sites/default/files/2025-09/ST_SG_AC10_1_Rev24e_Vol%20I.pdf)、[UNECE Manual of Tests and Criteria](https://unece.org/transport/dangerous-goods/rev8-files)

### MB-J1-003 — `partially_closed`

- 成立した修正：国土交通省報道発表を`guideline`かつ版未確認として保持し、2026-04-24適用の告示候補を別の`SRC-MB-005`として追加した。航空の個数・容量、機内充電、他機器への給電を3つのDocumentation Requirementへ分割した。数値と禁止内容は国土交通省公式発表と一致する。
- 残余：`PRV-MB-005`〜`007`のcanonical locatorは「2026-04-24適用」の説明で、告示内の条・別表・特別規定等の位置を一意に示していない。Source自身も「国土交通省告示第581号等（対象範囲は未確認）」で、報道発表が言及する運用通達を追加していない。国内線・日本発着便という対象範囲もAssessment Contextへ確定記録していない。
- 最小追加修正：告示と運用通達のうち3義務を直接支える位置を特定し、Provision locatorへ記録する。`APP-MB-002`には便の範囲と例外を人確認後に追加する。それまでは`SRC-MB-005.status: unknown`、Applicability `uncertain`を維持する。
- 参照：[国土交通省 2026-04-14報道発表](https://www.mlit.go.jp/report/press/kouku10_hh_000310.html)、[航空機による爆発物等の輸送基準等を定める告示候補](https://safetyp.cab.mlit.go.jp/wp-content/uploads/2026/04/01-%EF%BC%88%E7%88%86%E7%99%BA%E7%89%A9%E7%AD%89%E5%91%8A%E7%A4%BA%EF%BC%89%E5%91%8A%E7%A4%BA%E6%9C%AC%E6%96%87%EF%BC%88260424%EF%BC%89.pdf)

## 新規Finding

### V03-J1-NEW-001 — Discovery Logの参照整合をvalidatorが検査しない

- 重大度：`Medium`
- 根拠：Schemaの`regulatoryDiscoveryRecord.candidate_source_refs`は一般的な文字列配列で、validatorの`semantic_errors()`はDiscovery Logを走査しない。未定義Source IDまたは未定義Configuration IDをDiscovery Logへ入れても、この箇所の意味参照検査では検出されない。また`queries`の空配列を許容し、全Sourceが採用・除外・保留のいずれかでDispositionされたことも検査しない。
- 現モデルへの影響：3製品の現在の`candidate_source_refs`と`configuration_ref`は目視上すべて解決するため、既存モデルの即時FAILではない。ただし`CR-J1-X-001`を将来自動閉鎖する仕組みとしては不十分である。
- 最小修正：validatorへDiscovery LogのConfiguration/Source参照解決、Source coverage、Disposition整合を追加する。原始queryが存在しない移行データは空配列ではなく、明示的な`query_log_state: unavailable_legacy_run`等で区別する。

## 文書同期観察

新規Highではないが、`evaluation.md`とモデル内Summaryにはv0.3 source patch前の文章が一部残る。

- 懐中電灯の`source_limitations`は「METIと消費者庁の公式説明ページだけを取得」とするが、v0.3モデルはe-Gov法令Sourceを追加済みである。
- モバイルバッテリーのC-SRC-02説明はProvision 8件とするが、現行モデルは`PRV-MB-009`を含む9件である。

重大度は`Low`。Closure Review結果を反映する際に、モデル版、Source/Provision件数、残余制約を同期する。

## Closure後の推奨Gate

- `generator`: 既存判定を維持
- `compliance`: `revise`
- `se`: 本レビュー対象外のため既存J1判定を維持
- `assurance`: 本レビュー対象外のため既存J1判定を維持
- `meta_judge`: `revise`

次に閉じる優先順は、(1) 懐中電灯の下位法令Provision、(2) UN 2.9.4(g)の主体・版・取込み、(3) 航空告示/運用通達の正確なlocator、(4) 電波法Obligation分割、(5) 次回runからの原始Discovery Log保存である。
