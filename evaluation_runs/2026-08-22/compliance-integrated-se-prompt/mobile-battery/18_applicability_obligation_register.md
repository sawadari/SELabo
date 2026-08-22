# Applicability and Obligation Register

## Normative Statement

| ID | Provision | 種別 | 様相 | 主体 | 条件 | 行為／性質 | 対象 | 限界 | 解釈状態 |
|---|---|---|---|---|---|---|---|---|---|
| NRM-MB-001 | PRV-MB-001 | definition | definition | — | 日本の電安法上の対象性を検討する場合 | 単電池1個当たりの体積エネルギー密度と用途除外を用いてリチウムイオン蓄電池の対象範囲を判断する | 対象製品の電池構成 | 400 Wh/L以上という対象条件および公式ページ記載の用途除外 | ai_candidate |
| NRM-MB-002 | PRV-MB-002 | normative | obligation | 届出事業者 | 届出に係る型式の電気用品を製造または輸入する場合 | 当該電気用品を適用される技術上の基準に適合させる | 届出に係る型式の電気用品 | — | ai_candidate |
| NRM-MB-003 | PRV-MB-003 | normative | obligation | 届出事業者 | 対象電気用品を製造または輸入する場合 | 所定の検査を実施して検査記録を作成し保存する | 製造または輸入に係る電気用品 | — | ai_candidate |
| NRM-MB-004 | PRV-MB-004 | normative | prohibition | 販売事業者または届出事業者 | 電安法対象製品を日本で販売または販売目的で陳列する場合 | 所定の義務履行前の無表示製品を販売または陳列しない | 電安法対象製品 | — | ai_candidate |
| NRM-MB-005 | PRV-MB-005 | normative | prohibition | 航空旅客 | 日本の航空機内へモバイルバッテリーを持ち込む場合 | 2個を超えるモバイルバッテリーまたは160Whを超えるモバイルバッテリーを持ち込まない | 旅客が携行するモバイルバッテリー | 2個まで、各160Wh以下 | ai_candidate |
| NRM-MB-006 | PRV-MB-006 | normative | prohibition | 航空旅客 | 航空機内にいる間 | 機内電源からモバイルバッテリーを充電しない | モバイルバッテリー | — | ai_candidate |
| NRM-MB-007 | PRV-MB-007 | normative | recommendation | 航空旅客 | 航空機内にいる間 | モバイルバッテリーから他の電子機器へ給電しないよう求める | 携帯するモバイルバッテリー | — | ai_candidate |
| NRM-MB-008 | PRV-MB-008<br>PRV-MB-009 | normative | obligation | セルまたは電池の製造者および後続流通業者候補 | 2003年6月30日後に製造され、UN 38.3の輸送要件が対象セルまたは電池型式に適用される場合 | 対象電池型式の試験要約を利用可能にする | リチウム電池試験要約 | 2003年6月30日後に製造されたセルまたは電池 | ai_candidate |

## Applicability Assessment（適用性評価コンテキスト・判断候補・拘束根拠・再評価トリガー）

