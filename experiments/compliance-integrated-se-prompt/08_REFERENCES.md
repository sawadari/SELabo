# 参考にした概念と標準

この実験は特定標準の準拠実装ではありません。次の標準・仕様が整理した概念境界を参考にした、SELabo独自の軽量Canonical Modelです。

| 対象 | 参考にした概念 |
|---|---|
| OASIS Akoma Ntoso 1.0 | 法令文書、条項、識別子、参照構造 |
| OASIS LegalRuleML 1.0 | Authority、Jurisdiction、規範、時間、解釈、原典と規則の対応 |
| ISO/IEC 17000 | 適合性評価の共通概念と語彙 |
| ISO/IEC 17007 | 評価可能な規定要求と適合性評価手段 |
| ISO/IEC 17067 | 製品認証スキーム |
| NIST OSCAL | Control、Implementation、Assessmentの層分離とMapping |
| OMG ReqIF 1.2 | 工学要求と属性・関係の交換 |
| OMG SACM 2.3 | Claim、Argument、Evidence、provenance |
| ISO/IEC/IEEE 29148 | Engineering Projection後の要求品質 |
| ISO/IEC/IEEE 15288 | 製品・プロセス・ライフサイクルへの展開 |
| OMG SysML 1.7 / 2.0 | 工学要求、設計、V&Vへのモデル投影 |

## 採用した責務分離

- LegalRuleMLやAkoma Ntosoを直接実装せず、Authority、Source、Provision、NormativeStatementの境界を借ります。
- OSCALをCanonical Modelにせず、SourceからImplementation、Assessmentへ進む層分離とMappingを借ります。
- ReqIFは工学要求化した後の交換先とし、法的AuthorityやApplicabilityの正本にしません。
- SACMはEvidenceから適合・保証Claimを論証する将来adapterの接続先とします。
- SysMLはEngineering Projection後の工学モデルへ限定します。

## 注意

版、発行日、現行性、利用条件は使用時に各発行主体の正式情報で確認してください。このファイルは規格本文を再配布せず、適合や準拠を主張しません。
