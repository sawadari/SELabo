# Applicability and Obligation Register

## Normative Statement

| ID | Provision | 種別 | 様相 | 主体 | 条件 | 行為／性質 | 対象 | 限界 | 解釈状態 |
|---|---|---|---|---|---|---|---|---|---|
| NRM-SF-PSE | PRV-SF-PSE-8-1 | normative | obligation | 届出事業者 | 届出に係る型式の電気用品を製造または輸入する場合 | 技術基準に適合させる | 届出に係る電気用品 | — | ai_candidate |
| NRM-SF-INSPECTION | PRV-SF-PSE-8-2 | normative | obligation | 届出事業者 | 第8条第1項の対象電気用品を製造または輸入する場合 | 検査を行い、検査記録を作成して保存する | 製造または輸入に係る電気用品 | — | ai_candidate |
| NRM-SF-STABILITY | PRV-SF-STABILITY | normative | obligation | 技術基準省令解釈を採用する届出事業者候補 | 対象製品が当該扇風機に該当する場合 | 通常使用状態で所定傾斜を与えても容易に転倒しない構造とする | 扇風機候補構成 | 任意方向10° | ai_candidate |
| NRM-SF-AGING | PRV-SF-AGING | normative | obligation | 技術基準省令解釈を採用する届出事業者候補 | 対象製品が表示対象の扇風機に該当する場合 | 経年劣化に係る注意喚起事項を本体へ表示する | 扇風機候補構成 | — | ai_candidate |
| NRM-SF-RADIO | PRV-SF-RADIO-4 | normative | obligation | 無線局を開設する者 | 法定の免許不要条件に該当しない無線局を開設する場合 | 総務大臣の免許を受ける | 無線局 | — | ai_candidate |

## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）

| ID | Normative Statement | コンテキスト | 判断候補 | 拘束根拠 | 理由 | 人確認状態 | 確認者 | 確認日時 | 再評価トリガー |
|---|---|---|---|---|---|---|---|---|---|
| APP-SF-PSE | NRM-SF-PSE | {'jurisdiction': '日本（暫定仮定）', 'market': '日本国内販売候補', 'product_classification': '扇風機候補（給電方式および定格未確認）', 'intended_use': '一般家庭の屋内送風', 'configuration_ref': 'CFG-SF-CONCEPT', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | 公式一覧は定格消費電力300W以下の扇風機を候補に含むが、給電方式、定格、事業者区分を確認できない | pending | — | — | 市場、給電方式、定格または事業者区分を決定したとき<br>法令版を変更したとき |
| APP-SF-INSPECTION | NRM-SF-INSPECTION | {'jurisdiction': '日本（暫定仮定）', 'market': '日本国内販売候補', 'product_classification': '扇風機候補（給電方式および定格未確認）', 'intended_use': '一般家庭の屋内送風', 'configuration_ref': 'CFG-SF-CONCEPT', 'lifecycle_stage': 'production'} | uncertain | direct_regulation | 第8条第1項の対象性と製造輸入主体が未確認であり、第2項義務の対象性も確定できない | pending | — | — | 対象電気用品分類または事業者区分を決定したとき<br>法令版を変更したとき |
| APP-SF-STABILITY | NRM-SF-STABILITY | {'jurisdiction': '日本（暫定仮定）', 'market': '日本国内販売候補', 'product_classification': '扇風機候補（給電方式、定格、高さ調節機能未確認）', 'intended_use': '一般家庭の屋内送風', 'configuration_ref': 'CFG-SF-CONCEPT', 'lifecycle_stage': 'development'} | uncertain | acceptable_means_of_compliance | 扇風機分類と別表第八を適合経路として採用するかを確認していない | pending | — | — | 製品分類、定格、高さ調節機能または適合経路を決定したとき<br>解釈版を変更したとき |
| APP-SF-AGING | NRM-SF-AGING | {'jurisdiction': '日本（暫定仮定）', 'market': '日本国内販売候補', 'product_classification': '扇風機候補（用途および除外条件未確認）', 'intended_use': '一般家庭の屋内送風', 'configuration_ref': 'CFG-SF-CONCEPT', 'lifecycle_stage': 'development'} | uncertain | acceptable_means_of_compliance | 扇風機候補だが、表示対象範囲、除外条件、採用する適合経路を人が確認していない | pending | — | — | 製品分類、用途または表示経路を決定したとき<br>解釈版を変更したとき |
| APP-SF-RADIO | NRM-SF-RADIO | {'jurisdiction': '日本（暫定仮定）', 'market': '日本国内販売候補', 'product_classification': '無線設備組込み製品候補（無線仕様未確認）', 'intended_use': '家庭内の通信操作候補', 'configuration_ref': 'CFG-SF-CONCEPT', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | 無線方式、周波数、出力、モジュール、適合表示および免許不要条件が未確認で、Sourceの現行Revision IDも未確認 | pending | — | — | 無線方式、周波数、出力またはモジュールを決定したとき<br>電波法現行版を確認したとき |

## Obligation

| ID | 種別 | 義務主体候補 | 対象 | 条件 | 必要結果 | 状態 |
|---|---|---|---|---|---|---|
| OBL-SF-PSE | mandatory | 届出事業者候補 | CFG-SF-CONCEPT | 対象構成が届出に係る電気用品である場合 | 採用した技術基準への適合を確認する | candidate |
| OBL-SF-INSPECTION | mandatory | 届出事業者候補 | CFG-SF-CONCEPT | 対象構成が第8条第2項の対象である場合 | 検査を実施し、検査記録を作成して保存する | candidate |
| OBL-SF-STABILITY | mandatory | 届出事業者候補 | CFG-SF-CONCEPT | 当該扇風機分類で別表第八を採用する場合 | 通常使用状態の所定傾斜で転倒しない | candidate |
| OBL-SF-AGING | mandatory | 届出事業者候補 | CFG-SF-CONCEPT | 表示対象の扇風機で別表第八を採用する場合 | 必要な注意喚起事項を本体へ表示する | candidate |
| OBL-SF-RADIO | mandatory | 無線機能の設計および市場投入責任者候補 | CFG-SF-CONCEPTの無線通信部候補 | 日本市場候補で無線機能を使用可能にする場合 | 免許要否、適合経路および表示情報を確認する | candidate |

## 人の確認バックログ

- APP-SF-PSE: 公式一覧は定格消費電力300W以下の扇風機を候補に含むが、給電方式、定格、事業者区分を確認できない
- APP-SF-INSPECTION: 第8条第1項の対象性と製造輸入主体が未確認であり、第2項義務の対象性も確定できない
- APP-SF-STABILITY: 扇風機分類と別表第八を適合経路として採用するかを確認していない
- APP-SF-AGING: 扇風機候補だが、表示対象範囲、除外条件、採用する適合経路を人が確認していない
- APP-SF-RADIO: 無線方式、周波数、出力、モジュール、適合表示および免許不要条件が未確認で、Sourceの現行Revision IDも未確認
