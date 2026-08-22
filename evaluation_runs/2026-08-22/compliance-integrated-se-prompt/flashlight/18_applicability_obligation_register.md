# Applicability and Obligation Register

## Normative Statement

| ID | Provision | 種別 | 様相 | 主体 | 条件 | 行為／性質 | 対象 | 限界 | 解釈状態 |
|---|---|---|---|---|---|---|---|---|---|
| NRM-JP-DENAN-TECH-01 | PRV-JP-DENAN-08-1 | normative | obligation | 届出事業者 | 届出に係る電気用品を製造または輸入する場合 | 電気用品を技術上の基準に適合させる | 届出に係る電気用品 | — | ai_candidate |
| NRM-JP-DENAN-INSPECT-01 | PRV-JP-DENAN-08-2<br>PRV-JP-DENAN-REG-11-3 | normative | obligation | 届出事業者 | 対象電気用品を製造または輸入する場合 | 自主検査を行い、検査記録を作成して保存する | 対象電気用品の検査記録 | 検査の日から3年間（電気用品安全法施行規則第11条第3項） | ai_candidate |
| NRM-JP-CSPSA-REPORT-01 | PRV-JP-CSPSA-35-1<br>PRV-JP-CSPSA-ORDER-03-1 | normative | obligation | 消費生活用製品の製造または輸入事業者 | 自ら製造または輸入した消費生活用製品について重大製品事故が発生したことを知った場合 | 消費者庁へ報告する | 重大製品事故情報 | 知った日から10日以内（重大事故報告等に関する内閣府令第3条第1項） | ai_candidate |

## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）

| ID | Normative Statement | コンテキスト | 判断候補 | 拘束根拠 | 理由 | 人確認状態 | 確認者 | 確認日時 | 再評価トリガー |
|---|---|---|---|---|---|---|---|---|---|
| APP-FL-DENAN-01 | NRM-JP-DENAN-TECH-01<br>NRM-JP-DENAN-INSPECT-01 | {'jurisdiction': '日本', 'market': '日本の一般消費者市場（仮定）', 'product_classification': '携帯照明。リチウムイオン蓄電池または充電器の対象区分は未決定', 'intended_use': '成人が一時的に周囲を照らす', 'configuration_ref': 'CFG-FL-01', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | METIは一定条件のリチウムイオン蓄電池を対象品目としているが、電池化学系、体積エネルギー密度、内蔵方式、充電器同梱、事業者役割が未決定である。 | pending | — | — | 電池化学系または体積エネルギー密度を決定した場合<br>内蔵、交換式、同梱充電器または販売単位を決定した場合<br>製造者または輸入者の役割を決定した場合<br>電気用品安全法、施行令、技術基準または公式対象解釈が改正された場合 |
| APP-FL-CSPSA-01 | NRM-JP-CSPSA-REPORT-01 | {'jurisdiction': '日本', 'market': '日本の一般消費者市場（仮定）', 'product_classification': '一般消費者向け携帯照明（仮定）', 'intended_use': '成人が一時的に周囲を照らす', 'configuration_ref': 'CFG-FL-01', 'lifecycle_stage': 'operation'} | uncertain | direct_regulation | 一般消費者向け製品という仮定では候補になるが、法上の消費生活用製品該当性、除外、製造輸入主体が未確認である。 | pending | — | — | 市場、用途または製品分類を変更した場合<br>製造者または輸入者の役割を決定した場合<br>重大製品事故の定義、報告期限または対象除外が改正された場合 |

## Obligation

| ID | 種別 | 義務主体候補 | 対象 | 条件 | 必要結果 | 状態 |
|---|---|---|---|---|---|---|
| OBL-FL-DENAN-01 | mandatory | 届出事業者候補 | CFG-FL-01に含まれ、DENAN対象と人が決定した電気用品 | APP-FL-DENAN-01を人がapplicableまたはpartially_applicableと決定した場合 | 対象電気用品が特定された技術基準に適合する | candidate |
| OBL-FL-DENAN-02 | mandatory | 届出事業者候補 | 対象電気用品の自主検査プロセスおよび検査記録 | APP-FL-DENAN-01を人がapplicableまたはpartially_applicableと決定した場合 | 必要な自主検査を実施し、検査記録を作成して要求期間保存する | candidate |
| OBL-FL-CSPSA-01 | mandatory | 日本の製造または輸入事業者候補 | 重大製品事故の識別および報告プロセス | APP-FL-CSPSA-01を人がapplicableまたはpartially_applicableと決定し、重大製品事故を知った場合 | 所定の期限内に消費者庁へ報告する | candidate |

## 人の確認バックログ

- APP-FL-DENAN-01: METIは一定条件のリチウムイオン蓄電池を対象品目としているが、電池化学系、体積エネルギー密度、内蔵方式、充電器同梱、事業者役割が未決定である。
- APP-FL-CSPSA-01: 一般消費者向け製品という仮定では候補になるが、法上の消費生活用製品該当性、除外、製造輸入主体が未確認である。
