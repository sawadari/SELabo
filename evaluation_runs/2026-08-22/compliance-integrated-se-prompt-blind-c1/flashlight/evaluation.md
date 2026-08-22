# 盲検C1評価：懐中電灯

## 結論

- 40点初稿状態：`reviewable_40_candidate`
- モデル品質：`pass_with_provisional_assumption`
- Assurance outcome：`not_performed`
- Compliance approval：`not_a_compliance_approval=true`
- 法規inventoryの網羅性、個別適用性、技術基準適合、認証は人確認待ちである。

入力は同フォルダの`input.md`、許可されたprompt/config/schema/scripts、実行時の公式Web検索に限定した。修正版C1、B0成果物・Review、他製品の盲検出力は参照していない。

## 自動探索結果

実検索query、公式探索先、候補Source、採否、時刻は`candidate_model.json#/compliance/regulatory_discovery_log`を正本とし、`21_regulatory_discovery_log.md`へ投影した。5記録すべて`query_log_state=complete`、`human_inventory_confirmation_state=pending`である。

| 候補 | 採否 | 理由 |
|---|---|---|
| [METI 電気用品安全法対象情報](https://www.meti.go.jp/policy/consumer/seian/denan/subject01.html) | `adopted_candidate` | リチウムイオン蓄電池や同梱直流電源装置が構成依存で候補。電池仕様・販売単位が不明のため適用性は`uncertain` |
| [消費者庁 重大製品事故報告制度](https://www.caa.go.jp/policies/policy/consumer_safety/centralization_of_accident_information/) | `adopted_candidate` | 一般消費者向け製品候補の流通後義務。製品該当性と製造・輸入主体が不明のため`uncertain` |
| [消費者庁 家庭用品品質表示法対象範囲](https://www.caa.go.jp/policies/policy/representation/household_goods/outline/outline_04.html) | `on_hold` | 指定品目制度は確認できたが、懐中電灯の個別該当性を確定できない |
| [IEC 60598-2-8:2013](https://webstore.iec.ch/en/publication/2578) | `on_hold` | ハンドランプ規格候補だが、製品分類、国内での拘束根拠、本文・最新版確認が不足 |
| [ICAO Dangerous Goods Technical Instructions](https://www.icao.int/Dangerous-Goods/Technical-Instructions) | `on_hold` | 航空輸送とリチウム電池構成が未決定。版・具体要件は未確認 |

検索対象外の法域・市場は網羅していない。日本も入力確定情報ではなく探索仮定である。

## 標準化メトリクス

| 指標 | 結果 |
|---|---:|
| Stakeholder | 1 |
| Need | 2 |
| Need Validation Case | 2 |
| Requirement | 4 |
| Requirement Verification Case | 4 |
| Behavior / Structure | 3 / 1 |
| Authority / Source / Discovery Record | 4 / 5 / 5 |
| ApplicabilityAssessment | 2（`uncertain` 2） |
| Obligation / EngineeringProjection | 2 / 5 |
| ProjectionTarget | 2 |
| EvidenceRequirement / EvidenceItem | 5 / 0 |
| AssessmentResult | 2（`not_performed` 2） |
| 派生Trace行 | 65 |
| 架空EvidenceItem | 0 |
| 適合・認証確定主張 | 0 |

## 40点Gate

| 評価軸 | 判定 | 根拠 |
|---|---|---|
| Stakeholder → Need | `sufficient` | 2/2 NeedがStakeholderへ接続 |
| Need → Validation | `sufficient` | 2/2 Needが独立Validation Caseと代表Scenarioへ接続 |
| Need → Requirement | `sufficient` | 2/2主要Needが1件以上の要求へ接続 |
| Requirement → Behavior / Structure | `sufficient` | 4/4要求がBehaviorと共通Structureへ接続 |
| Requirement → Verification | `sufficient` | 4/4要求がVerification CaseとEvidenceRequirementへ接続 |
| 1要求1中心義務 | `sufficient` | 照明切替、通知、計画消灯、条件付きDENAN制約を分離 |
| 数値・安全・適用性 | `weak` | 光量、猶予時間、温度、環境等級、電池・充電方式、市場が未決定 |
| 過剰詳細 | `not_applicable` | 部品型番、公差、詳細実装を創作していない |

人がレビューを開始できる最小Traceはあるが、意味妥当性と要求値は未確認であるため、承認済み要求には昇格できない。

## Compliance品質

- Authority、Source、Provision、NormativeStatement、ApplicabilityAssessment、Obligation、EngineeringProjection、EvidenceRequirementを分離した。
- DENAN由来の製品制約候補だけを`REQ-0004`へ投影した。
- 重大製品事故報告は`projection_targets`のProcess / Documentationへ投影し、対象システムの製品要求へ偽装していない。
- 2 Mandatory ObligationはいずれもEngineeringProjectionとEvidenceRequirementを持つ。
- EvidenceItemは0件で、将来必要な証拠を取得済みと表現していない。
- ApplicabilityAssessmentは2件とも`human_confirmation_state=pending`である。
- Generator以外のCompliance / SE / Assurance Gateは`review_pending`、Meta-Judgeは`not_performed`である。

## 機械検証

| 検査 | 結果 |
|---|---|
| JSON構文・合成Schema | PASS |
| 意味参照・型付き投影 | PASS |
| ID一意性 | PASS（61 ID） |
| `09_traceability.csv`決定的生成 | PASS（65行） |
| Compliance view export | PASS（5ファイル） |
| Export `--check` | PASS |

実行コマンド：

```powershell
python experiments/compliance-integrated-se-prompt/scripts/validate_candidate.py evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/flashlight/candidate_model.json --trace-csv evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/flashlight/09_traceability.csv
python experiments/compliance-integrated-se-prompt/scripts/export_compliance_views.py evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/flashlight/candidate_model.json --output-dir evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1/flashlight --check
```

## 人の確認バックログ

1. 販売市場と法域を決定する。
2. 電池化学系、体積エネルギー密度、内蔵・交換式、充電器同梱、販売単位を決定する。
3. 製造・輸入・販売・事故報告の責任主体を確認する。
4. DENAN、家庭用品品質表示、JIS / IEC、航空輸送を含むinventoryの採否と網羅性を法規責任者が確認する。
5. 低電池閾値、通知方式、通知後猶予、最低光出力、安全停止例外、温度条件、耐水・防じん・落下条件を決定する。
6. Compliance、SE、Assurance ReviewerとMeta-Judgeを独立実行する。

本評価は法的助言、適用判断、設計承認、適合性評価または認証判定ではない。
