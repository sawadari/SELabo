# 検証レポート

## 目的

実験3の意味正本、文書投影モデル、参照整合性、要求本文不変性の境界を確認する。これは生成品質、事業妥当性、要求承認、契約承認を証明する検査ではない。

## 実施した検査

| 検査 | 結果 | 方法 |
|---|---|---|
| JSON構文 | pass | 収録JSONをPythonで読み込んだ |
| 実験1Schemaとの合成 | pass | `python scripts/validate_candidate.py examples/representative_model.json` |
| 追加名前空間の必須項目 | pass | 合成Schema |
| ID一意性 | pass | 検証スクリプト。22件 |
| document_views参照 | pass | 検証スクリプト |
| 文書投影Schema自体 | pass | `Draft202012Validator.check_schema` |
| 文書投影モデル生成 | pass | `python document_generation/scripts/project_document_model.py ...` |
| 正本ハッシュ | pass | `source_binding.content_hash`と入力ファイルのSHA-256を比較 |
| DOCREQ要求レジストリ | pass | 正本要求1件をDOCREQ 1件へ一意に投影 |
| 要求本文不変性 | pass | `rendered_statement.value == source.requirements[].statement` |
| 関係トレーサビリティ | pass | `se_model.relations`の関係ID・端点を確認 |
| データモデル・データ品質 | pass_with_provisional_assumption | エンティティを投影し、正本にない品質基準は`not_determined`と記録 |
| OpenAPI/AsyncAPI外部契約lint | not_performed | `spec_ref`が未提供 |
| 日本語技術文章検証 | not_performed | 専用レンダリング後検査は未実施 |
| Markdown/HTML/DOCX/PDFレンダリング | not_performed | レンダラーとレイアウト検査は未実施 |
| 人によるレビュー・承認 | not_performed | 候補成果物のため未実施 |

## 実行コマンド

```powershell
python scripts/validate_candidate.py examples/representative_model.json
python document_generation/scripts/project_document_model.py examples/representative_model.json document_generation/20_document_model.json
python document_generation/scripts/validate_document_projection.py examples/representative_model.json document_generation/20_document_model.json
```

## 判定

代表モデルについて、意味正本と文書投影モデルのSchema、正本ハッシュ、DOCREQ参照、要求本文の不変性、関係トレーサビリティは確認できた。出力は`candidate`であり、企画・要求・API契約・データ品質基準・受入の承認や実施を意味しない。
