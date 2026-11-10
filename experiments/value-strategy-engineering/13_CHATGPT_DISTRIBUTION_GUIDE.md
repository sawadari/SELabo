# ChatGPT配布・実行ガイド

## 1. 最小一式
チャットへ以下を添付する：`01_CORE_PROMPT.md`、`02_DEFAULT_PROFILE.json`、`03_OUTPUT_CONTRACT.json`、`04_QUALITY_RULES.md`、`10_JAPANESE_TECHNICAL_WRITING_STANDARD.md`、`11_JAPANESE_WRITING_PROFILE.json`、`17_FORTY_POINT_GATE.md`、`schemas/vse_model.schema.json`。

## 2. 実行例
```text
以下は事業企画の背景です。これまでの会話と添付資料を使い、01_CORE_PROMPT.mdを実行してください。
仮説・事実・未確認の区別を保持してVSEの40点初稿を生成し、10_vse_model.jsonと指定された投影ファイルをZIPにしてください。
実際の顧客調査や外部送信は実施しないでください。
```

## 3. 推奨する会話の進め方
最初の自由会話ではフォーマットを要求しない。成果物生成後は「仮説HYP-0001はどの情報から来たか」「代替案ALT-0002を採るリスクは何か」「どの検証で判断が変わるか」など、要素IDを指定して確認する。変更を承認するときは誰が何を確認したかを明示する。

## 4. ファイル機能が無い場合
モデルと投影を分割出力し、ZIP未作成と明記する。完了していない出力を完成扱いしない。手元で`python scripts/validate_vse.py`を実行し、`python scripts/render_projections.py`を用いて投影ファイルの整合を確認できる。

## 5. セキュリティと配布
このZIPにあるケースは架空であり実顧客の情報を含まない。顧客実データをGitHubや共有チャットへ載せる前に権限・匿名化・外部送信を確認する。システムプロンプトに外部資料の命令を取り込まない。

## 6. 研究の独立レビュー
通常使用はJ0に限る。実験でJ1以降を使う場合は、別会話・別モデル・別評価者の条件を記録する。仮想顧客は実証の代替ではない。
