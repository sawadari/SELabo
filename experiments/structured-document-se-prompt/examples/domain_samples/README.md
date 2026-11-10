# ドメイン別サンプル文書

同じ構造化SEプロンプトと文書投影パイプラインを、ドメインだけ変えて実行したサンプルです。各サンプルは、`10_se_model.json`を意味正本とし、`20_document_model.json`から企画書・要件定義書を生成しています。

## サンプル一覧

| ドメイン | 企画書 | 要件定義書 | 主な観点 |
|---|---|---|---|
| 自動車開発 | [企画書](automotive/21_planning_document.md) | [要件定義書](automotive/22_requirements_definition.md) | 商品企画、車両システム要求、充電状態表示、評価・受入 |
| 製造業 | [企画書](manufacturing/21_planning_document.md) | [要件定義書](manufacturing/22_requirements_definition.md) | 設備異常、保全依頼、復旧状況、設備台帳参照 |
| 物流 | [企画書](logistics/21_planning_document.md) | [要件定義書](logistics/22_requirements_definition.md) | 入出荷作業、作業遅延、在庫情報参照 |

各ディレクトリには、次の成果物があります。

- `10_se_model.json`: ドメイン別の候補意味正本
- `20_document_model.json`: 非正本の文書投影モデル
- `21_planning_document.md`: 企画書サンプル
- `22_requirements_definition.md`: 要件定義書サンプル
- `23_document_traceability.csv`: 文書と正本のトレーサビリティ
- `24_document_quality_report.md`: 品質状態と未実施事項
- `25_document_generation_manifest.json`: 生成物マニフェスト

サンプルは候補初稿です。API詳細、スケジュール、予算、データ品質基準、規制適用性、受入実施結果は推測せず、未確定または未実施として表示しています。
