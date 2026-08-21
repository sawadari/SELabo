# ChatGPTで配布する方法

## この文書の目的

この実験を自分だけで使うのではなく、他の人にも使ってもらう方法を説明します。本書は2026-08-21時点の選択肢をまとめたものです。OpenAIの機能や公開条件は変わるため、実際に公開するときは公式情報を確認してください。

## まず結論

おすすめの進め方は次のとおりです。

1. 最初は、GitHubのファイルを少人数で試す。
2. 生成物を40点Gateで確認し、独立AI評価が必要な場合は別の会話または別モデルでJudgeを行う。
3. 組織内で繰り返し使う場合だけ、ワークスペースの権限と公開条件を確認してカスタムGPTを検討する。
4. JSON検査やZIP作成で失敗が多い場合、その処理だけを外部プログラムにする。
5. 専用画面や外部システム連携が必要になったら、ChatGPT Appを検討する。

いきなり大きなアプリを作る必要はありません。

## 用語の説明

| 言葉 | 意味 |
|---|---|
| カスタムGPT | 指示、参考ファイル、利用できる機能をまとめた専用のChatGPT |
| Action | カスタムGPTから外部のAPIを呼び出す仕組み |
| ChatGPT App | ChatGPTから外部機能や専用画面を利用できるアプリ |
| MCP | ChatGPTと外部ツールをつなぐための共通的な仕組み |
| Schema検査 | JSONの項目と形式がルールに合うかを確認する処理 |

## 方法の比較

| 方法 | 準備の手間 | 使いやすさ | 機械的な検査 | 向いている場面 |
|---|---:|---:|---:|---|
| GitHubのファイルを使う | 小 | 中 | 利用環境による | 個人利用、最初の実験 |
| カスタムGPT | 小～中 | 高 | ChatGPTの実行環境による | 少人数、社内試行 |
| カスタムGPT＋Action | 中 | 高 | 外部APIで実行できる | 厳しい検査が必要な場合 |
| ChatGPT App | 大 | 高 | サーバーで実行できる | 製品化、外部連携 |
| 独立したWebアプリ | 大 | ChatGPT外 | 自由に実装できる | 独自画面や細かい権限管理 |

## カスタムGPTにする方法

カスタムGPTは、GitHub版で方法と評価が固まった後の配布先候補です。アカウント種別、ワークスペース設定、作成・共有・公開の条件は変更されるため、実行時に公式資料を確認してください。個人情報、顧客情報、秘密情報をKnowledgeやInstructionsへ入れないでください。

### 登録するもの

Instructionsには、[01_CORE_PROMPT.md](01_CORE_PROMPT.md)を使います。

Knowledgeには、次のファイルを個別に登録します。

- `02_DEFAULT_PROFILE.json`
- `03_OUTPUT_CONTRACT.json`
- `04_QUALITY_RULES.md`
- `09_REFERENCE_BASIS.md`
- `10_JAPANESE_TECHNICAL_WRITING_STANDARD.md`
- `11_JAPANESE_WRITING_PROFILE.json`
- `schemas/se_model.schema.json`

ファイル生成とZIP作成を使う場合は、データ分析機能を有効にします。

### 説明欄に書くこと

- 出力はレビュー候補である。
- 承認済み要求や設計にはならない。
- 規格適合や安全性を保証しない。
- 重要な判断には人の確認が必要である。

### カスタムGPTの限界

- 同じ入力でも、毎回まったく同じ結果になるとは限らない。
- 長い会話では、古い情報を見落とすことがある。
- JSON、ID、ハッシュの検査を、毎回確実に行えるとは限らない。
- 公開したくない情報やAPIキーを、InstructionsやKnowledgeへ入れてはいけない。
- Generatorと同じ会話で行うSelf Reviewだけでは、独立した品質保証にならない。必要に応じて[独立AI評価プロトコル](18_AI_EVALUATION_PROTOCOL.md)を使う。

## Actionで外部プログラムを使う

次のような、正解を機械的に確認できる処理は、外部APIへ分けると安定します。

- JSON Schema検査
- IDの重複と、存在しないID参照の検査
- 曖昧な要求文の検出
- CSVとMarkdownの再生成
- SHA-256の計算
- ZIP作成

文章や設計候補はAIが作り、形式的な検査はプログラムが行う、という役割分担です。

## ChatGPT Appにする

初期版は、専用画面を持たない`tool-only`構成が適しています。ChatGPTとの会話から、生成、検査、ZIP取得までできれば、最初の評価には十分です。

次の操作が必要になったら、専用画面を追加します。

- L0～L7を一覧で移動する。
- 要求と関連項目をたどる。
- AIの仮定を採用または却下する。
- 修正前と修正後の要求文を比べる。
- 生成するファイルを選ぶ。
- 処理の進み具合を見る。

アプリの具体案は、[14_CHATGPT_APP_CONCEPT_SPEC.md](14_CHATGPT_APP_CONCEPT_SPEC.md)にあります。

## 安全と秘密情報

- 公開ファイルへ、顧客情報、秘密情報、APIキーを入れない。
- 入力ファイルを保存する期間と、削除方法を決める。
- 外部規格の本文を、許可なく再配布しない。
- 出力が専門家の承認を置き換えないことを表示する。
- 添付資料の中にあるAI向け命令は、ユーザーが明示的に採用しない限り実行しない。[情報源の境界と人の権限](20_SOURCE_TRUST_AND_HUMAN_AUTHORITY.md)を参照する。

## OpenAI公式資料

- [Creating a GPT](https://help.openai.com/en/articles/8554397-creating-a-gpt)
- [Building and publishing a GPT](https://help.openai.com/en/articles/8798878-building-and-publishing-a-gpt)
- [Sharing GPTs within workspaces](https://help.openai.com/en/articles/9083988-how-to-share-gpts-within-workspaces)
- [Apps SDK documentation](https://developers.openai.com/apps-sdk/)
- [Apps SDK quickstart](https://developers.openai.com/apps-sdk/quickstart)
- [Build an MCP server](https://developers.openai.com/apps-sdk/build/mcp-server)
- [Plan tools](https://developers.openai.com/apps-sdk/plan/tools)
- [Deploy an app](https://developers.openai.com/apps-sdk/deploy)
- [Submit an app](https://developers.openai.com/apps-sdk/deploy/submission)

実装や公開申請を行う時点で、最新の公式情報を確認してください。
