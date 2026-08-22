# Strict blind C1 独立Compliance J1レビュー

## 1. 結論

**総合Gate: FAIL / revise**

3製品とも、raw query、探索時点、候補Source、採用・保留・除外理由をモデル内に保存し、全Applicabilityを`uncertain`かつ人確認`pending`に留め、適合・認証・市場投入承認を主張していない。この意味で、**製品に応じた候補の自動発見と人判断境界は成立している**。

ただし、意味品質には次の未解決点がある。

- モバイルバッテリーは、3本すべてのmandatory/prohibition chainで、法令・告示正本と行政解説又はUN Manualの役割を分離できていない。特にDENANの義務主体、UN 38.3 test summaryの義務根拠、日本の航空ルールの拘束根拠が、採用Sourceだけでは成立しない。
- 懐中電灯の`PRV-0002`は、現行の電気用品安全法施行令別表第二に存在しない正規位置を記録している。
- スマート扇風機の電波法chainは、無線局開設者の免許不要条件と、証明機関又は製品取扱業者の表示権限・義務を一つのNormative Statementへ寄せ、`PRV-0006`の要約も現行条文と一致しない。

したがって、構造・同期検査のPASSをCompliance J1の意味品質PASSへ読み替えてはならない。旧`compliance-integrated-se-prompt-blind-c1`は参考runであり、本レビューの件数、Gate及びstrict runの効果判定には含めていない。

## 2. 対象と判定基準

対象は次のstrict runだけである。

- `smart-fan/candidate_model.json`, `evaluation.md`, `09_traceability.csv`, `17`–`21`
- `mobile-battery/candidate_model.json`, `evaluation.md`, `09_traceability.csv`, `17`–`21`
- `flashlight/candidate_model.json`, `evaluation.md`, `09_traceability.csv`, `17`–`21`
- 共通Schema、validator、exporter
- `04_COMPLIANCE_QUALITY_RULES.md`及び`09_TRACEABILITY_CANONICAL_RULES.md`

主な判定観点は、C-SRC-01/02、C-APP-02/03、C-DISC-01、C-ASR-01、C-ATT-01、C-TRC-02及びC-GATE-01である。本レビューは適用性を確定せず、候補Source、主張の境界、追跡性及び人確認境界を評価する。

## 3. 機械的検証

2026-08-22の最新スナップショットに対して実行した。

| 製品 | validator | 正規trace再生成と09のSHA-256 | `export_compliance_views.py --check` |
|---|---|---|---|
| smart-fan | PASS (`ids=54`, `derived_relations=70`) | 一致 | PASS (`files=5`) |
| mobile-battery | PASS (`ids=57`, `derived_relations=67`) | 一致 | PASS (`files=5`) |
| flashlight | PASS (`ids=50`, `derived_relations=61`) | 一致 | PASS (`files=5`) |

この結果は、参照解決、09の決定的生成及び17–21の鮮度を示す。Sourceの法的役割、Provision locator及びNormative Statementの法的正確性は別判定である。

## 4. 横断結果

### 4.1 Discovery Log

| 製品 | RDL件数 / `complete` | 保存raw query数 | disposition | 判定 |
|---|---:|---:|---|---|
| smart-fan | 4 / 4 | 17 | adopted 2、on-hold 1、excluded 1 | 構造PASS |
| mobile-battery | 3 / 3 | 3 | adopted 3 | 構造PASS、意味revise |
| flashlight | 3 / 3 | 12 | adopted 2、on-hold 1 | 構造PASS |

全RDLに市場、構成、公式探索先、raw query文字列、候補Source、実行時点、disposition理由がある。全件で`human_inventory_confirmation_state=pending`であり、網羅性を確定していない。保存されたモデルだけでは各queryの外部実行receiptまでは再現できないため、本判定は「実行時queryとして記録された文字列が存在する」ことまでを確認したものである。

### 4.2 ApplicabilityとFalse claim境界

| 製品 | APP | EvidenceItem | AssessmentResult | Attestation | False conformity/certification claim |
|---|---|---:|---|---:|---|
| smart-fan | 3/3 `uncertain`・`pending` | 0 | 1件 `not_performed` | 0 | なし |
| mobile-battery | 3/3 `uncertain`・`pending` | 0 | 3件 `not_performed` | 0 | なし |
| flashlight | 2/2 `uncertain`・`pending` | 0 | 1件 `not_performed` | 0 | なし |

