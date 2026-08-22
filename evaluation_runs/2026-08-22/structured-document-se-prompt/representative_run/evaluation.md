# 実験3 代表モデル投影評価

## 1. 生成できた文書種別

同じ候補意味正本から、次の文書種別を生成できた。

- 企画書: `17_planning_document.md`
- 要件定義書: `18_requirements_document.md`
- 要求カタログ: `19_requirements_catalog.csv`
- 文書ビュー・正本参照表: `20_document_view_traceability.csv`
- データモデル図のテキスト投影: `21_data_model.mermaid.md`
- 受入条件のGherkin投影: `22_acceptance_criteria.feature`

企画書は `VIEW-0001`、要件定義書は `VIEW-0002` の章順と参照IDを基礎にした。帳票 `RPT-0001` は `reports` から要件定義書へ投影したが、`VIEW-0002.element_refs` には明示されていない。この差分はトレーサビリティ表に記録し、ビュー定義を勝手に変更していない。

## 2. 正本参照の確認

- 物理入力 `experiments/structured-document-se-prompt/examples/representative_model.json` を読み込んだ。
- 入力の `meta.source_of_truth_status` は `candidate_semantic_source_of_truth` のまま表示した。
- 入力の `document_views[*].source_of_truth_ref` は `10_se_model.json` のまま表示した。
- 企画書と要件定義書は、IDを参照して同じ要素を投影した。
- 要求カタログの `REQ-0001` から `SCR-0001`、`API-0001`、`DATA-0001`、`VER-0001`、`ACC-0001` を参照できる。
- MermaidとGherkinには、正本ではなく投影であることを明記した。

## 3. 未指定値保持の確認

次の未指定値・状態を補完せず保持した。

- `KPI-0001.target_or_range`: `null`
- `planning.cost_estimate.low/base/high`: `null`
- `planning.cost_estimate.value_state`: `tbd`
- `planning.schedule.value_state`: `tbd`
- `planning.schedule.milestones`: `[]`
- `planning.governance.sponsor_ref`: `null`
- `REQ-0001.condition`, `performance_or_limit`, `unit`, `tolerance`: `null`
- `API-0001.spec_version`, `spec_ref`: `null`
- `API-0001.operation_refs`: `[]`
- `DATA-0001.relationship_candidates`: `[]`
- `operations_maintenance` の要求参照とサービスレベル候補: `[]`
- `security` の要求、脅威、管理策、検証参照: `[]`

## 4. 限界

- 代表モデルは候補意味正本であり、企画・要求・契約・設計の承認済み正本ではない。
- `RPT-0001` は帳票候補だが、要件参照は `[]` である。
- APIはOpenAPIスタイルの契約候補にとどまり、仕様参照、操作、パス、型は未指定である。
- データモデルはエンティティと属性候補のみで、関係候補は空である。
- 運用・保守・移行・教育、サービスレベル、セキュリティ要求は正本内の参照配列が空である。
- Gherkinは受入条件を表現しただけで、シナリオ実行や合格判定を行っていない。
- Mermaidは図の表示に変換しただけで、図を正本化していない。
- 企画書と要件定義書のWord/PDF/HTMLレンダリング品質は確認していない。

## 5. 次の確認事項

- 企画レビューで `KPI-0001` の現状値・目標値・測定条件を確認する。
- `STK-0002` の業務分担と適用性を確認する。
- `ASM-0001` の認証方式、利用者区分、認証サービス利用可否を業務・セキュリティ担当者が確認する。
- `RPT-0001` を `VIEW-0002` に含めるか、帳票と要求の関係を確認する。
- `API-0001` の外部OpenAPI仕様、操作、パス、型、契約状態を確認する。
- `DATA-0001` の関係候補、属性候補、データ保持条件を確認する。
- `operations_maintenance` と `security` の要求・検証を追加する必要があるか確認する。
- `VER-0001` を実施し、`ACC-0001` を受入判定する。
- Mermaid描画、Gherkin実行、Word/PDF/HTMLレンダリングを別途確認する。
