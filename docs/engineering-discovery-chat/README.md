# 実験6 Webプロトタイプ（GitHub Pages）

実験6の「入力 → 仮説 → 最大3件の確認質問 → 更新 → 提案・PoC骨子への投影」を、ブラウザだけで操作できる静的ページです。

- 公開先（Pages有効化・mainへのマージ後）：`https://sawadari.github.io/SELabo/engineering-discovery-chat/`
- ソース：`docs/engineering-discovery-chat/`
- 参照する方法論：`experiments/engineering-discovery-chat/`
- 実装状態：**methodology UI prototype**。本来のAI Chatエンジンではありません。

## 利用できること

1. 案件情報、困り事、追加の回答を自由記述で入力する。
2. 21 Pain Familyの一部キーワードによる暫定分類と、Pain Modelの上流原因候補を表示する。
3. 原則3問までの質問に回答して、仮説を更新する。
4. 課題構造、提案骨子、PoC骨子に切り替えて表示する。
5. 候補正本の `Opportunity Data` をJSONでダウンロードする。表示サマリーもコピーできる。
6. 「新規案件」でセッションを破棄する。ブラウザ内に自動保存しない。

**厳密な意味でのAI診断は未実装です。** キーワード照合だけでは、否定文、用語の意味の違い、因果、矛盾、自由文脈の解釈はできません。因果関係・Actionable Root Pain・AI適用・Authority等を確定しません。提案／PoC画面は項目の投影であって、個別案件に最適化した提案生成ではありません。

`03_ENGINEERING_CASE_PATTERN_LIBRARY.md` の116ケースは**現時点のブラウザ実装には取り込んでいません**。将来のAI連携でも顧客事実として使用しないことが必須です。

## GitHub Pagesの公開手順

1. PRをレビューして `main` にマージする。
2. GitHubの `sawadari/SELabo` → **Settings** → **Pages** を開く。
3. **Build and deployment** で **Deploy from a branch** を選ぶ。
4. **Branch** を `main`、フォルダを `/docs` に指定して保存する。
5. `https://sawadari.github.io/SELabo/engineering-discovery-chat/` にアクセスする。

すでに別のGitHub Pages公開元がある場合は設定を上書きしないでください。Pagesはリポジトリ単位で1サイトです。公開権限・組織ポリシーの最終確認は管理者が行ってください。

## データ・セキュリティ

- このページはGitHub Pages上で静的に配信されるHTML/CSS/JavaScriptです。入力した文章はブラウザ内で処理し、APIへ送信しません。
- ページは入力内容をCookie、Local Storage、IndexedDBに保存しません。リロードすると消えます。手動でJSONをダウンロードすると、そのファイルは利用者端末に残ります。
- ページのContent Security Policyはネットワーク接続（`connect-src`）を禁止します。
- **公開ページを社内専用システムと誤認しないこと**。実顧客名、未公開設計情報、議事録等は投入しないでください。匿名化した架空サンプルでの検証から始めます。
- 顧客データの保持・共有、ブラウザ拡張・端末・ダウンロードファイルの安全性は本プロトタイプでは保証していません。
- GitHub Pagesでの公開前に、リポジトリ内のライセンス未設定、事例出典の利用条件、方法論自体の公開範囲を確認してください。

## 今後の「本来のAI Chat」を実現する構成

```text
GitHub Pages（チャット・画面表示）
    │ 認証付きHTTPS
    ▼
Serverless API（Cloudflare Workers等）
    ├─ ユーザー認証、アクセス制限、Rate Limit、予算制限
    ├─ Prompt/Knowledge/Profile/Output Contractの版管理
    ├─ 21 Pain Family、116ケースから関連候補を検索
    ├─ 事実/仮説/類似例/未確認の区分と根拠を強制
    ├─ Opportunity Dataのスキーマ検証、履歴管理
    └─ LLM Provider API（秘密鍵はサーバーのみ）
    │
    ▼
候補JSON + 対話応答 → GitHub Pages画面
```

GitHub Pages単独には秘密鍵を安全に保存したり、サーバー側のLLM推論を実行する機能はありません。APIキーを静的JavaScript・GitHub repository・GitHub Pagesに置かないでください。

AI統合時の**最低条件**は、ユーザー認証（CORSのみは認証ではない）、APIトークンのサーバー側Secret保管、Rate Limit、入力サイズ制限、利用料金の上限、ログ・顧客情報の保持ポリシー、Prompt Injection耐性、Schema Validation、Human Approvalです。

また、`01_MASTER_CHAT_PROMPT.md`、`02_ENGINEERING_PAIN_CAUSAL_MODEL.md`、`03_ENGINEERING_CASE_PATTERN_LIBRARY.md`、`04_AI_AND_OFFERING_PATTERNS.md`、`05_DISCOVERY_PROFILE.json`、`06_CHAT_OUTPUT_CONTRACT.md`、`schemas/opportunity_data.schema.json` は、API側でバージョン固定・厳密に役割分離して利用します。AI出力の候補は独立検証を経るまで確定事実になりません。

## 試験

Node.js 22以上で、リポジトリのルートから実行：

```sh
node --test experiments/engineering-discovery-chat/tests/engine.test.mjs
```

試験で確認するのは分類・質問上限・回答済み質問の非再表示・出典区分・候補正本の最低限の形です。**LLMの回答品質、根本原因の正確性、顧客ヒアリングの効果は試験対象外**です。実案件に使う前に、元のREADMEの計画通り10〜20ケース以上の人手レビュー・評価が必要です。
