# Regulatory Discovery Log

## 対象構成と市場

| ID | 市場 | 構成 |
|---|---|---|
| RDL-0001 | 日本国内の一般家庭向け市場 | CFG-0001 |
| RDL-0002 | 日本国内の一般家庭向け市場 | CFG-0001 |
| RDL-0003 | 日本国内の一般家庭向け市場 | CFG-0001 |
| RDL-0004 | 日本国内の一般家庭向け市場 | CFG-0001 |

## 探索した公式台帳・探索queryと実行時点

| ID | 公式探索先 | Query | Query記録状態 | 実行時点 |
|---|---|---|---|---|
| RDL-0001 | https://laws.e-gov.go.jp/law/336AC0000000234<br>https://laws.e-gov.go.jp/law/337CO0000000324/<br>https://www.meti.go.jp/policy/consumer/seian/denan/non_specified_electrical.html<br>https://www.meti.go.jp/policy/consumer/seian/denan/procedure_04.html | site:elaws.e-gov.go.jp 電気用品安全法施行令 別表第二 扇風機<br>site:laws.e-gov.go.jp 電気用品安全法 第8条 第10条 表示 販売 扇風機<br>site:laws.e-gov.go.jp 電気用品安全法施行令 別表第二 扇風機 300W<br>site:meti.go.jp/policy/consumer/seian/denan 電気用品安全法 届出事業者 義務 技術基準 適合検査 表示 | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0002 | https://laws.e-gov.go.jp/law/425M60000400034<br>https://www.meti.go.jp/policy/consumer/seian/denan/choki/choki02.pdf<br>https://www.meti.go.jp/product_safety/producer/shouan/07_tyouki.html | site:meti.go.jp 扇風機 電気用品安全法 長期使用製品安全表示制度<br>site:laws.e-gov.go.jp 電気用品の技術上の基準を定める省令 第20条 扇風機 | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0003 | https://laws.e-gov.go.jp/document?lawid=325AC0000000131_20240401_504AC0100000052<br>https://api-catalog.e-gov.go.jp/info/ja/apicatalog/view/47 | site:tele.soumu.go.jp Wi-Fi 技術基準適合証明 電波法 無線設備<br>site:soumu.go.jp Wi-Fi 技適 電波法 2.4GHz 無線LAN<br>site:tele.soumu.go.jp/j/sys/equ/tech/ 技術基準適合証明 無線LAN<br>site:soumu.go.jp 電波法 無線LAN 技術基準適合証明 免許不要<br>site:elaws.e-gov.go.jp 電波法 第4条 無線局 免許を要しない 技術基準適合証明<br>site:tele.soumu.go.jp 技適マーク Wi-Fi 日本 国内 使用<br>総務省 電波利用ホームページ 技適マーク 無線LAN<br>総務省 Wi-Fi 技適マーク 電波法<br>e-Gov 電波法 第4条 無線局 免許を要しない<br>e-Gov 電波法 第38条の7 技術基準適合証明 | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0004 | https://www.meti.go.jp/policy/consumer/seian/shouan/act_outline.html | site:meti.go.jp 扇風機 電気用品安全法 長期使用製品安全表示制度 | complete | 2026-08-22T00:00:00+09:00 |

## 採用・除外・保留候補Sourceと理由

| ID | 候補Source | 扱い | 理由 |
|---|---|---|---|
| RDL-0001 | SRC-0001<br>SRC-0002<br>SRC-0003 | adopted_candidate | 電安法第8条の技術基準適合義務と、施行令及び経済産業省一覧の扇風機分類を候補チェーンに採用した。定格消費電力等が未確定のため適用判定は保留する。 |
| RDL-0002 | SRC-0004 | adopted_candidate | 省令第20条と経済産業省公式制度案内が家庭用扇風機を長期使用表示の対象として示すため候補チェーンに採用した。 |
| RDL-0003 | SRC-0005 | on_hold | 電波法第4条及び第38条の7を候補Sourceとして保持するが、Wi-Fi搭載有無と無線仕様が未決定のため適用候補を保留する。 |
| RDL-0004 | SRC-0006 | excluded | 長期使用製品安全表示制度の概要確認には有用だが、本モデルでは表示義務の直接根拠を電気用品の技術上の基準を定める省令第20条としたため、規範チェーンから除外した。 |

## 網羅性の限界・人によるinventory確認

| ID | Query記録状態 | inventory確認 |
|---|---|---|
| RDL-0001 | complete | pending |
| RDL-0002 | complete | pending |
| RDL-0003 | complete | pending |
| RDL-0004 | complete | pending |

> Queryまたは除外候補が未記録、あるいは人のinventory確認がpendingの場合、探索の網羅性を主張できません。
