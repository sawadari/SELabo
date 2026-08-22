# スマート扇風機 C1-blind 評価

## 結論

本出力は、Compliance Layerを含む**人レビュー用の40点初稿候補**として、生成器レベルのStop Ruleを回避し、Schema v0.3.1と意味的参照検査を通過した。モデル構造品質は`pass_with_provisional_assumption`、製品の保証結果は`not_performed`である。Compliance Reviewer、SE Reviewer、Assurance Reviewerは`review_pending`、Meta-Judgeは`not_performed`であり、総合Pass、正式な法的適用、規格適合、PSE表示可否、技適適合、認証取得のいずれも主張しない。

日本国内販売は入力にないため探索用の暫定仮定である。5件のApplicabilityAssessmentはすべて`uncertain`かつ人確認待ちであり、法規候補探索の網羅性も人によるinventory確認待ちである。

## 盲検条件

- 条件: `C1-blind`
- 入力: `input.md`の合成Q&Aだけを製品情報として使用
- 使用した実験資産: 元実験のprompt/config/schema、およびCompliance拡張の01–08、README、schemas、scripts
- 参照しなかったもの: 既存C1修正版、B0出力、レビュー、他製品のblind出力
- 対象時点: 2026-08-22
- 対象構成: `CFG-SF-CONCEPT`（ユーザー確認前のconcept candidate）
- 法域・市場: 日本国内販売を探索用に仮定。確定していない

## Web自動探索

検索は所管官庁、e-Gov法令検索、資源エネルギー庁等の一次情報に限定した。実行時の生検索語は`candidate_model.json`の`regulatory_discovery_log[].queries`に保存し、4探索記録すべてを`query_log_state=complete`とした。

### 実行したraw query（11件）

1. `site:meti.go.jp 電気用品安全法 扇風機 特定電気用品以外の電気用品`
2. `site:meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku 扇風機 別表第八 10°`
3. `site:meti.go.jp "扇風機、換気扇、サーキュレーター及び送風機"`
4. `site:laws.e-gov.go.jp/law/336AC0000000234 電気用品安全法 第八条`
5. `site:meti.go.jp 扇風機 長期使用製品安全表示制度 公式`
6. `site:soumu.go.jp 無線LAN 技術基準適合証明 電波法 公式`
7. `site:laws.e-gov.go.jp 電波法 第四条 適合表示無線設備 無線LAN`
8. `site:laws.e-gov.go.jp 特定無線設備の技術基準適合証明等に関する規則 第二条 無線LAN`
9. `site:tele.soumu.go.jp 技適マーク 無線LAN 公式`
10. `site:meti.go.jp 省エネ法 扇風機 トップランナー 公式`
11. `site:meti.go.jp トップランナー制度 対象機器 扇風機`

### 候補と採否

| 探索観点 | 候補 | 処置 | 理由 |
|---|---|---|---|
| 電気用品安全 | 電気用品安全法、METI技術基準解釈別表第八 | `adopted_candidate` | 扇風機の品目候補、法第8条、安定性および長期使用表示の候補規定を公式原典で確認。ただし定格、製品分類、事業者区分、適用経路は未確認 |
| 長期使用表示 | METI長期使用製品安全点検・表示制度ページ、別表第八(41)ホ | `adopted_candidate` | 扇風機が表示制度の対象候補であることを確認。個別製品への適用は未確認 |
| 無線 | 電波法第4条、特定無線設備制度 | `on_hold` | Wi-Fi搭載可能性から候補化したが、無線仕様、モジュール、現行Revisionおよび設備分類が未確認 |
| 省エネ表示・トップランナー | 資源エネルギー庁の対象機器一覧 | `excluded` | 取得した一覧で扇風機を確認できず、今回のObligation chainから除外。正式な`not_applicable`判断ではない |

### 参照した公式一次情報

