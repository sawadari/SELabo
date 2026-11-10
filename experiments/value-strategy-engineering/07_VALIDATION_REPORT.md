# VSE v1.0.0 検証レポート

検証日：2026-11-10（日本時間）

## 1. 実施した検査

1. `schemas/vse_model.schema.json`：JSON Schema Draft 2020-12による2つの架空ケースの検証。
2. `scripts/validate_vse.py`：ID一意性、参照解決、関係型・方向、状態、現状維持案、因果の不正昇格等を検査。
3. `scripts/render_projections.py`：各ケースで17種類の成果物を正本JSONから生成。
4. `python -m unittest discover -s tests -v`：構造的な不正を意図的に混入したケースを含む12個の回帰テスト。
5. `16_generation_manifest.json`：サンプルにおける自動投影ファイルのSHA256を収録。パッケージ全体のSHA256は`package_manifest.json`。

## 2. 結果

| 対象 | 結果 | 備考 |
|---|---|---|
| B2B ALM架空例：Schema/関係検証 | pass | 情報源はすべて架空 |
| 新製品企画架空例：Schema/関係検証 | pass | 市場実測値なし |
| B2B ALM：17ファイル投影 | pass | Markdown, JSON, CSV, Mermaid図仕様 |
| 新製品企画：17ファイル投影 | pass | 同上 |
| Python回帰テスト12件 | pass | バリデーターと投影の自動検査 |
| ZIP完全性 / package_manifest照合 | pass | ZIP 72ファイルの展開テストとパッケージSHA256照合で確認 |

## 3. 実施していない検査

- 実在の顧客ヒアリング・実需の検証・マーケティング施策の効果測定。
- 実在のマーケティング/営業/SE専門家による独立レビュー。
- 異なるAIモデルを使用したJ1～J4の独立評価。
- 因果効果の推定、商談化率や売上の改善を検証する実案件評価。
- このプロンプトでChatGPTがあらゆる入力に対して17ファイルを完璧に生成することの保証。

## 4. 読み方
このレポートの`pass`は**パッケージの静的構造とサンプルの技術的再現性**に対する判定であり、戦略の妥当性や事業成果に対する判定ではない。`reviewable_40_candidate`も人によるレビューを開始できる候補という意味に限る。

## 5. 再現方法

```bash
python -m pip install jsonschema
python scripts/validate_vse.py examples/b2b_alm/10_vse_model.json --strict
python scripts/validate_vse.py examples/consumer_product/10_vse_model.json --strict
python -m unittest discover -s tests -v
python scripts/validate_package.py
```

`validate_package.py`は全ファイルを含む配布ZIP展開後に動く。スクリプト実行で追加されるPythonの`__pycache__`はハッシュ対象に含めない。
