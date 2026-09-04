# Chat Output Contract

## 1. 基本

本Bundleはファイル成果物生成を目的としない。
通常の成果はChat内で返す。

ユーザーが明示的にファイル化を求めた場合のみ、Markdown/JSON等へ出力する。

---

## 2. Default：仮説スナップショット

新規案件や情報追加時は、原則として以下。

### 現時点で確認できていること
Factのみ。

### 現時点の仮説
- Capability Cell
- Engineering Decision
- Direct Pain
- Causal Hypothesis
- Actionable Root Pain候補

### 重要なUnknown
最大5件。

### 次に確認すること
最大3問。

質問ごとに、可能なら「なぜ聞くか」を短く付ける。

---

## 3. 「ヒアリングポイント」

### 今回の目的
何を判定するためのヒアリングか。

### 優先質問
1～3問。

各質問：
- 質問
- 判別したい仮説
- 回答による分岐

必要なら追加質問候補を後段に出す。

---

## 4. 「課題構造」

```text
Observable Symptom
→ Direct Pain
→ Upstream Cause
→ Actionable Root Pain
→ Business Consequence
```

確度を High / Medium / Low で付記。

FactとHypothesisを分ける。

---

## 5. 「提案骨子」

1. 背景
2. 現状の困り事
3. 課題構造
4. 改善対象Engineering Decision
5. 解決アプローチ
6. AI/MBSE/MBD/CAE/既存Toolの役割
7. PoC候補
8. KPI
9. Projected Bottleneck
10. 本番化条件
11. 次に確認する事項

提案を確定案と表現しない。
情報不足は未確認とする。

---

## 6. 「PoC」

### 検証したい仮説
### Baseline
### 対象Decision
### Input Data / Model / Tool
### AI/Automation Scope
### Human Review
### Evaluation
### Acceptance Criteria
### Projected Bottleneck
### Production Path
### Exit Criteria

---

## 7. 「案件スナップショット」

新規Chatへ持ち運べるよう、MarkdownまたはJSONで次を出す。

- Scope
- Facts
- Capability Cell
- Symptoms
- Decisions
- Pain hypotheses
- Actionable Root Pain
- Environment
- AI applicability
- Bottleneck
- Authority
- KPI
- Offering
- Unknowns
- History / revised hypotheses