| ID | Normative Statement | コンテキスト | 判断候補 | 拘束根拠 | 理由 | 人確認状態 | 確認者 | 確認日時 | 再評価トリガー |
|---|---|---|---|---|---|---|---|---|---|
| APP-MB-001 | NRM-MB-001<br>NRM-MB-002<br>NRM-MB-003<br>NRM-MB-004 | {'jurisdiction': '日本', 'market': '日本国内一般消費者向け販売候補', 'product_classification': 'リチウムイオン蓄電池を内蔵する携帯用充電器候補', 'intended_use': '携帯機器への給電', 'configuration_ref': 'CFG-MB-CANDIDATE', 'lifecycle_stage': 'concept/development/production'} | uncertain | direct_regulation | METI公式情報はモバイルバッテリーとリチウムイオン蓄電池を電安法対象候補として示すが、単電池の体積エネルギー密度、用途除外、事業者役割および販売経路が未確認 | pending | — | — | セルまたは電池パック仕様を決定した場合<br>体積エネルギー密度を確認した場合<br>用途分類または事業者役割を決定した場合<br>販売時点で有効な法令・技術基準を変更した場合 |
| APP-MB-002 | NRM-MB-005<br>NRM-MB-006 | {'jurisdiction': '日本', 'market': '日本発着便の旅客利用候補', 'product_classification': 'モバイルバッテリー候補', 'intended_use': '航空旅客手荷物として携行する可能性', 'configuration_ref': 'CFG-MB-CANDIDATE', 'lifecycle_stage': 'utilization'} | uncertain | direct_regulation | 国土交通省は2026-04-24適用ルールを公表しているが、航空旅客利用が製品の意図する使用に含まれるか、定格Whおよび航空会社追加条件が未確認 | pending | — | — | 定格Whまたは航空旅客利用方針を決定した場合<br>航空法令、告示または航空会社条件を変更した場合<br>利用法域または運送事業者を変更した場合 |
| APP-MB-003 | NRM-MB-008 | {'jurisdiction': 'international/unknown', 'market': '日本向け製品の物流候補', 'product_classification': 'リチウムイオン電池を内蔵する製品候補', 'intended_use': '製造・輸入・流通時の輸送', 'configuration_ref': 'CFG-MB-CANDIDATE', 'lifecycle_stage': 'production'} | uncertain | unknown | UNECE公式版は確認したが、採用すべき版、輸送モード、セル・電池型式、法域ごとの取込みおよび供給者責任が未確認 | pending | — | — | 輸送モード、法域または運送事業者を決定した場合<br>セル・電池・製品構成を変更した場合<br>UN Manualの採用版を変更した場合 |
| APP-MB-004 | NRM-MB-007 | {'jurisdiction': '日本', 'market': '日本発着便の旅客利用候補', 'product_classification': 'モバイルバッテリー候補', 'intended_use': '航空旅客手荷物として携行する可能性', 'configuration_ref': 'CFG-MB-CANDIDATE', 'lifecycle_stage': 'utilization'} | uncertain | unknown | 国土交通省は他機器への給電を避けるよう要請しているが、公式資料は法律に基づく禁止事項ではないと明記する。組織の採用方針と対象便は未確認。 | pending | — | — | 航空旅客利用方針を決定した場合<br>国土交通省の安全要請または航空会社条件を変更した場合<br>利用法域または運送事業者を変更した場合 |

## Obligation

| ID | 種別 | 義務主体候補 | 対象 | 条件 | 必要結果 | 状態 |
|---|---|---|---|---|---|---|
| OBL-MB-001 | mandatory | 届出事業者候補 | CFG-MB-CANDIDATE | 対象製品が電安法対象であり、届出事業者が製造または輸入する場合 | 販売時点に適用される技術上の基準へ適合する | candidate |
| OBL-MB-002 | mandatory | 届出事業者候補 | 製造または輸入に係る対象製品 | 対象製品が電安法対象であり、届出事業者が製造または輸入する場合 | 所定の検査を実施して検査記録を保存する | candidate |
| OBL-MB-003 | prohibition | 届出事業者または販売事業者候補 | 日本で販売する対象製品 | 対象製品が電安法対象で日本で販売または陳列される場合 | 所定義務を履行して表示条件を満たすまで販売または陳列しない | candidate |
| OBL-MB-004 | prohibition | 航空旅客 | 旅客が携行するモバイルバッテリー | 日本の航空機内へ持ち込む場合 | 持込み個数を2個まで、各定格を160Wh以下とする | candidate |
| OBL-MB-005 | prohibition | 航空旅客 | 機内へ持ち込むモバイルバッテリー | 航空機内にいる間 | モバイルバッテリーへ充電しない | candidate |
| OBL-MB-006 | recommendation | 航空旅客 | 機内へ持ち込むモバイルバッテリー | 航空機内にいる間 | 安全上、モバイルバッテリーから他の電子機器へ給電しない運用を推奨する | candidate |
| OBL-MB-007 | mandatory | 製造者・流通関係者候補 | 輸送するセルまたは電池型式 | 選定した輸送制度がUN 38.3を取り込み、対象セルまたは電池が2003年6月30日後に製造され、組込みボタン電池の例外に該当せず、対象型式に適用される場合 | 製造時点と組込みボタン電池例外の該当性を確認し、適用される対象型式に対応する試験要約を利用可能にする | candidate |

## 人の確認バックログ

- APP-MB-001: METI公式情報はモバイルバッテリーとリチウムイオン蓄電池を電安法対象候補として示すが、単電池の体積エネルギー密度、用途除外、事業者役割および販売経路が未確認
- APP-MB-002: 国土交通省は2026-04-24適用ルールを公表しているが、航空旅客利用が製品の意図する使用に含まれるか、定格Whおよび航空会社追加条件が未確認
- APP-MB-003: UNECE公式版は確認したが、採用すべき版、輸送モード、セル・電池型式、法域ごとの取込みおよび供給者責任が未確認
- APP-MB-004: 国土交通省は他機器への給電を避けるよう要請しているが、公式資料は法律に基づく禁止事項ではないと明記する。組織の採用方針と対象便は未確認。
