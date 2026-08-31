# 実験5：SEデータからSysMLモデリング前PlantUMLを生成する

## 1. 何を試す実験か

実験1（`hierarchical-se-prompt`）で作成した候補SEデータを入力にして、SysML v1.xへ正式にモデリングする前のレビュー用PlantUMLビューを生成できるかを試す。

この実験の意味上の正本は`10_se_model.json`である。PlantUML、図一覧、SysML 1.xモデル仕様は正本からの投影であり、独立した設計正本や正式SysMLモデルではない。

想定する流れは次のとおりである。

```text
会話・資料
  ↓
実験1：候補SEデータ
  ↓
10_se_model.json
  ↓
実験5：投影判定・PlantUML生成
  ↓
人によるレビュー
  ↓
Cameo / Enterprise Architect等で正式SysMLモデル化
```

## 2. なぜ試すのか

PlantUMLはレビューしやすいテキスト表現だが、図を成立させるためにAIが新しいRequirement、Block、Interface、State、通信や設計決定を創作しやすい。そこで、次の仮説を検証する。

> `10_se_model.json`のID、出自、確定度を保ったまま、生成可能な図だけを選び、不足情報を`VIEW_DERIVED`または`UNRESOLVED`として表示できる。

## 3. 使い方

実行時には、少なくとも次を同時に渡す。

- `01_CORE_PROMPT.md`
- `02_PLANTUML_PROFILE.json`
- `03_OUTPUT_CONTRACT.json`
- `04_QUALITY_RULES.md`
- 実験1の`schemas/se_model.schema.json`
- 入力の`10_se_model.json`

利用可能な場合は、実験1の`02_DEFAULT_PROFILE.json`、`04_QUALITY_RULES.md`、日本語文章規則、既存のSysML投影仕様も渡す。競合時は、ユーザー確認済み情報、`10_se_model.json`、この実験の品質規則、表示上の推論の順に扱う。

コアプロンプトは、生成物をチャット本文へ長く貼り付けず、ファイルとして作成することを要求する。ZIPを作成できない環境では、未作成と明記してコードブロックへフォールバックする。

## 4. 出力

必要な図だけを`.puml`として生成する。`99_generation_index.puml`には、生成した図、生成しなかった図、未解決情報を記録する。各図の冒頭コメントには、図の問い、`semantic_mode`、正本、source ID、限界を残す。

`strict_projection`は正本要素・関係だけで成立する図、`projection_with_view_derived_elements`は正本の文章を表示用に分解した図、`insufficient_data`は図ファイルを作らずIndexに理由を書く状態である。

## 5. 実験結果

最初の試行は、実験1系のスマート扇風機候補モデルを使った。

- 入力：`evaluation_runs/2026-08-22/compliance-integrated-se-prompt/smart-fan/candidate_model.json`
- 試行結果：[evaluation_runs/2026-08-31/sysml-pre-model-plantuml/smart-fan](../../evaluation_runs/2026-08-31/sysml-pre-model-plantuml/smart-fan/)
- 検証スクリプト：[scripts/validate_projection.py](scripts/validate_projection.py)

この入力ではRequirement、Behavior、Scenario、Verification、System Structureは存在する一方、Interface、Constraint、構造化されたState Transition、Use Caseが存在しない。そのため、Requirement、Activity、Sequence、BDD、Verification Traceを生成し、IBD、State Machine、Parametric、Use Case、Package、完全なContext Viewは生成しない。

## 6. 評価すること

- 正本IDが図とIndexへ保持されているか
- 図に登場するCanonical要素が入力に存在するか
- `VIEW_DERIVED`と`UNRESOLVED`が明示されているか
- Requirement、Behavior、Structure、Verificationの投影が相互に矛盾しないか
- Scenarioの文章から作った表示上の順序を、設計上の関係として誤って扱っていないか
- Interface、State、Constraintがない場合に、見栄えのための創作をしていないか
- PlantUML構文検証の実施／未実施を正しく記録しているか

## 7. まだ確認できていないこと

人によるSysML意味レビュー、Cameo / Enterprise Architectへの正式モデル化、SysMLツール間の互換性、複数モデル・複数ドメインでの再現性、専門家による意味妥当性は別試験である。この試行のPASSは、入力Schema、PlantUML構文、PNG生成、投影ルールの確認を意味し、設計承認やSysML適合を意味しない。
