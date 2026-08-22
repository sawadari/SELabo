# 検証レポート

## 目的

実験3の追加Schema、代表モデル、参照整合性検査が動作することを確認する。これは生成品質、事業妥当性、要求承認、契約承認を証明する検査ではない。

## 実施する検査

| 検査 | 結果 | 方法 |
|---|---|---|
| JSON構文 | pass | 収録JSONをPythonで読み込んだ |
| 実験1Schemaとの合成 | pass | `python scripts/validate_candidate.py examples/representative_model.json` |
| 追加名前空間の必須項目 | pass | 合成Schema |
| ID一意性 | pass | 検証スクリプト。22件 |
| document_views参照 | pass | 検証スクリプト |
| 外部API契約の参照境界 | pass_with_provisional_assumption | `spec_ref`は未指定であり、詳細lintは未実施 |
| Markdown・Word・PDF投影 | not_performed | この版ではレンダリングを実施しない |
| AIモデル間の比較 | not_performed | 実験入力と実行記録が未提供 |

今回の検査範囲では上記の結果です。Schemaが合格しても、モデル内の仮定や候補値が正しいことを意味しません。
