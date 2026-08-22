# Regulatory Discovery Log

## 対象構成と市場

| ID | 市場 | 構成 |
|---|---|---|
| RDL-SF-PSE | 日本国内販売候補 | CFG-SF-CONCEPT |
| RDL-SF-LONG-USE | 日本国内販売候補 | CFG-SF-CONCEPT |
| RDL-SF-RADIO | 日本国内販売候補 | CFG-SF-CONCEPT |
| RDL-SF-ENERGY | 日本国内販売候補 | CFG-SF-CONCEPT |

## 探索した公式台帳・探索queryと実行時点

| ID | 公式探索先 | Query | Query記録状態 | 実行時点 |
|---|---|---|---|---|
| RDL-SF-PSE | 経済産業省 電気用品安全法ページ<br>e-Gov法令検索 | site:meti.go.jp 電気用品安全法 扇風機 特定電気用品以外の電気用品<br>site:meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku 扇風機 別表第八 10°<br>site:meti.go.jp "扇風機、換気扇、サーキュレーター及び送風機"<br>site:laws.e-gov.go.jp/law/336AC0000000234 電気用品安全法 第八条 | complete | 2026-08-22T09:24:58+09:00 |
| RDL-SF-LONG-USE | 経済産業省 製品安全 長期使用製品安全点検・表示制度 | site:meti.go.jp 扇風機 長期使用製品安全表示制度 公式 | complete | 2026-08-22T09:24:58+09:00 |
| RDL-SF-RADIO | e-Gov法令検索 電波法<br>e-Gov法令検索 特定無線設備規則 | site:soumu.go.jp 無線LAN 技術基準適合証明 電波法 公式<br>site:laws.e-gov.go.jp 電波法 第四条 適合表示無線設備 無線LAN<br>site:laws.e-gov.go.jp 特定無線設備の技術基準適合証明等に関する規則 第二条 無線LAN<br>site:tele.soumu.go.jp 技適マーク 無線LAN 公式 | complete | 2026-08-22T09:24:58+09:00 |
| RDL-SF-ENERGY | 資源エネルギー庁 トップランナー・小売事業者表示制度 | site:meti.go.jp 省エネ法 扇風機 トップランナー 公式<br>site:meti.go.jp トップランナー制度 対象機器 扇風機 | complete | 2026-08-22T09:24:58+09:00 |

## 採用・除外・保留候補Sourceと理由

| ID | 候補Source | 扱い | 理由 |
|---|---|---|---|
| RDL-SF-PSE | SRC-SF-PSE-ACT<br>SRC-SF-PSE-INTERP | adopted_candidate | 扇風機の品目候補、第8条および別表第八の扇風機個別事項を公式情報で確認した。給電方式、定格および適合経路は未確認 |
| RDL-SF-LONG-USE | SRC-SF-LONG-USE<br>SRC-SF-PSE-INTERP | adopted_candidate | 公式ページで扇風機を表示制度候補として確認し、具体的Provisionは別表第八(41)ホへ接続した。対象範囲は人確認待ち |
| RDL-SF-RADIO | SRC-SF-RADIO-ACT | on_hold | 第4条と特定無線設備制度は確認したが、無線仕様と2026-08-22時点の現行Revision IDを確認できないため適用chainを保留候補として保持する |
| RDL-SF-ENERGY | SRC-SF-ENERGY-LIST | excluded | 取得した公式対象機器一覧で扇風機を確認できなかったため今回のObligation chainへ採用しない。正式なnot_applicable判断ではない |

## 網羅性の限界・人によるinventory確認

| ID | Query記録状態 | inventory確認 |
|---|---|---|
| RDL-SF-PSE | complete | pending |
| RDL-SF-LONG-USE | complete | pending |
| RDL-SF-RADIO | complete | pending |
| RDL-SF-ENERGY | complete | pending |

> Queryまたは除外候補が未記録、あるいは人のinventory確認がpendingの場合、探索の網羅性を主張できません。
