# Regulatory Discovery Log

## 対象構成と市場

| ID | 市場 | 構成 |
|---|---|---|
| RDL-0001 | 日本の一般消費者市場（探索仮定） | CFG-0001 |
| RDL-0002 | 日本の一般消費者市場（探索仮定） | CFG-0001 |
| RDL-0003 | 日本の一般消費者市場（探索仮定） | CFG-0001 |
| RDL-0004 | 日本の一般消費者市場（探索仮定） | CFG-0001 |
| RDL-0005 | 日本の一般消費者市場（探索仮定） | CFG-0001 |

## 探索した公式台帳・探索queryと実行時点

| ID | 公式探索先 | Query | Query記録状態 | 実行時点 |
|---|---|---|---|---|
| RDL-0001 | METI 電気用品安全法対象非対象解釈例一覧<br>METI DENAN手続案内 | site:meti.go.jp 電気用品安全法 懐中電灯 充電式 LED 電池 対象 非対象<br>site:meti.go.jp 電気用品安全法 リチウムイオン蓄電池 400Wh/L 対象 公式<br>site:meti.go.jp/policy/consumer/seian/denan 直流電源装置 ACアダプター 対象 電気用品安全法 公式 | complete | 2026-08-22T15:30:00+09:00 |
| RDL-0002 | 消費者庁 重大製品事故情報報告・公表制度 | site:caa.go.jp 消費生活用製品安全法 重大製品事故 10日 製造 輸入 公式 | complete | 2026-08-22T15:32:00+09:00 |
| RDL-0003 | 消費者庁 家庭用品品質表示法対象範囲・施行令 | site:caa.go.jp 懐中電灯 家庭用品品質表示法 対象 電気機械器具 | complete | 2026-08-22T15:34:00+09:00 |
| RDL-0004 | IEC Webstore | site:iec.ch portable handlamps IEC 60598-2-8 official<br>site:jisc.go.jp 懐中電灯 JIS 規格 照明器具 | complete | 2026-08-22T15:36:00+09:00 |
| RDL-0005 | ICAO Dangerous Goods Technical Instructions<br>国土交通省航空危険物情報 | site:mlit.go.jp リチウム電池 航空輸送 携帯 電子機器 公式<br>site:icao.int lithium batteries transport technical instructions official passenger baggage | complete | 2026-08-22T15:38:00+09:00 |

## 採用・除外・保留候補Sourceと理由

| ID | 候補Source | 扱い | 理由 |
|---|---|---|---|
| RDL-0001 | SRC-DENAN | adopted_candidate | 電池・充電構成により対象となる可能性があるため候補採用。適用性はuncertain。 |
| RDL-0002 | SRC-CSPSA | adopted_candidate | 一般消費者製品候補の流通後義務として採用。製品該当性と義務主体はuncertain。 |
| RDL-0003 | SRC-HQL | on_hold | 指定品目制度は確認したが、懐中電灯の個別該当性を一次情報から確定できない。 |
| RDL-0004 | SRC-IEC60598 | on_hold | ハンドランプ規格候補だが、製品分類、国内採用根拠、本文および最新版を人が確認していない。 |
| RDL-0005 | SRC-ICAO9284 | on_hold | 航空輸送とリチウム電池構成が未決定で、版・具体要件を確認していない。 |

## 網羅性の限界・人によるinventory確認

| ID | Query記録状態 | inventory確認 |
|---|---|---|
| RDL-0001 | complete | pending |
| RDL-0002 | complete | pending |
| RDL-0003 | complete | pending |
| RDL-0004 | complete | pending |
| RDL-0005 | complete | pending |

> Queryまたは除外候補が未記録、あるいは人のinventory確認がpendingの場合、探索の網羅性を主張できません。
