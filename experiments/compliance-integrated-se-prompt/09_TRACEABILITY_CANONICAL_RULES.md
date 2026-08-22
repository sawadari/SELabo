# Traceability正本規則

## 目的

この実験では、`10_se_model.json`内の要素別参照とトップレベル`relations[]`が同じ関係を競合して保持しないようにします。

## 正本規則

関係の正本は、意味を所有する要素の型付き直接参照です。

| 関係 | 正本フィールド例 |
|---|---|
| Stakeholder→Need | `needs[].stakeholder_refs` |
| Need→Requirement | `requirements[].source_need_refs` |
| Requirement→Behavior | `behaviors[].requirement_refs` |
| Requirement→Structure | `structures[].requirement_refs` |
| Requirement→Verification | `verification_cases[].target_requirement_refs` |
| Obligation→EngineeringProjection | `engineering_projections[].obligation_refs` |
| EngineeringProjection→Target | `engineering_projections[].target_refs` |
| EvidenceRequirement→対象 | `evidence_requirements[].target_refs` |

トップレベル`relations[]`は、型付きフィールドで表現できない補助関係だけに使用します。同じsource、target、relation typeを型付き参照と`relations[]`へ重複記録しません。

## 非Product投影先

Process、Assurance、Organization、Documentation、Supplierへの投影先は、トップレベル`projection_targets[]`へ型付きオブジェクトとして保存します。

```text
projection_kind                         target container
────────────────────────────────────────────────────────────
product / interface / constraint /     requirements[]
operational

process / assurance / organizational / projection_targets[]
documentation / supplier

evidence                               compliance.evidence_requirements[]
no_projection                          target_refs=[] + reason
```

`projection_targets[]`の`target_kind`は、参照するEngineeringProjectionの`projection_kind`と一致しなければなりません。

## CSV投影

`09_traceability.csv`は`relations[]`の単純コピーではありません。型付き直接参照から決定的に生成し、補助`relations[]`を重複排除して追加します。

開発者向けオフラインQAでは、同梱の検証ツールを任意で使用できます。ChatGPTのプロンプト専用回帰ではツールを使わず、型付き参照と期待不変条件を人が確認します。

```powershell
python scripts/validate_candidate.py <10_se_model.json> --trace-csv <09_traceability.csv>
```

生成する`relation_id`は、relation type、source ID、target IDの組からSHA-256で決定します。同じ入力関係からは同じIDが得られます。

## 必須Consistency Check

- 全IDが一意である。
- EngineeringProjectionのObligationとtargetが存在する。
- Product系targetは`requirements[]`に存在する。
- 非Product系targetは`projection_targets[]`に存在し、型が一致する。
- Evidence系targetは`evidence_requirements[]`に存在する。
- Compliance由来RequirementのObligation、Projection、逆向きtargetが一致する。
- MandatoryまたはProhibitionのObligationにEvidenceRequirementがある。
- CSVへ投影するsource IDとtarget IDがすべて解決する。

JSON Schemaは構造を検証し、このConsistency Checkは複数配列を横断する意味的参照を検証します。Schema合格だけをTraceability合格と扱いません。
