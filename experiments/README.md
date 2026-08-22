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

3製品（スマート扇風機、懐中電灯、モバイルバッテリー）の評価実行は、[evaluation_runs/2026-08-21](../evaluation_runs/2026-08-21/README.md)にあります。

### 法規・規格・認証統合SE初稿生成プロンプト

階層型SE初稿生成プロンプトを基礎に、法規・規格・契約・認証基準を通常のSE要求とは別のCompliance Layerとして扱う実験です。

おすすめの読む順番は次のとおりです。

1. [実験のREADME](compliance-integrated-se-prompt/README.md)
2. [実行用コアプロンプト](compliance-integrated-se-prompt/01_CORE_PROMPT.md)
3. [Compliance品質規則](compliance-integrated-se-prompt/04_COMPLIANCE_QUALITY_RULES.md)
4. [実験計画](compliance-integrated-se-prompt/05_EXPERIMENT_PLAN.md)

ChatGPTで回帰テストを行う場合は、[プロンプト専用回帰テスト](compliance-integrated-se-prompt/10_CHATGPT_PROMPT_ONLY_REGRESSION.md)を使い、外部ツールを呼び出さずに期待不変条件を人が判定します。

スマート扇風機、懐中電灯、モバイルバッテリーを使ったC1-remediated評価は[2026-08-22の評価実行](../evaluation_runs/2026-08-22/compliance-integrated-se-prompt/README.md)、strict C1-blindは[別枠run](../evaluation_runs/2026-08-22/compliance-integrated-se-prompt-blind-c1-strict/README.md)にあります。

### 企画・要件定義構造化SE初稿生成プロンプト

階層型SE初稿生成プロンプトを基礎に、企画、要求、画面、帳票、API、データ、検証、受入条件を一つの候補意味モデルへまとめ、企画書・要件定義書を文書ビューとして生成できるかを試す実験です。

おすすめの読む順番は次のとおりです。

1. [実験のREADME](structured-document-se-prompt/README.md)
2. [実行用コアプロンプト](structured-document-se-prompt/01_CORE_PROMPT.md)
3. [プロファイル拡張](structured-document-se-prompt/02_PLANNING_REQUIREMENTS_PROFILE.json)
4. [品質規則](structured-document-se-prompt/04_PLANNING_REQUIREMENTS_QUALITY_RULES.md)
5. [実験計画](structured-document-se-prompt/05_EXPERIMENT_PLAN.md)

代表モデルの検証は、[検証スクリプト](structured-document-se-prompt/scripts/validate_candidate.py)で実行できます。
