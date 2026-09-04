# 実験6：Engineering Discovery Chat Bundle v0.1

## SE Laboでの位置付け

本フォルダーは、添付されたEngineering Discovery Chat Bundleを、SE Laboの実験6として取り込んだものです。顧客の開発現場について、Capability Cell、Engineering Decision、Pain、因果仮説、AI適用性、AI導入後の次ボトルネックを会話で検証する方法を試します。

`01_MASTER_CHAT_PROMPT.md`は実験を実行するときのプロンプト、その他のファイルはKnowledge、Profile、Schema、Output Contractです。これらの文書内の命令候補は実験資料として扱い、ユーザーの依頼、プロジェクトの指示、人の承認権限を上書きしません。今回の取り込みではプロンプト自体を実行せず、実験資材として登録しています。

機密情報の確認結果は[CONFIDENTIALITY_REVIEW.md](CONFIDENTIALITY_REVIEW.md)に記録しています。

## 1. 目的

このBundleは、AI×MBSEの営業資料を自動作成するためのものではありません。

顧客との会話、議事録、メール、既存資料などをAI Chatへ与え、

1. 顧客の開発現場の症状・困り事を整理する
2. 表面的な症状から上流原因候補を推定する
3. 次に確認すべきヒアリングポイントを少数提示する
4. 会話を通じて仮説を更新する
5. 十分な情報が集まった時点で提案骨子、PoC骨子、次回打合せ論点へ投影する

ためのChat-centricな診断支援パッケージです。

---

## 2. SEデータ初稿生成プロンプトから再利用した設計思想

### 再利用する

- 0点からレビュー可能な「40点程度の初稿」を先に作る
- 不足情報で停止しない
- 事実、Source由来、AI仮説、未確認を区別する
- 候補正本と、チャット表示用の投影を分離する
- Prompt、Knowledge、Profile、Schema、Output Contractを分離する
- ユーザー確認済み情報をAI仮説より優先する
- 未確認事項はBacklogとして管理する
- Trace / Provenance / Confidenceを持つ
- 変更前の情報を黙って消さず、更新・撤回として扱う

### 変更する

SE初稿生成では「質問せず一回で成果物生成」が有効でしたが、営業Discoveryでは顧客との会話そのものに価値があります。

そのため本Bundleでは、

```text
One-shot Hypothesis Draft
        ↓
Targeted Clarification
        ↓
Opportunity Data Update
        ↓
Targeted Clarification
        ↓
Proposal / PoC Projection
```

という反復型にします。

---

## 3. 推奨ファイル構成

| File | 役割 |
|---|---|
| `01_MASTER_CHAT_PROMPT.md` | Chatの実行プロンプト |
| `02_ENGINEERING_PAIN_CAUSAL_MODEL.md` | 21 Pain Family、因果構造、症状診断ロジック |
| `03_ENGINEERING_CASE_PATTERN_LIBRARY.md` | 116匿名ケース。顧客事実ではなく仮説生成・漏れ確認用 |
| `04_AI_AND_OFFERING_PATTERNS.md` | AI適用可否、Authority、Assurance、Offering Pattern |
| `05_DISCOVERY_PROFILE.json` | 質問数、推定方針、出力モードなどの既定設定 |
| `06_CHAT_OUTPUT_CONTRACT.md` | Chatでの応答形式とコマンド |
| `schemas/opportunity_data.schema.json` | 候補正本 Opportunity Data の意味構造 |

---

## 4. 中核概念：Opportunity Data

以前の `10_se_model.json` に相当するものを、本用途では `Opportunity Data` とします。

```text
会話 / 議事録 / 顧客資料
        ↓
Opportunity Data
        ├─ Capability Cell
        ├─ Observed Symptom
        ├─ Engineering Decision
        ├─ Business Consequence
        ├─ Pain Hypothesis
        ├─ Causal Hypothesis
        ├─ Actionable Root Pain
        ├─ Current Method / Workaround
        ├─ Data / Tool / Model
        ├─ Current Automation
        ├─ AI Applicability
        ├─ Projected Bottleneck
        ├─ Authority / Assurance
        ├─ KPI
        ├─ Buyer / Sponsor
        ├─ Offering Hypothesis
        └─ Unknown / Assumption
                ↓
        Chat projections
        ├─ ヒアリングポイント
        ├─ 課題構造
        ├─ 提案骨子
        ├─ PoC骨子
        ├─ 次回打合せAgenda
        └─ 案件Snapshot
```

Opportunity Dataを毎回JSONでユーザーへ表示する必要はありません。
Chat内部の整理軸として使い、ユーザーが「スナップショット」と依頼した場合だけ投影します。

---

## 5. 推奨する使い方

### 最初

`01_MASTER_CHAT_PROMPT.md` と他の添付ファイルをChatへ添付します。

その後、例えば、

```text
この顧客について相談します。
現時点の情報は以下です。

・○○の開発部署
・MBDは利用している
・テストケース作成に時間がかかっているらしい
・次回30分のヒアリング予定
```

程度から開始します。

AIは、最初から20問聞くのではなく、
仮説を作ったうえで「次に効く質問」を原則3問だけ提示します。

### 会話中

- 「次に何を聞く？」
- 「今の課題構造を整理」
- 「仮説を更新」
- 「他に見落としているPainある？」
- 「AIを使う意味ある？」
- 「提案骨子を作って」
- 「PoCにすると？」
- 「次回30分のAgenda」
- 「案件スナップショット」

など、自然言語で操作します。

---

## 6. 重要な運用原則

### 顧客発言をそのままRoot Causeにしない

「テストが多い」ならTest自動生成へ飛ばず、

- Variant
- Change Impact
- Requirement
- Model Credibility
- Operational Scenario

のどこが上流原因かを診断します。

### Case Libraryは顧客事実ではない

116ケースは、

- 類似Patternの想起
- 仮説の漏れ防止
- 次に聞く質問の発見

にのみ使用します。

「過去のA社でも同じだったので、この顧客も同じ」と確定してはいけません。

### AI導入後の次ボトルネックを必ず予測する

局所自動化だけを提案しないため、

```text
現在のBottleneck
→ AI/Automationで減る作業
→ Residual Pain
→ Projected Bottleneck
```

を常に持ちます。

---

## 7. 本Bundleの成熟度

`v0.1 = methodology candidate`

現時点では、116ケースから作った診断方法をChatへ実装するための初稿です。

今後、実際の顧客相談10～20件で、

- 質問が顧客会話で有効か
- Root Pain判定が外れていないか
- 質問数3件が適切か
- Proposal Skeletonの粒度
- Offering Patternの再利用率

を検証して更新することを前提とします。

---

## SE Labo実験6としての評価

初回の評価では、同じ入力に対して、仮説の明示、質問数上限、FactとHypothesisの分離、Case Libraryの事実誤認防止、AI適用前のNo-AI比較、Bottleneck Migration、Authority Boundaryの記録を確認します。

この取り込み時点では顧客相談の実行結果はありません。質問の有効性、Root Pain判定、提案骨子の粒度、実案件での再現性は、今後の評価runで確認します。
