# 実験5計画

## 仮説

実験1の候補SEデータを意味の正本として固定し、Canonical／VIEW_DERIVED／UNRESOLVEDを分けたPlantUML投影を後段専用プロンプトで作ると、レビュー可能な図を得ながら、図側の意味創作を抑えられる。

## 比較条件

| 条件 | 内容 |
|---|---|
| B0 | SEデータを与えず、一般的な依頼だけでPlantUMLを作る |
| B1 | 実験1の`10_se_model.json`から自由形式で図を作る |
| P1 | 本実験5のコアプロンプト、Profile、Output Contract、Quality Rulesを使う |

同じ対象、同じ入力、同じモデルを使い、B1とP1で「正本ID保持」「未確定情報の創作」「生成しない図の判断」を比較する。P1の今回の試行は、まず代表1事例で行うパイロットである。

## 1実行で記録する項目

- 実験ID、対象、入力ファイル、入力ハッシュ
- 使用モデル、実行日時、プロンプト・Profile・Schemaの版
- 生成した図数と図種別
- `strict_projection`、`projection_with_view_derived_elements`、`insufficient_data`の件数
- Canonical IDの解決率と重複ID数
- VIEW_DERIVEDとUNRESOLVEDの明示件数
- 根拠のないActor、Block、Interface、State、Relationship、数値の件数
- Diagram間の不整合件数
- JSON Schema、参照、PlantUML構文、画像レンダリング、人レビューの実施状態
- 人が採用、修正、却下、保留した投影の数

## 成功判定

代表事例で、入力Schemaが通り、図のsource IDが入力へ解決し、未確定情報が明示され、根拠のないCanonical要素が0件であることをP1の機械的成功条件とする。PlantUMLレンダリング、人の意味レビュー、正式SysMLツールへの投入は別の検証であり、未実施なら`not_performed`と記録する。

## Stop Rule

入力にない意味要素の生成、VIEW_DERIVEDのCanonical化、未検証構文のPASS、正式モデル化や適合の誤主張が確認された場合、そのrunはP1として合格にしない。修正後は同じ入力ハッシュと版を記録して再試行する。

## 次の試験

次は、Interfaceと複数Structureを持つモデルでIBD・Sequence整合性を確認する。その後、構造化State TransitionとConstraintを追加した入力でState Machine・Parametricの生成条件を評価する。実験1の3製品評価へ遡及して図を作る場合は、対象モデルのSchemaと拡張フィールドを個別に記録する。
