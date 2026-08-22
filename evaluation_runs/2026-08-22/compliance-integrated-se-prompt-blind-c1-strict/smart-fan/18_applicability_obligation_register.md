# Applicability and Obligation Register

## Normative Statement

| ID | Provision | 種別 | 様相 | 主体 | 条件 | 行為／性質 | 対象 | 限界 | 解釈状態 |
|---|---|---|---|---|---|---|---|---|---|
| NRM-0001 | PRV-0001<br>PRV-0002<br>PRV-0003 | normative | obligation | 届出事業者 | 対象製品が電気用品安全法施行令別表第二の扇風機又はサーキュレーターに該当する場合 | 届出に係る電気用品を技術上の基準に適合させる | 家庭用スマート扇風機候補 | 定格消費電力300 W以下という分類閾値を含む | ai_candidate |
| NRM-0002 | PRV-0004 | normative | obligation | 製造又は輸入を行う届出事業者 | 対象製品が産業用を除く省令第20条の扇風機に該当する場合 | 製造年、設計上の標準使用期間及び期間超過時の経年劣化事故のおそれに関する注意を表示する | 家庭用スマート扇風機候補 | — | ai_candidate |
| NRM-0003 | PRV-0005<br>PRV-0006 | normative | obligation | 無線局を開設する者 | 日本国内で免許を要しないWi-Fi無線局を開設する場合 | 免許不要条件に対応する表示が付された対象無線設備を使用する | Wi-Fi無線設備候補 | — | ai_candidate |

## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）

| ID | Normative Statement | コンテキスト | 判断候補 | 拘束根拠 | 理由 | 人確認状態 | 確認者 | 確認日時 | 再評価トリガー |
|---|---|---|---|---|---|---|---|---|---|
| APP-0001 | NRM-0001 | {'jurisdiction': '日本', 'market': '日本国内の一般家庭向け市場', 'product_classification': '家庭用扇風機候補', 'intended_use': '寝室又は居室での家庭用送風', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | 電源方式及び定格消費電力が未確定であり、別表第二への分類を確定できない。 | pending | — | — | 電源方式又は定格消費電力を決定した場合<br>販売及び製造輸入主体を決定した場合<br>適用する技術基準体系を選定した場合 |
| APP-0002 | NRM-0002 | {'jurisdiction': '日本', 'market': '日本国内の一般家庭向け市場', 'product_classification': '家庭用扇風機候補', 'intended_use': '寝室又は居室での家庭用送風', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'production'} | uncertain | direct_regulation | 入力は一般家庭用途を示すが、法令上の扇風機分類と製造又は輸入構成が未確定である。 | pending | — | — | 製品分類又は用途区分を確定した場合<br>設計上の標準使用期間を決定した場合<br>表示版下を作成した場合 |
| APP-0003 | NRM-0003 | {'jurisdiction': '日本', 'market': '日本国内の一般家庭向け市場', 'product_classification': 'Wi-Fi無線設備搭載候補', 'intended_use': '寝室又は居室での家庭用送風', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | Wi-Fi搭載自体、周波数、空中線電力、無線モジュール及び表示方法が未決定である。 | pending | — | — | Wi-Fi搭載有無を決定した場合<br>無線モジュール又はアンテナを選定した場合<br>無線仕様又はファームウェアを変更した場合 |

## Obligation

| ID | 種別 | 義務主体候補 | 対象 | 条件 | 必要結果 | 状態 |
|---|---|---|---|---|---|---|
| OBL-0001 | mandatory | 届出事業者候補 | 家庭用スマート扇風機候補 | 施行令別表第二の対象電気用品に該当する場合 | 人が選定した技術基準体系の適用項目へ適合する | candidate |
| OBL-0002 | mandatory | 製造又は輸入を行う届出事業者候補 | 家庭用スマート扇風機候補 | 産業用を除く省令第20条の扇風機に該当する場合 | 本体に製造年、設計上の標準使用期間及び経年劣化事故のおそれに関する注意が表示される | candidate |
| OBL-0003 | mandatory | 無線局を開設する者候補 | Wi-Fi無線設備候補 | 日本国内で免許を要しないWi-Fi無線局を開設する構成の場合 | 免許不要条件に対応する表示が付された対象無線設備が使用される | candidate |

## 人の確認バックログ

- APP-0001: 電源方式及び定格消費電力が未確定であり、別表第二への分類を確定できない。
- APP-0002: 入力は一般家庭用途を示すが、法令上の扇風機分類と製造又は輸入構成が未確定である。
- APP-0003: Wi-Fi搭載自体、周波数、空中線電力、無線モジュール及び表示方法が未決定である。
