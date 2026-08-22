# 企画・要件定義構造化SE初稿生成プロンプト

## 何を試す実験か

この実験は、[階層型SE初稿生成プロンプト](../hierarchical-se-prompt/README.md)を基礎に、企画書と要件定義書を別々に作るのではなく、企画・要求・画面・API・データ・検証・受入条件を機械可読な意味モデルへまとめ、そのモデルから文書ビューを生成できるかを確かめます。

実験1のL0～L7、由来、主張状態、決定状態、ベースライン状態、確信度、トレーサビリティは維持します。追加するのは、情報システム向けの意味要素と、企画書・要件定義書を投影するための`document_views`です。

## 中核となる考え方

```text
入力・調査資料
  → 10_se_model.json（候補意味正本）
  → document_views（企画書・要件定義書の表示順と参照ID）
  → Markdown / CSV / HTML / Word / PDF 等
```

文書の章やテンプレートに要求の意味を閉じ込めません。要求ID、画面ID、API ID、データモデルID、検証ID、受入条件IDを共有し、同じ意味要素を複数のビューから参照します。実験3で作るものは候補初稿であり、承認済みの企画、正式要求、API契約、設計承認を意味しません。

## 実験1からの追加

| 名前空間 | 役割 |
|---|---|
| `planning` | 背景、目的、KPI、対象ユーザー、代替案、費用、計画、体制 |
| `screens` | 画面の目的、利用者、要求、入力候補、遷移候補 |
| `reports` | 帳票・レポートの利用者、目的、データ、要求 |
| `api_contracts` | OpenAPI等の外部契約への参照、操作、関連要求 |
| `data_models` | エンティティ、属性、関係、関連要求 |
| `operations_maintenance` | 運用、保守、移行、教育の要求参照 |
| `security` | 脅威、管理策候補、セキュリティ要求、検証参照 |
| `acceptance_criteria` | 受入条件を検証ケースとは別の意味要素として保持 |
| `document_views` | 企画書・要件定義書の章構成と表示対象ID |

`api_contracts`の`spec_ref`はOpenAPIやAsyncAPIの外部ファイル参照です。実験3の意味モデルがOpenAPI仕様そのものを置き換えることはありません。未指定値は`null`や`value_state: tbd`のまま保持し、AIが数値や承認状態を補完しません。

## 使い方

実験1の次のファイルと、本フォルダーの拡張ファイルを同時にAIへ渡します。

- `../hierarchical-se-prompt/01_CORE_PROMPT.md`
- `../hierarchical-se-prompt/02_DEFAULT_PROFILE.json`
- `../hierarchical-se-prompt/03_OUTPUT_CONTRACT.json`
- `../hierarchical-se-prompt/04_QUALITY_RULES.md`
- `../hierarchical-se-prompt/10_JAPANESE_TECHNICAL_WRITING_STANDARD.md`
- `../hierarchical-se-prompt/11_JAPANESE_WRITING_PROFILE.json`
- `../hierarchical-se-prompt/schemas/se_model.schema.json`
- `01_CORE_PROMPT.md`
- `02_PLANNING_REQUIREMENTS_PROFILE.json`
- `03_PLANNING_REQUIREMENTS_OUTPUT_EXTENSION.json`
- `04_PLANNING_REQUIREMENTS_QUALITY_RULES.md`
- `schemas/planning_requirements_se_model.schema.json`

入力には、対象事業・業務、利用者、対象範囲、既存業務、既存システム、必要な画面・帳票・API・データ、受入観点を分かる範囲で含めます。分からない項目は未指定のまま実行できます。

代表モデルのSchema検証は次で実行します。

```powershell
python scripts/validate_candidate.py examples/representative_model.json
```

## 成功条件

1. 実験1のSE要素と実験3の企画・情報システム要素が同じ候補意味正本で追跡できる。
2. 企画目的 → KPI → ニーズ → 要求 → 画面/API/データ → 検証 → 受入条件をIDでたどれる。
3. 企画書と要件定義書が独立した事実のコピーではなく、`document_views`から投影できる。
4. 未指定値、AI推測、仮定、提案中の決定が確定値や承認済み要求へ昇格しない。
5. Schema検証、参照整合性、文書ビューの正本参照を別々に確認できる。

## まだ確認できていないこと

この版はスキーマと生成プロンプトの実験用パッケージです。実際のAIモデル間の品質差、Word/PDFのレイアウト、OpenAPI/AsyncAPIのlint、社内テンプレートとの一致、業界別の企画書・要件定義書の網羅性は未検証です。実験1と同じく、正式な要求ベースライン、法令適合、セキュリティ承認、受入完了をAIだけで判断しません。
