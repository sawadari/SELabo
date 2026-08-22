# Compliance Layer C1評価実行

履歴を引き継がない新規サブエージェントで行った自動探索評価は、[strict C1-blind](../compliance-integrated-se-prompt-blind-c1-strict/README.md)として別枠に保存しています。本runは既知Finding修復を含むため、Compliance Layer単独の効果判定には使用しません。

## 目的

実験1で使用したスマート扇風機、懐中電灯、モバイルバッテリーの合成Q&Aを再利用し、`hierarchical-se-prompt`へ`compliance-integrated-se-prompt`を追加するC1条件を評価しました。

3製品は別々のサブエージェントが担当し、製品ごとにコンパクトな正本候補`candidate_model.json`と評価記録`evaluation.md`を作成しました。調整担当は3モデルを同じ合成Schemaで再検証し、横断Meta Reviewを行いました。

## 評価条件

| 項目 | 内容 |
|---|---|
| 実行日 | 2026-08-22（Asia/Tokyo） |
| 条件 | C1：元実験＋Compliance拡張 |
| 入力 | 2026-08-21の3製品合成Q&Aと独立レビュー |
| 生成 | 製品ごとに独立したサブエージェント |
| 製品内評価 | 生成担当による規則検査。J0相当 |
| 横断評価 | 調整担当によるSchema再検証とMeta Review |
| 人の校正 | 未実施 |

既存の独立レビューFindingを各生成担当へ渡し、最小修復を指示しました。そのため本実行は純粋なブラインドC1ではなく、実質的に`C1-remediated`です。B0からのGate改善をCompliance Layerだけの効果とは扱いません。

## 製品別結果

| 製品 | B0 Gate | C1 Gate | Applicability | Source→Evidence Requirement | Evidence Item |
|---|---|---|---:|---:|---:|
| [スマート扇風機](smart-fan/evaluation.md) | `below_reviewable` | `reviewable_40_candidate` | 3/3 `uncertain` | 6/6 Obligation | 0 |
| [懐中電灯](flashlight/evaluation.md) | `below_reviewable` | `reviewable_40_candidate` | 2/2 `uncertain` | 3/3 Obligation | 0 |
| [モバイルバッテリー](mobile-battery/evaluation.md) | `below_reviewable` | `reviewable_40_candidate` | 4/4 `uncertain` | 7/7 Obligation | 0 |

各製品の正本候補は次のファイルです。

- [スマート扇風機のcandidate_model.json](smart-fan/candidate_model.json)
- [懐中電灯のcandidate_model.json](flashlight/candidate_model.json)
- [モバイルバッテリーのcandidate_model.json](mobile-battery/candidate_model.json)

## 横断集計

| 指標 | 3製品合計 |
|---|---:|
| Stakeholder / Need / Requirement | 10 / 14 / 23 |
| Scenario / Validation Case | 7 / 14 |
| Behavior / Structure / Verification Case | 19 / 8 / 23 |
| 主要Need→Requirement | 14/14 |
| 主要Requirement→Behavior / Structure | 23/23 |
| 主要Requirement→V&V候補 | 23/23 |
| Authority / Source / Provision | 7 / 17 / 20 |
| NormativeStatement / ApplicabilityAssessment / Obligation | 17 / 9 / 16 |
| `uncertain` Applicability | 9/9 |
| EngineeringProjection / EvidenceRequirement | 29 / 23 |
| ObligationからEvidenceRequirementへ到達 | 16/16 |
| 投影のないObligation | 0 |
| Mandatory・ProhibitionでEvidenceRequirementなし | 0 |
| EvidenceItem / Attestation | 0 / 0 |
| AssessmentResult | 9件、全件`not_performed` |
| 正式適用・適合・認証の確定主張 | 0 |
| Need Validation | 14/14 |
| 型付き非Product投影先 | 13件 |
| 決定的に生成したTrace関係 | 132 / 88 / 197 |
| `relations[]` | 3製品とも0件（補助関係専用） |

## 機械検証

調整担当が3つの`candidate_model.json`を再度読み込み、元SchemaをRegistryへ登録したJSON Schema Draft 2020-12の合成検証を行いました。

- JSON構文：3/3 PASS
- v0.3.1合成Schema：3/3 PASS、エラー0件
- Schema外のID参照・投影先種別・Evidence到達検査：3/3 PASS
- 型付き直接参照からの`09_traceability.csv`生成：3/3 PASS
- Applicabilityの`human_confirmation_required=true`かつ`human_confirmation_state=pending`：9/9
- `regulatory_candidate`：0件
- Obligationの投影欠落：0件
- Mandatory・Prohibition ObligationのEvidenceRequirement欠落：0件
- `conforming`、`nonconforming`、Attestation：0件
- Assurance統合回帰：正例4件、負例65件PASS

Schema合格は法的正確性、製品安全、規格適合または認証取得を示しません。

## Pilot判断

横断結果は[meta_review.md](meta_review.md)にまとめています。初回判断カテゴリは`修正`です。v0.2のSchema・Trace修正後、独立J1が3役とも全製品`revise`と判定したため、v0.3.1でHigh Findingと残件を修正しました。独立再レビュー完了まではMeta-Judge Gateを`revise`に保ちます。

Complianceの意味境界、`uncertain`の保持、Evidence RequirementとEvidence Itemの分離は3製品で再現しました。Process、Documentation、Supplier投影は共通の型付き`projection_targets[]`へ移行し、製品間の表現分岐を解消しました。次はブラインドC1と専門家入力付きC2を分けて行います。

主要Traceは各要素内の型付き直接参照を正本とし、`relations[]`を補助関係専用とする規則へ統一しました。3製品の`09_traceability.csv`は同じvalidatorで再生成済みです。

## 未実施

- 元出力契約の完全Bundle生成（追加5成果物は3製品で生成・一致検査済み）
- SysML、ReqIF、OSCAL、SACM adapter検証
- v0.3.1修正後の独立Compliance、SE、Assurance再レビュー（実行中）
- 法務・法規・認証・安全専門家による校正
- 実在するEvidence Itemを使ったAssessment ResultとAttestationの評価
- 生成時間、専門家レビュー時間、SEレビュー時間の計測

独立J1の記録は[Compliance Review](reviews/compliance_review.md)、[SE Review](reviews/se_review.md)、[Assurance Review](reviews/assurance_review.md)です。
