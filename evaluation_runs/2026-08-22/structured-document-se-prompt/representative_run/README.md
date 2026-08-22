# 実験3 代表モデル投影実行

## 実行条件

- 実行日: `2026-08-22`
- 実験: `structured-document-se-prompt`
- 実行単位: `representative_run`
- 目的: 実験3の候補意味正本から、企画書・要件定義書と関連する文書ビューを投影できるかを確認する。
- 書き込み範囲: 本ディレクトリだけ。実験3本体および入力正本は変更していない。
- 生成物の位置付け: すべて候補初稿または投影であり、承認済み文書、正式要求、API契約、設計、試験実施結果を意味しない。

## 入力正本

- 物理入力ファイル: `experiments/structured-document-se-prompt/examples/representative_model.json`
- 正本参照名: モデル内の `document_views[*].source_of_truth_ref` に記載された `10_se_model.json` を変更せず保持した。
- `meta.artifact_type`: `hierarchical_se_model_candidate`
- `meta.source_of_truth_status`: `candidate_semantic_source_of_truth`
- `meta.documents_are_projections`: `true`
- 対象システム: `保全依頼管理システム`
- 文書言語: `ja-JP`

## 生成した文書一覧

| ファイル | 種別 | 投影元 |
|---|---|---|
| `17_planning_document.md` | 企画書 | `planning`, `objectives`, `measures`, `scope`, `document_views` |
| `18_requirements_document.md` | 要件定義書 | `requirements`, `screens`, `reports`, `api_contracts`, `data_models`, `operations_maintenance`, `security`, `verification_cases`, `acceptance_criteria`, `document_views` |
| `19_requirements_catalog.csv` | 要求カタログ | `requirements` と要求の参照ID |
| `20_document_view_traceability.csv` | 文書ビュー・正本参照表 | `document_views` と参照要素 |
| `21_data_model.mermaid.md` | Mermaid ER図テキスト | `data_models` |
| `22_acceptance_criteria.feature` | Gherkin受入条件投影 | `acceptance_criteria`, `verification_cases` |
| `evaluation.md` | 評価記録 | 生成結果と検証結果 |

## 未実施事項

- OpenAPI仕様lint: `API-0001.spec_ref` が `null` のため未実施。
- Word/PDF/HTMLのレンダリング確認: 未実施。
- Mermaidレンダラーによる描画確認: 未実施。
- Gherkinランナーによるシナリオ実行: 未実施。
- 実システム、実データ、利用者、セキュリティ担当者による確認: 未実施。
- `VER-0001` の検証実施および `ACC-0001` の受入判定: 未実施。
