# SE実験の一覧

このフォルダーには、SEに関する実験を置きます。実験ごとにフォルダーを分けているため、興味のある実験だけを読んだり、試したりできます。

## 各実験に書くこと

各実験のREADMEには、次の内容を書きます。

1. 何を試す実験か
2. なぜ試すのか
3. どうやって実行するか
4. 用途に合わせて何を変えるか
5. 結果をどう評価するか
6. まだ確認できていないこと

プロンプト、設定、検査ルール、参考資料は、できるだけ各実験のフォルダー内にまとめます。

実験結果を公開するときは、次の情報も一緒に残します。

- 入力した内容
- 使用したAIモデル
- プロンプトと設定の版
- 実行した日時
- 人が修正した内容

## 現在の実験

### 階層型SE初稿生成プロンプト

対象システムの情報が少ない段階で、SEの議論を始めるための初稿をAIに作らせる実験です。

おすすめの読む順番は次のとおりです。

1. [実験のREADME](hierarchical-se-prompt/README.md)
2. [用途別ガイド](hierarchical-se-prompt/05_USE_CASE_GUIDE.md)
3. [実行用コアプロンプト](hierarchical-se-prompt/01_CORE_PROMPT.md)

生成後の評価方法を調べる場合は、次の順に読みます。

1. [40点GateとStop Rule](hierarchical-se-prompt/17_FORTY_POINT_GATE.md)
2. [独立AI評価プロトコル](hierarchical-se-prompt/18_AI_EVALUATION_PROTOCOL.md)
3. [実験計画](hierarchical-se-prompt/19_EXPERIMENT_PLAN.md)
4. [情報源の境界と人の権限](hierarchical-se-prompt/20_SOURCE_TRUST_AND_HUMAN_AUTHORITY.md)