全モデルで`assurance_outcome=not_performed`、`not_a_compliance_approval=true`である。適合、認証取得又は市場投入可能との確定主張は見つからなかった。

## 5. 製品別レビュー

### 5.1 スマート扇風機 — revise

自動発見候補は、(1) DENAN法第8条、施行令別表第二第8号(41)及びMETI品目一覧、(2) 長期使用製品安全表示の省令第20条、(3) Wi-Fi搭載時の電波法候補である。消費生活用製品安全法の概要ページは、長期使用表示義務の直接根拠ではないとして明示的に除外した。定格消費電力、電源方式、Wi-Fi有無・周波数・空中線電力・モジュール、製造輸入主体が未確定であることも探索限界として記録されている。

DENANと長期使用表示は、法令正本と行政案内を別Sourceとして識別しており、APPも未確定である。電波法chainには次の修正が必要である。

#### Finding SF-C1S-001 — Medium — 電波法の義務主体と表示条項が混在

- **根拠:** `PRV-0005`は電波法第4条全体、`PRV-0006`は第38条の7第1項を参照するが、`NRM-0003`は「無線局を開設する者」に「免許不要条件に対応する表示が付された対象無線設備を使用する」と一括している。現行第4条第3号は免許不要局について適合表示無線設備のみを使用する条件を置く。一方、第38条の7第1項は登録証明機関が技術基準適合証明後に表示を付さなければならない規定であり、同条第2項は組込み製品取扱業者が同一表示を製品へ付すことができる規定である。`PRV-0006.excerpt`の「設備には表示を付すことができる」は第1項の義務を正確に表していない。
- **影響:** 無線局開設者、登録証明機関、認証取扱業者及び組込み製品取扱業者の責任が混ざり、`REQ-0003`の製品表示確認がどの法的routeから導出されたか曖昧になる。個別証明、工事設計認証及び既認証モジュール採用の違いも判定できない。
- **最小修正:** 第4条第3号を正規位置で原子化し、第38条の7第1項・第2項の主体とmodalityを分ける。量産用の工事設計認証routeを候補にするなら第38条の24～第38条の26も別Provision/Statementとして追加し、選ばないrouteは`on_hold`にする。`PRV-0006`の要約を現行条文へ合わせ、Sourceの版を2026-08-22時点で再確認する。
- **公式一次情報:** [e-Gov 電波法](https://laws.e-gov.go.jp/law/325AC0000000131)

### 5.2 モバイルバッテリー — revise

自動発見候補は、(1) METIのモバイルバッテリー/PSE案内、(2) UNECE UN Manual of Tests and Criteria Revision 8、(3) MLITの2026-04-24航空旅客携行ルール案内であり、製品固有性はある。化学系、体積エネルギー密度、用途除外・組込み状態、輸送mode、適用版・国内取込み、Wh定格、便・運送人が未確定である点もAPPに残している。

しかし3件とも、探索起点をmandatory/prohibition chainの直接根拠へ昇格させており、公式一次情報優先とSource identityのGateを満たさない。

#### Finding MB-C1S-001 — High — DENAN行政案内だけから直接法規義務を生成

- **根拠:** `SRC-0001`はMETIの消費者向け行政案内で`source_type=guideline`である。これだけを参照する`PRV-0001`から、`NRM-0001`は「日本で販売する事業者候補」に技術基準適合とPSE表示を課し、`APP-0001.binding_basis=direct_regulation`、`OBL-0001.obligation_kind=mandatory`としている。現行法では技術基準適合、表示及び表示のない電気用品の販売禁止は別条項で、義務主体も同一ではない。行政案内には400 Wh/L閾値等が示されるが、法令正本の代替にはならない。
- **影響:** 販売者、届出製造・輸入事業者及び表示主体を誤って統合し、適用性が後で確定された際に誤った組織・Evidenceへ投影される。
- **最小修正:** 電気用品安全法第8条、第10条、第27条及び施行令別表第二第12号を法令Source/Provisionとして追加する。METI案内はguidelineのまま分類解釈・探索補助へ分離する。技術基準適合、表示及び販売禁止を主体別のNormative Statementへ分け、体積エネルギー密度、用途除外及び機器組込み状態を人確認事項へ入れる。
- **公式一次情報:** [e-Gov 電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234?occasion_date=20260611)、[e-Gov 電気用品安全法施行令](https://laws.e-gov.go.jp/law/337CO0000000324)、[METI リチウムイオン蓄電池搭載製品案内](https://www.meti.go.jp/product_safety/consumer/lithium_ion_battery.html)

#### Finding MB-C1S-002 — High — UN 38.3 test summaryの義務根拠をManualへ誤帰属

- **根拠:** `SRC-0002`/`PRV-0002`はUN Manual of Tests and Criteria 38.3.5であり、test summaryの記載内容を規定する資料である。モデルはこれだけから「製造者または頒布者候補が試験要約を利用可能にする」というmandatory義務を作った。make availableの規範文はUN Model Regulations Rev.24 2.9.4(g)にあり、製造日条件及び機器・回路基板へ組み込まれたbutton cellの例外もモデルにない。`APP-0002.binding_basis=unknown`とした境界自体は適切だが、Normative StatementのSource chainは成立していない。
- **影響:** Manualの試験・文書内容とModel Regulationsの主体・条件を取り違え、対象電池、主体及び例外を過剰に広げる。国内又は各輸送modeへの取込み確認もできない。
- **最小修正:** UN Model Regulationsの該当版をManualとは別Sourceとして追加し、2.9.4(g)を義務Provision、Manual 38.3.5をtest-summary内容Provisionとして分離する。製造日条件、主体及びbutton cell例外を原子化し、各輸送modeへの法的取込みが確認されるまで`binding_basis=unknown`とAPP `uncertain`を維持する。
- **公式一次情報:** [UNECE UN Manual Rev.8/Amend.1配布ページ](https://unece.org/transport/dangerous-goods/rev8-files)、[UNECE UN Model Regulations Rev.24 Vol. I](https://unece.org/sites/default/files/2025-09/ST_SG_AC10_1_Rev24e_Vol%20I.pdf)

#### Finding MB-C1S-003 — High — 文書提供義務を対象システムのProduct Requirementへ投影

- **根拠:** `OBL-0002.target_kind=documentation`及び`NRM-0002`の主体は製造者又は頒布者候補である。それにもかかわらず`EPR-0003.projection_kind=product_requirement`は、`product_layer=system`の`REQ-0002`へ投影し、対象システムのrequirements配列内で「製造者は試験要約を利用可能にする」と記述している。これは製品特性又は挙動ではなく、組織・documentationへの義務である。
- **影響:** C-EPR-02の非Product投影境界に反し、製造者の文書管理責任をモバイルバッテリー本体のSysML Requirementとして扱う。将来のverification coverageも、製品試験と文書提供processを混同する。
- **最小修正:** test summaryの作成・維持・提供は`projection_targets[]`のdocumentation又はprocess requirementへ投影する。製品に必要な設計特性を別途導出する場合だけ、根拠を明示してproduct requirementを追加する。EvidenceRequirementはdocumentation targetと対象電池型式へ接続する。
- **公式一次情報:** [UNECE UN Model Regulations Rev.24 Vol. I](https://unece.org/sites/default/files/2025-09/ST_SG_AC10_1_Rev24e_Vol%20I.pdf)

#### Finding MB-C1S-004 — High — 航空の行政解説を直接法規として扱い、告示正本がない

- **根拠:** `SRC-0003`はMLIT報道発表で`source_type=guideline`であるが、`APP-0003.binding_basis=direct_regulation`、`NRM-0003`/`OBL-0003`は法的prohibitionとしている。報道発表自身が「航空機による爆発物等の輸送基準等を定める告示」及び運用通達の改正に基づくと説明しているが、その告示正本はモデルSourceにない。
- **影響:** C-SRC-01及びC-APP-02に反し、行政解説の種類から拘束力を推測している。正規条項、対象便、例外及び運送人追加条件へ戻れない。
- **最小修正:** 2026-04-24施行の告示正本と必要な運用通達を別Source/Provisionとして追加し、報道発表はguidelineへ保持する。告示上の対象・例外を確認するまでAPPは`uncertain`のままとする。
- **公式一次情報:** [MLIT 報道発表](https://www.mlit.go.jp/report/press/kouku10_hh_000310.html)、[航空機による爆発物等の輸送基準等を定める告示（2026-04-24）](https://safetyp.cab.mlit.go.jp/wp-content/uploads/2026/04/01-%EF%BC%88%E7%88%86%E7%99%BA%E7%89%A9%E7%AD%89%E5%91%8A%E7%A4%BA%EF%BC%89%E5%91%8A%E7%A4%BA%E6%9C%AC%E6%96%87%EF%BC%88260424%EF%BC%89.pdf)

#### Finding MB-C1S-005 — Medium — 採用した2026航空案内の製品固有ルールを部分抽出

- **根拠:** MLIT報道発表は、2026-04-24からの追加ルールとして、160 Wh以下のモバイルバッテリー2個まで、機内でモバイルバッテリーを充電しないこと、モバイルバッテリーから他機器へ給電しないことを列挙する。モデルは160 Wh超の持込み禁止だけを`NRM-0003`にし、残りをadopted Sourceの除外又は保留理由へ記録していない。
- **影響:** Discovery inventoryが未確認であることは表現できているが、既に採用した一次探索結果から直接見える製品固有候補を落とし、候補集合の再現性を弱める。
- **最小修正:** 3項目を別Normative Statement候補として原子化するか、今回scope外ならRDLの明示的な除外理由と再探索triggerを残す。航空旅客の運用義務をモバイルバッテリー本体要求へ直接変換せず、process/operational projectionとして扱う。
- **公式一次情報:** [MLIT 2026年4月14日報道発表](https://www.mlit.go.jp/report/press/kouku10_hh_000310.html)

### 5.3 懐中電灯 — revise

自動発見候補は、(1) DENANの充電式携帯電灯候補、(2) 消費生活用製品安全法の重大製品事故報告、(3) JISC公式カタログである。法令SourceとMETI行政解釈・事故報告解説を別Sourceにしており、具体的JIS番号・版を確定できないためJISC候補を`on_hold`とした点は適切である。電池方式、充電方式、交流接続、定格、市場及び製造輸入主体が探索限界として残っている。

重大製品事故報告chainは、消費生活用製品安全法第35条と内閣府令第3条を直接根拠とし、METI解説を別Sourceへ分けている。10日報告を製品特性ではなくprocess投影にしており、False conformity claimもない。

#### Finding FL-C1S-001 — High — 充電式携帯電灯Provisionの正規位置が存在しない

- **根拠:** `PRV-0002.locator.canonical`は「別表第二第8号(86)(17)」である。2026-08-22時点の電気用品安全法施行令別表第二では、第8号は電動力応用機械器具で、充電式携帯電灯は**第9号（光源及び光源応用機械器具）第17号**にある。「86」は同Provisionの正規位置ではない。
- **影響:** Provisionが原典の一意な位置へ戻れず、C-SRC-02に不合格となる。誤ったlocatorが09及び17–21へ同期しているため、機械的同期PASSでも原典追跡は成立しない。
- **最小修正:** `PRV-0002`の正規位置を「別表第二第9号(17)」へ修正し、関連する根拠文、09及び17–21を再生成する。旧技術基準解釈の項番を引用する場合は、施行令Provisionとは別Source/Provisionとして版付きで記録する。
- **公式一次情報:** [e-Gov 電気用品安全法施行令](https://laws.e-gov.go.jp/law/337CO0000000324)、[METI 特定電気用品以外の電気用品一覧（品目302）](https://www.meti.go.jp/policy/consumer/seian/denan/non_specified_electrical.html)

## 6. 最終Gate

| 製品 | Discovery | APP/人確認境界 | False claim | Source/Provision意味品質 | 09/17–21同期 | J1 Gate |
|---|---|---|---|---|---|---|
| smart-fan | PASS | PASS | PASS | revise（Medium 1） | PASS | **revise** |
| mobile-battery | 構造PASS・意味revise | PASS | PASS | fail（High 4、Medium 1） | PASS | **revise / fail** |
| flashlight | PASS | PASS | PASS | fail（High 1） | PASS | **revise / fail** |

**Compliance J1総合GateはFAIL。** High findingを閉じ、Source/Provision/Normative Statement/APP/Projectionの再生成後にvalidator、09ハッシュ照合及びexport `--check`を再実行する必要がある。適用性、適合性又は認証状態は、本レビューでも確定していない。
