# Regulatory Discovery Log

## 対象構成と市場

| ID | 市場 | 構成 |
|---|---|---|
| RDL-0001 | 日本市場 | CFG-0001 |
| RDL-0002 | 国際輸送 | CFG-0001 |
| RDL-0003 | 日本の航空旅客輸送 | CFG-0001 |

## 探索した公式台帳・探索queryと実行時点

| ID | 公式探索先 | Query | Query記録状態 | 実行時点 |
|---|---|---|---|---|
| RDL-0001 | https://www.meti.go.jp/product_safety/consumer/lithium_ion_battery.html<br>https://www.meti.go.jp/policy/consumer/seian/denan/subject01.html | site:meti.go.jp モバイルバッテリー 電気用品安全法 PSE リチウムイオン蓄電池 | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0002 | https://unece.org/transport/dangerous-goods/rev8-files<br>https://unece.org/transport/publications/un-manual-tests-and-criteria-rev8-2023 | site:unece.org UN 38.3 lithium battery test summary Manual of Tests and Criteria | complete | 2026-08-22T00:00:00+09:00 |
| RDL-0003 | https://www.mlit.go.jp/report/press/kouku10_hh_000310.html<br>https://www.mlit.go.jp/common/001469460.pdf | site:mlit.go.jp モバイルバッテリー 航空機 持ち込み リチウムイオン電池 100Wh | complete | 2026-08-22T00:00:00+09:00 |

## 採用・除外・保留候補Sourceと理由

| ID | 候補Source | 扱い | 理由 |
|---|---|---|---|
| RDL-0001 | SRC-0001 | adopted_candidate | METI公式案内をDENAN候補チェーンの探索起点として採用した。対象該当性と法令版は保留した。 |
| RDL-0002 | SRC-0002 | adopted_candidate | UNECE公式のRevision 8配布ページを38.3および試験要約候補の探索起点として採用した。適用版と拘束経路は保留した。 |
| RDL-0003 | SRC-0003 | adopted_candidate | 国土交通省の2026年4月24日適用案内を日本の航空旅客携行候補として採用した。便別の運送人条件は保留した。 |

## 網羅性の限界・人によるinventory確認

| ID | Query記録状態 | inventory確認 |
|---|---|---|
| RDL-0001 | complete | pending |
| RDL-0002 | complete | pending |
| RDL-0003 | complete | pending |

> Queryまたは除外候補が未記録、あるいは人のinventory確認がpendingの場合、探索の網羅性を主張できません。