- [e-Gov 電気用品安全法](https://laws.e-gov.go.jp/law/336AC0000000234?occasion_date=20260611)
- [METI 特定電気用品以外の電気用品一覧](https://www.meti.go.jp/policy/consumer/seian/denan/non_specified_electrical.html)
- [METI 技術基準解釈 別表第八（2026-06-01 PDF）](https://www.meti.go.jp/policy/consumer/seian/denan/kaishaku/gijutsukijunkaishaku/beppyoudai8_260601.pdf)
- [METI 長期使用製品安全点検・表示制度](https://www.meti.go.jp/product_safety/producer/shouan/07_tyouki.html)
- [e-Gov 電波法（取得できた2024-04-01時点表示）](https://laws.e-gov.go.jp/document?lawid=325AC0000000131_20240401_504AC0100000052)
- [資源エネルギー庁 小売事業者表示制度・トップランナー対象一覧](https://www.enecho.meti.go.jp/category/saving_and_new/saving/enterprise/retail/)

電波法は2026-08-22時点の現行Revision IDを確認できなかったため、Sourceの状態を`unknown`、適用性を`uncertain`とした。規格本文の転載は行っていない。

## 標準化メトリクス

| 指標 | C1-blind結果 |
|---|---:|
| raw query | 11 |
| discovery record (`complete`) | 4 / 4 |
| Source / Provision / NormativeStatement | 5 / 5 / 5 |
| ApplicabilityAssessment (`uncertain`) | 5 (5) |
| Obligation / EngineeringProjection | 5 / 12 |
| Product / Process / Assurance / Documentation / Evidence投影 | 1 / 2 / 1 / 2 / 5 |
| Supplier投影（参考） | 1 |
| 原典からEvidenceRequirementへ到達するObligation経路 | 5 |
| 投影のないObligation | 0 |
| mandatoryだがEvidenceRequirementのないObligation | 0 |
| EvidenceRequirement / 実在確認済みEvidenceItem / 架空EvidenceItem | 11 / 0 / 0 |
| AssessmentActivity planned / AssessmentResult not_performed | 2 / 2 |
| Attestation | 0 |
| Need Validation候補接続 | 5 / 5 (100%) |
| Requirement Verification候補接続 | 7 / 7 (100%) |
| 決定生成したtrace行 | 128 |
| 人が採用・修正・却下した判断 | 0（全件pending） |
| 初稿生成時間・各Reviewer時間 | 未計測 / 未実施 |
| False Pass / False Certification Claim | 0 / 0（生成器静的確認） |

投影種別のProductは`constraint_requirement`をProduct系として集計した。到達経路は、Source→Provision→NormativeStatement→ApplicabilityAssessment→Obligation→EvidenceRequirementが解決する5 Obligation chainを数えたものであり、法的な有効性を示す指標ではない。

## C-品質規則の自己評価

| 規則 | 結果 | 根拠・留保 |
|---|---|---|
| C-SRC-01 | `pass_with_provisional_assumption` | AuthorityとSourceを分離し公式locatorを保持。電波法現行版、補助ページの版は未確認 |
| C-SRC-02 | `pass` | 採用した5 Provisionは取得した公式原典の位置へ戻る |
| C-SRC-03 | `pass` | 原典、解釈、適用性、Obligationを別オブジェクト化 |
| C-APP-01 | `pass_with_provisional_assumption` | 判断コンテキストを保持するが市場・分類・構成仕様は仮定またはunknown |
| C-APP-02 | `pass` | 法律の直接法規候補と技術基準解釈等の根拠種別を分離 |
| C-APP-03 | `pass` | 5件すべて`uncertain`、confirmation pending、確認者・日時なし |
| C-APP-04 | `pass` | 市場、分類、構成、原典版等のreview triggerを保持 |
| C-OBL-01 | `pass` | 各ObligationがNormativeStatementとApplicabilityAssessmentへ戻る |
| C-EPR-01 | `pass` | 5/5 Obligationに1件以上の投影あり |
| C-EPR-02 | `pass` | 非Product投影は型付き`projection_targets`、Evidence投影はEVRへ接続 |
| C-EPR-03 | `pass` | 全Requirementに導出元あり。Compliance由来REQはObligationとProjectionを明記 |
| C-EPR-04 | `pass` | 法令要素自体をSysML Requirement化していない |
| C-EVI-01 | `pass` | 証拠計画11件と実在証拠0件を分離 |
| C-EVI-02 | `not_applicable` | EvidenceItemなし |
| C-EVI-03 | `pass` | mandatory 5/5をEVRが覆う |
| C-AST-01 | `pass` | PSE系・無線系の活動をplannedとして分離 |
| C-ASR-01 | `pass` | 証拠未評価の結果を`not_performed`とした |
| C-ATT-01 | `not_applicable` | Attestationなし |
| C-CHG-01 | `not_applicable` | stale/superseded Sourceなし |
| C-MAP-01 | `not_applicable` | 同等性等のMappingを主張していない |
| C-TRC-01 | `pass` | 型付き直接参照を正本とした |
| C-TRC-02 | `pass` | 128行を正本からexportし、全参照検査を通過 |
| C-VAL-01 | `pass` | Need 5/5とValidation Case、Requirement 7/7とVerification Caseを別に接続 |
| C-CTX-01 | `pass` | 構成と責任ロール参照が正本内で解決 |
| C-DISC-01 | `pass_with_provisional_assumption` | 11 queryと採用・保留・除外理由を保存。inventory確認はpending |
| C-GATE-01 | `pass` | model qualityとassurance outcomeを分離し、`not_a_compliance_approval=true` |
| C-ASR-02 | `pass` | definitive outcomeを生成せず、全結果を未実施とした |
| C-ATT-02 | `not_applicable` | issued Attestationなし |

これは生成器による構造・トレーサビリティ自己評価であり、各規則の専門家承認ではない。

## 40点Gate

生成器の静的確認では、原典・条項の創作、AIによる正式適用判断、追跡不能な重大Obligation、Productと非Product投影の混同、EvidenceRequirementとEvidenceItemの混同は検出されなかった。このため`below_reviewable`には分類せず、**40点初稿のレビュー可能候補**とする。

ただし、Reviewer別Gateは未完了である。したがって「40点Gate通過」は生成器レベルに限定し、総合Gateは`pending`とする。

## B0比較

盲検条件を守るため、このrunではB0成果物を閲覧せず、定量差分を**実施していない**。上表は後続の独立集計でB0と比較できる正規化指標である。B0比較者は、概念混同、非Product誤分類、有効trace、架空条項・証拠・認証主張、人確認バックログを同一定義で比較する必要がある。

## 人レビュー・確認バックログ

1. 販売国・市場、定格電圧、消費電力、AC接続方式、電池・充電器の同梱有無を確定する。
2. 「扇風機」または他品目としてのPSE分類、届出事業者・輸入者等の責任主体を確認する。
3. 別表第八(41)の安定性および長期使用表示候補の正確な適用範囲と最新版をCompliance Reviewerが確認する。
4. Wi-Fi/Bluetoothの搭載、周波数、出力、認証済み無線モジュールの利用有無を確定し、電波法と特定無線設備規則の現行版・該当区分を確認する。
5. 騒音、風量、停止時間、清掃中インターロック、cover-open検出の閾値と試験条件をSE Reviewerが決定する。
6. 児童接触、転倒、過熱、感電、発火、清掃時再起動を含む正式なhazard/risk分析を追加する。
7. 構成baseline、実在artifact、Evidence Item、評価者権限、完了したAssessment Activityが揃うまで適合評価を開始しない。

## 検証記録

実行コマンド:

```powershell
python experiments/compliance-integrated-se-prompt/scripts/validate_candidate.py evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/smart-fan/candidate_model.json --trace-csv evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/smart-fan/09_traceability.csv
python experiments/compliance-integrated-se-prompt/scripts/export_compliance_views.py evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/smart-fan/candidate_model.json --output-dir evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/smart-fan
python experiments/compliance-integrated-se-prompt/scripts/export_compliance_views.py evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/smart-fan/candidate_model.json --output-dir evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/smart-fan --check
```

- validator: `PASS` — `ids=107`, `derived_relations=128`
- trace export: `09_traceability.csv`を決定生成
- compliance views export: `PASS exported files=5`
- export `--check`: `PASS checked files=5`
- JSON構文: `python -m json.tool` 成功

## 非主張事項

この成果物は法的助言、法規inventoryの完全性、規格解釈の承認、製品の適合、PSE表示可否、技適取得、認証、出荷承認を意味しない。検索していない候補を発見済みとは扱わず、確認できない版、条項、適用性は確定しない。
