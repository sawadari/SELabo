# 実験7：VSEデータプロンプト

## 会話から、価値・戦略・意思決定をレビュー可能なデータ候補へ変換する

**Value & Strategy Engineering (VSE) v1.0.0** は、[SELabo 実験1「SEデータプロンプト」](https://github.com/sawadari/SELabo/blob/main/experiments/hierarchical-se-prompt/README.md)の実験構造を参考に、**事業企画・マーケティング・戦略・B2B営業**を横断して利用するために、新たに設計した独立パッケージです。

ユーザーは、「サービスの方向性を考えたい」「顧客にどんな課題がありそうか」「なぜこの戦略がよいのか」といった通常の会話から始めます。VSEプロンプトは、その会話・添付資料を、目的、顧客・関係者、問題、価値、仮説、戦略代替案、決定、施策、証拠、検証結果として整理します。

ここで生成する **VSEデータ** は、戦略書でも営業提案書でもなく、ツール・文書形式に依存しない候補意味データです。中心ファイルは `10_vse_model.json`。ほかのMarkdown/CSV/図仕様は、同じデータからの**投影**です。

> **重要**：レビュー可能な候補の生成は、市場・顧客・収益性を証明することではありません。VSEの事業成果に対する有効性は、現時点で未実証です。

## 1. 全体の仕組み

```text
日常の会話／顧客の発言／資料／市場情報（権限・出自の確認）
                              ↓
                     VSEデータプロンプト
                              ↓
        10_vse_model.json 〈唯一の候補意味ソース〉
        ├─ 事業目的・対象境界・顧客・購買関係者
        ├─ 問題と価値、競合する仮説・反証条件
        ├─ 現状維持を含む戦略代替案と判断基準
        ├─ 営業・提供・施策・資源・リスク
        └─ Evidence、Experiment、Outcome、Decision、Relation
                              ↓
            品質規則／40点Gate／独立Reviewer（別工程）
                              ↓
       人がレビュー・採否・補足・実顧客/実環境で検証
                              ↓
          ┌─────────┬─────────┬─────────┐
          ↓         ↓         ↓         ↓
      企画資料   戦略比較表  営業仮説   実験・KPI計画
                              ↓
          実際の観測結果を正本候補に追記・影響分析
```

**運用上の原則**：顧客や市場は自社が直接制御する部品ではありません。企業が設計できる行動・組織・提供体制と、外部の顧客・競合による独立した意思決定を明確に区別します。

## 2. なぜVSEなのか

元のSELaboは、`Stakeholder → Need → Requirement → Behavior/Structure → Verification & Validation`のつながりを、初期の会話から候補として生成します。これをマーケティングの用語へ単純置換するだけでは、「要求」と「顧客の行動予測」、また「トレーサビリティ」と「因果関係」を混同します。

VSEはこの問題を避けるため、**目的/範囲、顧客課題、価値仮説、代替戦略、行動、観測、判断、根拠の管理**として再定義しました。着想はSEにあるものの、マーケティング戦略論、QFD、Dynamic Capabilities、B2B営業研究、DSR/ADRを参照して設計しています。個別の根拠と限界は [`08_REFERENCES.md`](08_REFERENCES.md) と [`09_REFERENCE_BASIS.md`](09_REFERENCE_BASIS.md) を参照してください。

## 3. VSEデータとVSEプロンプトは異なる

| 名前 | 役割 |
|---|---|
| VSEデータ | 目的、顧客、価値、仮説、代替案、検証などをIDと関係で管理する候補中間データ |
| VSEデータプロンプト | 会話と資料を取り込み、上記候補データを生成・品質検査・投影するための指示 |
| 40点Gate | 不確実性を保持したまま、人が初期レビューできるかを判定する規則 |
| 独立Reviewer | 生成担当とは別の評価プロセス。J0のSelf Reviewは独立評価ではない |

## 4. V0～V7は「処理の順番」ではなく8つの分析視点

| View | 名称 | 主な問い |
|---|---|---|
| V0 | 事業・機会 | なぜ取り組むか。何を改善するか |
| V1 | 関係者・エコシステム | 誰が関与し、誰が意思決定するか |
| V2 | 顧客・業務文脈 | 顧客はどんな場面で何に困るか |
| V3 | 市場・価値仮説 | 何が価値を生むという説明か、何で反証するか |
| V4 | 価値提供構想 | どの製品・サービス・能力で価値を提供するか |
| V5 | 戦略・意思決定 | どの案を選び、どの案を選ばないか |
| V6 | 実行・営業 | 誰がどの接点・体制で実行するか |
| V7 | 検証・学習 | どう観測し、どの判断・仮説を更新するか |

視点は複数同時に適用可能で、製品/組織/市場/ライフサイクルの区分とは独立しています。全視点を必ず同量埋めることは求めません。

## 5. 情報の種類と、AIが勝手に「確認済み」にできないこと

VSEは、`origin`（入力・推論の由来）、`claim_state`（主張状態）、`decision_state`（採否状態）、`validity_state`（有効性）、`confidence`（暫定的信頼度）、`source_refs`（出典ID）を別々に記録します。

例えば、顧客から「ALMの利用が定着していない」と相談されても、その直接原因が「操作教育の不足」であるとは限りません。AIは「操作」「業務責任」「二重登録」など複数の原因仮説を生成し、それぞれの観測可能な予測と反証条件を記します。**仮説を事実として増殖させません**。

また、`supports`（根拠として支持する）と`causally_influences`（因果仮説）は別の関係です。「施策Aを行えば売上が上がる」という予測は、実験や適切な観測なしには確定できません。

## 6. 基本的な使い方

### 6-1. まず普通の会話で対象を説明する

例えば、次のように説明します。

```text
製造業向けのALM導入支援事業を検討しています。
顧客の一部では、教育を実施してもツールの利用が定着しない可能性があります。
操作教育、業務設計、既存成果物との二重管理のどれが主要課題か不明です。
どのサービスを提案すべきか、顧客に確認するための仮説と戦略の候補を整理したいです。
```

最初からSTP、4P、QFD、SysML、専用入力フォームに沿う必要はありません。

### 6-2. 必須ファイルをChatGPTに渡す

次のファイルを同時に添付し、「`01_CORE_PROMPT.md`の内容を実行し、出力契約に従って初稿ZIPを作ってください」と依頼します。

| ファイル | 役割 |
|---|---|
| [`01_CORE_PROMPT.md`](01_CORE_PROMPT.md) | 実行用プロンプト |
| [`02_DEFAULT_PROFILE.json`](02_DEFAULT_PROFILE.json) | 視点、状態、推論制約、初期設定 |
| [`03_OUTPUT_CONTRACT.json`](03_OUTPUT_CONTRACT.json) | 生成ファイル・投影の契約 |
| [`04_QUALITY_RULES.md`](04_QUALITY_RULES.md) | 品質規則 |
| [`10_JAPANESE_TECHNICAL_WRITING_STANDARD.md`](10_JAPANESE_TECHNICAL_WRITING_STANDARD.md) | 日本語による仮説・戦略・根拠の書き分け |
| [`11_JAPANESE_WRITING_PROFILE.json`](11_JAPANESE_WRITING_PROFILE.json) | 日本語規則のJSON |
| [`17_FORTY_POINT_GATE.md`](17_FORTY_POINT_GATE.md) | 40点Gateと停止規則 |
| [`schemas/vse_model.schema.json`](schemas/vse_model.schema.json) | 中心JSONのSchema |
| [`schemas/relation_type_contract.json`](schemas/relation_type_contract.json) | 関係型の意味と方向 |

必要なら[`05_USE_CASE_GUIDE.md`](05_USE_CASE_GUIDE.md)や[`06_CUSTOMIZATION_EXAMPLES.json`](06_CUSTOMIZATION_EXAMPLES.json)を追加して対象領域を選びます。

### 6-3. 最初に読むべき出力

標準の生成物は17ファイル（契約は`03_OUTPUT_CONTRACT.json`）。特に`01_executive_summary.md`で目的と主要な不確実性、`06_strategy_alternatives.md`で現状維持を含む比較、`08_validation_plan.md`で次の顧客確認、`13_quality_report.md`で未実施検査を読みます。

`10_vse_model.json`を**候補意味ソース**として扱い、表・グラフ・レビュー文書は再投影します。中心JSONは承認済み戦略でも市場の真実でもありません。

### 6-4. 人間が採否・更新する

- 「HYP-0002に根拠はありますか。反対証拠は何ですか」
- 「ALT-0001の現状維持と、ALT-0003の診断を共通の基準で比較してください」
- 「新しく得た顧客の意見が、DEC-0001の選択条件をどう変えますか」
- 「実顧客確認がない部分を未確認として残してください」

承認した事実だけ人間が確認済みへ変更します。新資料を反映する場合は元のIDを維持し、変更履歴と影響範囲を残します。

## 7. 40点Gate

40点は採点上の40/100ではありません。目的・顧客/問題・主要仮説/証拠・現状維持を含む代替案・次の検証が**レビューできる**状態を指します。未確認の数値や架空の事実が増えた状態は`overspecified_beyond_40`です。`17_FORTY_POINT_GATE.md`を参照してください。

## 8. 独立Reviewerと研究上の限界

通常のGenerator自己検査はJ0。別会話のJ1、別モデルのJ2、複数独立ReviewerのJ3、実在の専門家や顧客による校正を加えたJ4を区別します。4ラウンドの過去の役割別批判は**設計上の模擬レビュー**であり、J3/J4の実施を意味しません。

RQとB0/B1/B2/B3の比較実験計画は[`19_EXPERIMENT_PLAN.md`](19_EXPERIMENT_PLAN.md)に記録しています。

## 9. 同梱の再現可能な架空例

- [`examples/b2b_alm/10_vse_model.json`](examples/b2b_alm/10_vse_model.json)：ALM定着改善コンサルティングに関する架空の初期検討。**実在顧客の内容ではない**。
- [`examples/b2b_alm/candidate_bundle/01_executive_summary.md`](examples/b2b_alm/candidate_bundle/01_executive_summary.md)：B2B例の投影サマリー。
- [`examples/consumer_product/10_vse_model.json`](examples/consumer_product/10_vse_model.json)：静音卓上ファンの架空の製品企画。
- 両ケースとも`candidate_bundle`に17ファイルの出力例を同梱します。

### ローカルで再検証する

```bash
python -m pip install jsonschema
python scripts/validate_vse.py examples/b2b_alm/10_vse_model.json --strict
python scripts/render_projections.py examples/b2b_alm/10_vse_model.json --output-dir /tmp/vse_render --strict
python -m unittest discover -s tests -v
```

Python 3.10+を前提とし、スクリプトは外部送信・LLM呼び出し・GitHub書き込みを行いません。検査は構文・参照・特定の整合性を対象とし、実市場での妥当性は確認できません。

## 10. ファイル案内

| ファイル | 内容 |
|---|---|
| `01_CORE_PROMPT.md` | 実行プロンプト |
| `02_DEFAULT_PROFILE.json` | 初期設定とV0～V7 |
| `03_OUTPUT_CONTRACT.json` | 17出力ファイルの契約 |
| `04_QUALITY_RULES.md` | 品質規則 |
| `05_USE_CASE_GUIDE.md` | 企画/営業/製品/検証の用途 |
| `06_CUSTOMIZATION_EXAMPLES.json` | B2B/B2C/SaaS/戦略の上書き例 |
| `07_VALIDATION_REPORT.md` | 本ZIPの技術検査と未検証事項 |
| `08_REFERENCES.md` | 学術・方法論上の参考文献 |
| `09_REFERENCE_BASIS.md` | 論文から設計規則への追跡 |
| `10_JAPANESE_TECHNICAL_WRITING_STANDARD.md` | 日本語戦略・仮説文章標準 |
| `11_JAPANESE_WRITING_PROFILE.json` | 日本語規則の機械可読版 |
| `12_RULE_SOURCE_TRACEABILITY.csv` | 規則と学術根拠の関係 |
| `13_CHATGPT_DISTRIBUTION_GUIDE.md` | ChatGPTでの配布・実行 |
| `14_CHATGPT_APP_CONCEPT_SPEC.md` | 将来のアプリ概念仕様、未実装 |
| `15_RELEASE_NOTES.md` | リリース履歴 |
| `16_PUBLICATION_CHECKLIST.md` | 公開前の確認 |
| `17_FORTY_POINT_GATE.md` | 40点Gateと停止規則 |
| `18_AI_EVALUATION_PROTOCOL.md` | Reviewer独立性と評価手順 |
| `19_EXPERIMENT_PLAN.md` | B0/B1/B2/B3比較・G1～G4研究計画 |
| `20_SOURCE_TRUST_AND_HUMAN_AUTHORITY.md` | ソースの信頼と人の権限 |
| `21_CONCEPTUAL_MODEL_AND_ONTOLOGY.md` | 要素・型付き関係・境界 |
| `22_DECISION_AND_LEARNING_PROTOCOL.md` | 人間の選択と差分更新 |
| `23_FOUR_ROUND_CRITIQUE_AND_DESIGN_DECISIONS.md` | 4回の模擬レビューと設計決定 |
| `24_COMPARATIVE_EVIDENCE_MATRIX.md` | 先行研究と未検証の区別 |
| `25_RUNTIME_AND_VALIDATION_GUIDE.md` | スクリプト実行手順 |
| `schemas/` | VSEモデルSchema、Relation契約 |
| `scripts/` | VSE候補の構造検査、投影生成、架空ケース生成 |
| `tests/` | 回帰検査（故意に壊したモデルの検出を含む） |
| `examples/` | 2つの架空ケース、各17ファイルの投影例 |
| `package_manifest.json` | パッケージのファイルハッシュ一覧 |

## 11. できないこと

実顧客の需要保証、価格の確定、顧客が買うかの予測保証、売上改善の保証、因果効果の自動判定、正式な事業・契約・投資承認はできません。実在専門家・営業・顧客による外部検証も、このZIPの自動検査には含まれません。

VSEは戦略立案を自動完了するためのシステムではなく、**不確実な環境で人間がより良い問い・比較・検証を行えるか**を研究するための候補データ生成方法論です。
