# 3製品 strict C1-blind 評価

## 結論

履歴を引き継がない新規サブエージェントに、各製品のQ&A、実験prompt/config/schema、代表fixtureだけを与えて再生成した。既存B0、C1-remediated、review、先行blind出力は入力に含めていない。

3製品とも、公式情報を検索して製品別の法規・規格候補を自動抽出し、生query、候補、採用・保留・除外理由を記録できた。Schema・意味検証、決定的Trace生成、Compliance View同期にも合格した。一方、候補inventoryの完全性とSource同一性は保証できず、製品適合の総合Gateは`revise`とする。

## strict条件

- サブエージェント起動時に会話履歴を渡さない。
- 製品情報は親runの`input.md`だけを読む。
- 既存の評価run、修正版、review、他製品出力を読まない。
- Web探索は所管官庁、e-Gov、UNECE、JISC等の公式一次情報を優先する。
- AI生成Applicabilityは`uncertain / pending`から昇格させない。
- 実在artifactがないためEvidence ItemとAttestationを生成せず、Assessment Resultを`not_performed`とする。

先に同じ製品担当を再利用して作成した`../compliance-integrated-se-prompt-blind-c1/`はファイル入力を隔離した参考runであるが、担当履歴まで消去していないため、効果判定から除外する。

## 機械検証

| 製品 | ID | Trace | raw query | Discovery record | Source / Provision | APP / OBL / EPR / EVR | validator | 17–21同期 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| スマート扇風機 | 54 | 70 | 17 | 4 | 6 / 6 | 3 / 3 / 6 / 3 | PASS | PASS |
| 懐中電灯 | 50 | 61 | 12 | 3 | 7 / 6 | 2 / 2 / 4 / 2 | PASS | PASS |
| モバイルバッテリー | 57 | 67 | 3 | 3 | 3 / 3 | 3 / 3 / 6 / 3 | PASS | PASS |

全10 Discovery recordは`query_log_state=complete`で、inventory確認は`pending`である。全8 Applicability Assessmentは`uncertain / pending`、Evidence ItemとAttestationは0件、全Assessment Resultは`not_performed`である。

## 自動発見した主要候補

| 製品 | 自動発見した候補 | 保留・除外または不足 |
|---|---|---|
| スマート扇風機 | 電気用品安全法と施行令、技術基準省令、長期使用表示候補、Wi-Fi搭載時の電波法候補 | 電源・定格・製品分類・事業者区分・無線構成が未確定。公式候補の意味付けは人レビューが必要 |
| 懐中電灯 | 電安法上の充電式携帯電灯候補、消費生活用製品安全法の重大製品事故報告候補 | 電池・充電方式で分類が変わる。JISCカタログ候補は規格番号・版を選ばず保留 |
| モバイルバッテリー | METIのリチウムイオン電池安全情報、UNECE UN 38.3/test-summary候補、国土交通省の航空旅客携行候補 | 電安法の法令正本・対象分類、航空告示の条項、輸送モード・便別条件のinventoryが不足 |

## C1-remediatedとの比較

| 指標 | C1-remediated（source patch後） | strict C1-blind | 解釈 |
|---|---:|---:|---|
| Source | 3 / 6 / 8 | 6 / 7 / 3 | strictは自動探索だけでも候補を得たが、製品別の深さが不均一 |
| Applicability | 3 / 2 / 4 | 3 / 2 / 3 | いずれも人確認前の候補状態を保持 |
| Obligation | 6 / 3 / 7 | 3 / 2 / 3 | remediatedは独立レビューとsource patchで条項・義務を細分化 |
| Evidence Requirement | 9 / 7 / 7 | 3 / 2 / 3 | strictは最小chainであり、証拠計画の網羅性を示さない |
| raw query保存 | 3製品とも`unavailable_legacy_run` | 17 / 12 / 3 | strictで自動探索の実行証跡を初めて評価可能にした |

数値順はスマート扇風機／懐中電灯／モバイルバッテリーである。C1-remediatedは既知Finding修復を含むため、差をCompliance Layer単独の効果とは扱わない。

## 判定境界

- `PASS`はJSON、参照、Trace、exportの機械的一貫性だけを示す。
- 検索ログが`complete`でも、検索inventoryが完全であるとは限らない。
- `retrieved_from_official_source`や公式URLだけでは、権限者によるSource版・条項位置・適用性確認を代替しない。
- このrunは法的助言、製品適合、PSE表示可否、UN 38.3適合、航空輸送可否、認証取得または市場投入承認を主張しない。

独立Compliance Reviewは[blind_c1_review.md](blind_c1_review.md)に記録する。
