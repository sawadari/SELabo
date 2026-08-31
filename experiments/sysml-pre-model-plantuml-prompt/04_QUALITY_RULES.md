# 実験5 PlantUML投影品質規則

## QP-01 正本境界

`10_se_model.json`を候補意味正本とし、PlantUMLだけに存在する意味要素を許さない。図の見栄えを理由に正本へ反映されていない要素を追加しない。

判定：`pass`は、図に表示したCanonical IDが入力へ解決でき、追加要素がVIEW_DERIVEDまたはUNRESOLVEDとして明示されている場合に限る。

## QP-02 IDとAlias

Canonical要素は正本IDを表示名またはNoteへ残す。PlantUML Aliasは表示用であり、正本IDとは別物として扱う。Index、図メタデータ、TraceのID表記を一致させる。

## QP-03 VIEW_DERIVED

Scenarioの一文をActionまたはMessageへ分解する場合、その順序や分解はVIEW_DERIVEDである。`VD_`または`VIEW_DERIVED`を用いて表示し、正本のBehavior、Interface、State、Relationshipへ昇格させない。

## QP-04 UNRESOLVED

必要なsource、target、trigger、exchanged_item、equation、package_hierarchyが入力にない場合は創作しない。`TBD:`、`UNRESOLVED:`、Indexの未生成理由のいずれかで記録する。

## QP-05 図の生成条件

| 図 | 生成の最低条件 |
|---|---|
| Context | 対象システム、外部Actor/System、外部Interfaceの接続情報 |
| Requirement | Requirementが1件以上 |
| Use Case | Use CaseとActor関係 |
| Activity | Behaviorまたは明示順序を持つScenario |
| BDD | Structureが1件以上 |
| IBD | Structure、Interface、source/target、交換項目 |
| Sequence | Scenarioと送信者・受信者・順序を特定可能な情報 |
| State Machine | State、遷移元、遷移先、Trigger/Guard |
| Parametric | 式、parameter、property、binding |
| Verification Trace | Requirement、Verification Case、target参照 |
| Package | 明示されたpackage_hierarchy |

不足時に空の図だけを生成せず、`insufficient_data`としてIndexへ記録する。ただし、構造が不足していること自体をレビューする目的の図は、限界をタイトル・Noteへ明記したうえで生成してよい。

## QP-06 Relationship

Relationshipは`relations`の意味、型、source、target、direction_semantics、参照属性から確認する。既存の`source_need_refs`や`verification_case_refs`を使う場合は、どの正本属性を投影したかをコメントに残す。意味の確定しない関係を`deriveReqt`、`satisfy`、`verify`、`include`、`extend`、Composition、Generalizationへ変換しない。

## QP-07 抽象度

System Context、Black Box、Logical、Physical、Domain、Detailed Componentを原則として分ける。L0～L7は実験1の詳細化ラベルであり、SysMLの標準階層や製品分解階層と断定しない。

## QP-08 Cross-Diagram Consistency

- RequirementとBehaviorのRequirement参照が一致する。
- BehaviorのAllocation先がBDDのStructureと一致する。
- IBDのPart型がBDDまたはStructureとして存在する。
- SequenceのCanonical通信がIBDのInterfaceと矛盾しない。
- Stateで禁止される通信をSequenceが無条件に作らない。
- VerificationのTarget RequirementがRequirementへ解決する。

矛盾は都合よく図から消さず、FindingまたはUNRESOLVEDとして記録する。

## QP-09 PlantUML安全性

各図はUTF-8、`@startuml`、`@enduml`を持つ。外部URL、外部画像、ネットワーク依存includeを使わない。ローカルstyleのincludeは許可する。構文検証を実行していない場合は`syntax_validation: not_performed`とし、`pass`と書かない。

## QP-10 文章・名称

正本名称は原則変更しない。VIEW_DERIVEDのActionは対象＋動詞辞書形、Stateは持続状態の名詞句とする。未定義の「適切に」「十分に」「必要に応じて」などを要求本文へ追加しない。図のNoteでは、正本の未確定表現を確定値へ変換しない。

## QP-11 検査結果の分離

JSON Schema、参照整合性、図メタデータ、PlantUML境界、PlantUML実構文、SysML意味妥当性、人レビューを別の検査項目として記録する。ある検査のPASSを別の検査のPASSへ流用しない。

## QP-12 Stop Rule

次のいずれかがあれば、実験5の出力は`fail`または`below_reviewable`とする。

- 入力にないCanonical要素または関係を生成した。
- VIEW_DERIVEDを正本要素として表示した。
- 不足したState、Interface、Constraint、Protocol、数値を創作した。
- PlantUML構文を検証していないのにPASSと記録した。
- PlantUMLから正式SysMLモデル、XMI、認証、設計承認を主張した。
