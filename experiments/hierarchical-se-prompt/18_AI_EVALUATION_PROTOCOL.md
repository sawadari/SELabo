# 独立AI評価プロトコル

## 目的

生成AI自身の自己点検だけでは、作った内容を甘く評価する可能性があります。この文書は、生成（Generator）と評価（Reviewer）を分け、40点Gateを再現しやすくするための実験手順です。

通常の利用ではコアプロンプト内のSelf Reviewを使えます。ただし、それを独立した品質保証とは呼びません。

## 評価の段階

| Tier | 方法 | 使い道 |
|---|---|---|
| J0 | Generatorと同じ応答内のSelf Review | 生成中の最低限の修復 |
| J1 | 同じモデルを別の会話でReviewerとして実行 | 一般利用の追加確認 |
| J2 | 別モデルのReviewerを実行 | モデル固有の偏りを減らす |
| J3 | 複数の独立ReviewerとMeta-Judge | GitHub実験とRelease判定 |
| J4 | J3に少量の人による校正を加える | Reviewer自体の妥当性確認 |

SELaboの標準は、通常利用ではJ0、研究ではJ1～J3です。J4では全成果物を人が採点せず、代表サンプルと重大Findingを確認します。

## Reviewerの分担

Reviewerは同じ成果物を見ても、担当する問いを分けます。

1. **SE Coherence Reviewer**：StakeholderからV&Vまでの意味のつながり
2. **Requirements Reviewer**：1要求1義務、必要性、検証可能性、Trace
3. **Architecture / V&V Reviewer**：論理・物理の分離、配分、検証と妥当性確認
4. **Skeptical Reviewer**：矛盾、根拠のない数値、安全・法令・契約の過大主張
5. **Japanese Writing Reviewer**：名称、主語、条件、単位、曖昧語

Reviewer同士を先に議論させません。各Reviewerが独立してFindingを作り、最後にMeta-Judgeが重複、重大度、Gate状態を統合します。議論を標準手順にすると、最初の意見や長い説明に引っ張られる可能性があるためです。

## Findingの形式

感想ではなく、どの規則と証拠に基づく問題かを記録します。

```json
{
  "finding_id": "JDG-FND-0001",
  "reviewer": "requirements",
  "severity": "high",
  "type": "trace_gap",
  "rule_ids": ["Q-REQ-10"],
  "evidence_ids": ["REQ-0032", "NEED-0008"],
  "finding": "主要要求の上位Needとの関係が説明されていない。",
  "why_it_blocks_40": "要求の必要性をレビューできない。",
  "minimum_repair": "Need候補とのTraceまたは導出理由を候補として追加する。",
  "requires_human": false,
  "confidence": "high"
}
```

`requires_human`が`true`になる例は、数値の妥当性、安全分類、法規の適用、契約上の責任、リスク受入れ、承認判断です。

## Meta-Judgeの手順

1. 各ReviewerのFindingをIDで重複排除する。
2. 根拠が成果物内にあるか確認する。根拠がなければ、Finding自体を`low_confidence`として扱う。
3. `17_FORTY_POINT_GATE.md`のHard Blockerを先に確認する。
4. 主要Traceの指標と、重大Findingを合わせてGate状態を決める。
5. 修正する場合は、最小修正案だけを出す。詳細化のための追加生成は行わない。
6. 人に確認すべき事項と、AIが処理できる事項を分ける。

Meta-Judgeは、生成物の作者と同じ評価を繰り返しただけでは独立評価にならないことを明記します。モデル名、会話を分けたか、評価日時、使用したGateの版を記録してください。

## 人による校正

人は全成果物を採点しません。Pilotでは各ドメイン1～2実行、本実験では全実行の約10%を目安に確認します。次の場合は優先して確認します。

- Meta-JudgeがPassにした重大または高重大度Finding
- 根拠のない数値、法規、安全、契約に関係するFinding
- Reviewer間で判定が一致しない成果物
- `reviewable_40_candidate`になった成果物の代表サンプル

校正では、AIの見逃し（False Pass）を重点的に探します。人の確認結果は、Reviewerの版と一緒に保存します。

## 使わない評価方法

- Generatorに「自分の出力は何点か」とだけ尋ねる
- 37点と43点のような細かい数値を品質の差として扱う
- Reviewer同士の議論だけで正しさを決める
- 日本語の文法検査に合格したことを、要求の工学的妥当性とみなす

このプロトコルは、AIの判断を人の承認へ置き換えるものではありません。評価の自動化は、人が確認すべき箇所を絞るために使います。
