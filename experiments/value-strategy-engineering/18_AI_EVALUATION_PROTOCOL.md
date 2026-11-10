# VSE独立AI評価プロトコル v1.0

## 1. 基本原則
Generatorが自分の出力を見直すJ0は独立評価ではない。複数の「専門家役」を同じLLMに演じさせても、実在の専門家による妥当性確認にはならない。仮想顧客の「購入したい」は実需要の証拠ではない。

| Tier | 手続き | 価値と限界 |
|---|---|---|
| J0 | Generatorの自己検査 | 内部矛盾の一次発見。独立性なし |
| J1 | 同じモデル、別会話、生成結果のみ評価 | 会話由来の誘導を減らすがモデル偏りあり |
| J2 | 異なるモデルの独立Reviewer | モデル偏りが減る可能性。正しさは保証しない |
| J3 | 4つの専門Reviewerと独立Meta-Judge | 複数観点を統合。AI内の一致は実証ではない |
| J4 | J3＋実務専門家/実顧客による校正 | 人間の現実適合性を一部確認。サンプル設計が必要 |

## 2. 独立Reviewerの立場
- **Marketing Strategy Reviewer**：顧客のセグメント、競合、価値、資源配分、戦略代替案、非選択、マーケティングの妥当性。
- **B2B Sales Reviewer**：購買プロセス、社内推進者と決裁者、商談転換、提供能力、営業費用、収益性、長期関係。
- **Skeptical Customer Simulator**：導入負担、代替策、現状維持、予算懸念、内部合意。**シミュレーターは調査対象者ではない**。
- **Systems Engineering Reviewer**：境界、モデル分離、ID、意味的Trace、仮説と因果の混同、変更・更新、Gate適合。
- **Evidence & Causality Reviewer**：ソースの偏り、反対証拠、因果識別、測定妥当性、数値の根拠、外部妥当性。

## 3. 実行ルール
Reviewerは相互のFindingを見ず、同じ匿名化入力と同じVSE JSONから独立して所定の評価項目を記録する。共通の`04_QUALITY_RULES.md`に基づき、Findingにrule_id、証拠ID、severity、具体的な最小修正、human_requiredを付与する。問題が無いときは「検査した範囲」を明示する。

Meta-Judgeは(a)記載根拠の実在性、(b)重複排除、(c)Hard Blocker、(d)Gate判定、(e)異議・低信頼度の扱いを順に行う。新しい市場の『事実』を追加してはいけない。

## 4. Finding形式
```json
{
  "id": "FND-0001",
  "reviewer": "evidence_and_causality",
  "severity": "high",
  "rule_id": "Q-REL-02",
  "evidence_refs": ["HYP-0002", "INT-0001"],
  "message": "施策が成果を生むという因果関係を、実験なしで確定している。",
  "minimum_repair": "因果状態をhypothesizedへ戻し、検証デザインの候補を追加する。",
  "requires_human": false,
  "confidence": "high"
}
```

## 5. 4回の批判改善の使い方
4回のレビューを行う場合、各回で問題点→モデル修正→未解決事項→再評価を記録し、同じ誤りを反復しない。**本パッケージに収録した過去4回分は概念設計に関する模擬レビューであり、実験のJ3/J4結果ではない。**

## 6. False Passと人の校正
J0/J3が`reviewable_40_candidate`にした出力を抜き取り、実在の専門家が重大欠落を検査する。偽のPassを発見した場合は、規則、Reviewer、サンプルと修正履歴を保存し、再現可能な次回実験へ反映する。
