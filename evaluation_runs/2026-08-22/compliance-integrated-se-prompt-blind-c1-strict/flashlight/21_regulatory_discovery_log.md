# Regulatory Discovery Log

## 対象構成と市場

| ID | 市場 | 構成 |
|---|---|---|
| RDL-0001 | 日本国内の一般家庭向け市場候補 | CFG-0001 |
| RDL-0002 | 日本国内の一般家庭向け市場候補 | CFG-0001 |
| RDL-0003 | 日本国内の一般家庭向け市場候補 | CFG-0001 |

## 探索した公式台帳・探索queryと実行時点

| ID | 公式探索先 | Query | Query記録状態 | 実行時点 |
|---|---|---|---|---|
| RDL-0001 | https://laws.e-gov.go.jp/law/336AC0000000234<br>https://laws.e-gov.go.jp/law/337CO0000000324/<br>https://www.meti.go.jp/policy/consumer/seian/denan/subject01.html<br>https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/hani/haninokaishaku_150122.pdf | site:meti.go.jp/policy/consumer/seian/denan 懐中電灯 電気用品安全法 対象<br>site:laws.e-gov.go.jp 電気用品安全法施行令 携帯用電灯 懐中電灯<br>site:meti.go.jp/policy/consumer/seian/denan リチウムイオン蓄電池 対象 内蔵 機器<br>site:meti.go.jp/policy/consumer/seian/denan 特定電気用品以外 直流電源装置 リチウムイオン蓄電池<br>site:meti.go.jp/policy/consumer/seian/denan "充電式携帯電灯"<br>site:laws.e-gov.go.jp/law/337CO0000000324 "充電式携帯電灯"<br>site:meti.go.jp/policy/consumer/seian/denan/non_specified_electrical.html "充電式携帯電灯" | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0002 | https://laws.e-gov.go.jp/law/348AC0000000031<br>https://laws.e-gov.go.jp/law/421M60000002047/<br>https://www.meti.go.jp/product_safety/producer/guideline/index.html | site:laws.e-gov.go.jp 消費生活用製品安全法 第35条 重大製品事故 10日<br>site:meti.go.jp/product_safety 重大製品事故 報告義務 10日 製造 輸入<br>site:meti.go.jp/policy/consumer/seian/shouan 重大製品事故 報告 法第35条<br>site:laws.e-gov.go.jp 消費生活用製品安全法施行規則 重大製品事故 報告 10日 | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0003 | https://www.jisc.go.jp/app/jis/general/GnrJISSearch.html | site:jisc.go.jp 懐中電灯 JIS 規格 | complete | 2026-08-22T00:00:00+09:00 |

## 採用・除外・保留候補Sourceと理由

| ID | 候補Source | 扱い | 理由 |
|---|---|---|---|
| RDL-0001 | SRC-0001<br>SRC-0002<br>SRC-0003 | adopted_candidate | 法第8条と施行令別表第二の充電式携帯電灯を候補チェーンに採用した。経済産業省の範囲解釈は行政解説として分離した。充電方式未確定のため適用判定は保留する。 |
| RDL-0002 | SRC-0004<br>SRC-0005<br>SRC-0006 | adopted_candidate | 消費生活用製品安全法第35条と内閣府令第3条を規範チェーンに採用した。経済産業省の事故報告ページは行政解説として別Sourceに保持した。市場及び事業者未確定のため適用判定は保留する。 |
| RDL-0003 | SRC-0007 | on_hold | JISC公式カタログは確認したが、製品構成、電池方式及び試験目的が未確定で、採用すべき規格番号と版を一次情報から確定できないため保留する。 |

## 網羅性の限界・人によるinventory確認

| ID | Query記録状態 | inventory確認 |
|---|---|---|
| RDL-0001 | complete | pending |
| RDL-0002 | complete | pending |
| RDL-0003 | complete | pending |

> Queryまたは除外候補が未記録、あるいは人のinventory確認がpendingの場合、探索の網羅性を主張できません。
