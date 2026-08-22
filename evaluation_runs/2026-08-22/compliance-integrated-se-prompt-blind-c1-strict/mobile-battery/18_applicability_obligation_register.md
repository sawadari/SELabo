# Applicability and Obligation Register

## Normative Statement

| ID | Provision | 種別 | 様相 | 主体 | 条件 | 行為／性質 | 対象 | 限界 | 解釈状態 |
|---|---|---|---|---|---|---|---|---|---|
| NRM-0001 | PRV-0001 | normative | obligation | 日本で販売する事業者候補 | 対象製品が電気用品安全法上のリチウムイオン蓄電池に該当する場合 | 技術基準適合およびPSE表示を行う | 対象製品 | — | ai_candidate |
| NRM-0002 | PRV-0002 | normative | obligation | 製造者または頒布者候補 | リチウム電池を輸送に供する場合 | 38.3に基づく試験要約を利用可能にする | 対象セルまたは電池型式 | — | ai_candidate |
| NRM-0003 | PRV-0003 | normative | prohibition | 航空旅客候補 | 日本の対象便へモバイルバッテリーを持ち込む場合 | 160Whを超えるモバイルバッテリーを持ち込まない | モバイルバッテリー | 160Wh以下 | ai_candidate |

## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）

| ID | Normative Statement | コンテキスト | 判断候補 | 拘束根拠 | 理由 | 人確認状態 | 確認者 | 確認日時 | 再評価トリガー |
|---|---|---|---|---|---|---|---|---|---|
| APP-0001 | NRM-0001 | {'jurisdiction': 'JP', 'market': '日本市場', 'product_classification': 'モバイルバッテリー候補', 'intended_use': '携帯機器への給電', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'development'} | uncertain | direct_regulation | 電池化学系、体積エネルギー密度、除外用途および販売主体が未確定 | pending | — | — | 電池仕様または販売主体を確定した場合<br>法令または解釈を改正した場合 |
| APP-0002 | NRM-0002 | {'jurisdiction': 'UN-TRANSPORT', 'market': '国際輸送', 'product_classification': 'リチウムイオン蓄電池候補', 'intended_use': '製品輸送', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'development'} | uncertain | unknown | 電池型式、輸送モード、適用版および国内規則への取込みが未確定 | pending | — | — | 電池型式または輸送モードを確定した場合<br>UN文書適用版を確定した場合 |
| APP-0003 | NRM-0003 | {'jurisdiction': 'JP', 'market': '日本の航空旅客輸送', 'product_classification': 'モバイルバッテリー候補', 'intended_use': '旅客による機内持込み', 'configuration_ref': 'CFG-0001', 'lifecycle_stage': 'utilization'} | uncertain | direct_regulation | Wh定格、便、運送人および実際の旅客携行条件が未確定 | pending | — | — | Wh定格または対象便を確定した場合<br>国土交通省または航空会社の規則を改正した場合 |

## Obligation

| ID | 種別 | 義務主体候補 | 対象 | 条件 | 必要結果 | 状態 |
|---|---|---|---|---|---|---|
| OBL-0001 | mandatory | 日本で販売する事業者候補 | CFG-0001 | 法令上の対象に該当する場合 | 技術基準適合および必要表示が確認できる | candidate |
| OBL-0002 | mandatory | 製造者または頒布者候補 | CFG-0001に使用する電池型式 | 輸送規則上の対象に該当する場合 | 適用版に基づく試験要約が利用可能である | candidate |
| OBL-0003 | prohibition | 航空旅客候補 | CFG-0001 | 日本の対象便へ持ち込む場合 | 160Whを超えるモバイルバッテリーを持ち込まない | candidate |

## 人の確認バックログ

- APP-0001: 電池化学系、体積エネルギー密度、除外用途および販売主体が未確定
- APP-0002: 電池型式、輸送モード、適用版および国内規則への取込みが未確定
- APP-0003: Wh定格、便、運送人および実際の旅客携行条件が未確定
