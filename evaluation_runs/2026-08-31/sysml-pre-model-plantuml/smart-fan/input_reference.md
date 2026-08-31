# 実験5試行入力

## 入力

- 対象システム：スマート扇風機
- 入力ファイル：[candidate_model.json](../../../2026-08-22/compliance-integrated-se-prompt/smart-fan/candidate_model.json)
- 入力の意味：実験1の階層型SEデータを基礎にした候補モデル。Compliance拡張フィールドは今回のPlantUML投影対象外とした。
- Schema：[実験1のse_model.schema.json](../../../../experiments/hierarchical-se-prompt/schemas/se_model.schema.json)

## 使用した実験5ファイル

- [01_CORE_PROMPT.md](../../../../experiments/sysml-pre-model-plantuml-prompt/01_CORE_PROMPT.md)
- [02_PLANTUML_PROFILE.json](../../../../experiments/sysml-pre-model-plantuml-prompt/02_PLANTUML_PROFILE.json)
- [03_OUTPUT_CONTRACT.json](../../../../experiments/sysml-pre-model-plantuml-prompt/03_OUTPUT_CONTRACT.json)
- [04_QUALITY_RULES.md](../../../../experiments/sysml-pre-model-plantuml-prompt/04_QUALITY_RULES.md)

## 試行範囲

この試行は、入力のcore SE sections（scope、stakeholders、scenarios、requirements、behaviors、structures、interfaces、constraints、verification_cases、relations）を読んで、生成可能なPlantUMLだけを作った。入力にないInterface、State、Constraint、Packageは作成していない。
