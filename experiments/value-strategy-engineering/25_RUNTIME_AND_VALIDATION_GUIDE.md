# スクリプト実行・自動検証ガイド

## 依存条件
Python 3.10以上、標準ライブラリ。JSON Schema検査に`jsonschema`を使用する（任意だが厳格検査には必要）。

```bash
python -m pip install jsonschema
python scripts/validate_vse.py examples/b2b_alm/10_vse_model.json --strict
python scripts/render_projections.py examples/b2b_alm/10_vse_model.json --output-dir /tmp/vse_out
python -m unittest discover -s tests -v
```

上記はZIP展開後、そのルートディレクトリで実行する。`render_projections.py`は正本JSONからMarkdown/CSV/manifestを再構築し、新しい戦略事実は追加しない。実顧客の検証、独立したAI Reviewer、マーケットリサーチ、営業実行は行わない。

## `validate_vse.py` が確認すること
- JSON Schemaの構文・属性・必要フィールド（`--strict`では`jsonschema`必須）。
- IDの一意性、参照先の存在、source_fragmentsの参照、状態の矛盾。
- relationの方向・型の契約、因果状態の有無、仮説にprediction/falsification/planがあるか。
- Decisionに人間の承認が記録されていないのに`approved`になっていないか。
- status quoの存在、source_fragmentsが本当の資料か仮想例か、実観測を装っていないか。

## 制約
- スクリプトは外部送信、LLM呼び出し、GitHub書き込みを行わない。
- 静的検査で文章の真実性や戦略の有効性は証明できない。
- `not_performed`を残す検査は、意図的な研究上の限界である。
