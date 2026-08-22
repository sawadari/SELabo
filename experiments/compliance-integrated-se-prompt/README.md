# 法規・規格・認証統合SE初稿生成プロンプト

## 何を試す実験か

この実験は、[階層型SE初稿生成プロンプト](../hierarchical-se-prompt/README.md)を基礎に、法規・規格・契約・認証基準を通常のSE要求とは別のCompliance Layerとして扱うと、レビュー可能な初稿を作れるか確かめます。

元実験は変更しません。このフォルダーは元実験へ追加して使う拡張パッケージです。同じ対象を元実験と本実験で実行し、Compliance Layerの有無を比較できます。

## 中核となる考え方

法規の条文を直接SysML要求へ変換しません。次の意味境界を保ちます。

```text
外部の正式原典
  → Authority / Source / Provision
  → Normative Statement
  → Applicability Assessment
  → Obligation
  → Engineering Projection
  → SE要求・プロセス要求・Evidence Requirement
  → Assessment Activity / Evidence Item / Assessment Result
  → Attestation
```

`L0`～`L7`は設計詳細化軸のまま維持し、Compliance Layerを`L8`や特定レベルとして追加しません。暫定L0から市場、法域、製品分類、意図する使用、構成を得て適用性候補を作り、その結果をL1～L7へ横断投影します。

## 元実験から変えること

- `10_se_model.json`へ必須の`compliance`名前空間を追加します。
- `EngineeringProjection`を独立IDを持つ第一級オブジェクトにします。
- Process、Assurance、Organization、Documentation、Supplierの投影先を`projection_targets[]`へ保存します。
- 評価対象構成を`configurations[]`、責任主体を`parties_or_roles[]`へ保存します。
- Need ValidationとRequirement Verificationを別々に数えます。
- 自動探索の経路と採否を`regulatory_discovery_log[]`へ保存します。
- モデル品質、Assurance outcome、Reviewer別Gateを分離します。
- `requirements[].derivation_sources[]`で要求の工学分類と導出元を分離します。
- `requirement_type: regulatory_candidate`はこの実験では使用しません。
- 将来必要な`EvidenceRequirement`と、実在する`EvidenceItem`を分離します。
- SysMLへ投影する対象を製品・インターフェース・制約・運用要求とV&V候補に限定します。
- 法的適用、規格適合、認証取得をAIだけで確定しません。

## 正本の境界

法令・規格の真正な正本は外部の正式原典です。`10_se_model.json`が候補正本として保持するのは、参照した原典、版、条項、解釈候補、適用性候補、義務、工学投影、証拠要求およびそれらの関係です。

規格本文は原則として複製せず、識別子、版、条項位置、公式参照先、必要最小限の抜粋だけを記録します。利用条件が確認できない原典を全文保存しません。

## 使い方

元実験の次のファイルを、このフォルダーの実行ファイルと一緒にAIへ渡します。

- `../hierarchical-se-prompt/01_CORE_PROMPT.md`
- `../hierarchical-se-prompt/02_DEFAULT_PROFILE.json`
- `../hierarchical-se-prompt/03_OUTPUT_CONTRACT.json`
- `../hierarchical-se-prompt/04_QUALITY_RULES.md`
- `../hierarchical-se-prompt/10_JAPANESE_TECHNICAL_WRITING_STANDARD.md`
- `../hierarchical-se-prompt/11_JAPANESE_WRITING_PROFILE.json`
- `../hierarchical-se-prompt/schemas/se_model.schema.json`

本実験からは次を渡します。

- [01_CORE_PROMPT.md](01_CORE_PROMPT.md)
- [02_COMPLIANCE_PROFILE.json](02_COMPLIANCE_PROFILE.json)
- [03_COMPLIANCE_OUTPUT_EXTENSION.json](03_COMPLIANCE_OUTPUT_EXTENSION.json)
- [04_COMPLIANCE_QUALITY_RULES.md](04_COMPLIANCE_QUALITY_RULES.md)
- [schemas/compliance_se_model.schema.json](schemas/compliance_se_model.schema.json)
- [09_TRACEABILITY_CANONICAL_RULES.md](09_TRACEABILITY_CANONICAL_RULES.md)
- [10_CHATGPT_PROMPT_ONLY_REGRESSION.md](10_CHATGPT_PROMPT_ONLY_REGRESSION.md)

ユーザー入力には、分かる範囲で対象市場、法域、製品分類、意図する使用、ライフサイクル、対象構成、候補となる法令・規格・契約・認証スキームを含めます。分からない項目は空欄でも実行できますが、AIは未確認の条項番号や版を作らず、`uncertain`として人の確認へ送ります。

### ChatGPTでのプロンプト専用回帰（ツールなし）

ChatGPT上の回帰テストでは、Python、Web検索、ブラウザ、コード実行、コネクタ、その他のツールを使いません。固定入力に対する期待不変条件を人が判定する、プロンプトの行動回帰です。実行手順、R01～R10ケース、判定記録は[10_CHATGPT_PROMPT_ONLY_REGRESSION.md](10_CHATGPT_PROMPT_ONLY_REGRESSION.md)を使用します。

ツールを使っていないため、この回帰は法規の最新性、法的適用性、適合性、認証取得を証明しません。原典が与えられていない場合は、探索未実施と完全性非主張を品質報告に残し、実行済みqueryを創作しません。

## 出力

元実験の成果物をすべて生成し、さらに次を追加します。

| ファイル | 内容 |
|---|---|
| `17_compliance_source_register.md` | Authority、Source、Provision、版・発効日・入手状態 |
| `18_applicability_obligation_register.md` | 規範文、適用性候補、拘束根拠、Obligation |
| `19_engineering_projection_traceability.csv` | ObligationからSE・Process・Evidenceへの投影 |
| `20_conformity_evidence_plan.md` | 認証スキーム、評価活動、証拠要求、未評価事項 |
| `21_regulatory_discovery_log.md` | 公式探索先、query、候補Sourceの採否、網羅性限界 |

中心データは引き続き`10_se_model.json`です。追加MarkdownとCSVはこのJSONから投影します。

`09_traceability.csv`は空の`relations[]`をそのまま出力せず、要素別の型付き直接参照から決定的に生成します。非Product投影先とTraceの正本規則は[09_TRACEABILITY_CANONICAL_RULES.md](09_TRACEABILITY_CANONICAL_RULES.md)に定義しています。

### 開発者向けオフラインQA（任意）

ChatGPTの回帰テストとは別に、開発者がパッケージの構造・意味整合性を機械的に確認する任意のQAを行えます。このQAはChatGPT利用時の必須手順ではなく、プロンプト回帰のPASSや法的正確性を意味しません。

#### Trace CSV生成と候補モデル検証

```powershell
python scripts/validate_candidate.py <10_se_model.json> --trace-csv <09_traceability.csv>
```

この検証は合成Schemaに加え、複数配列を横断するObligation、EngineeringProjection、投影先、Evidence Requirementの参照と型を確認します。

Evidence Itemが存在しても自動的に適合扱いにせず、構成変更で証拠を失効させる後段経路は、公開可能な合成fixtureで検証します。

```powershell
python scripts/validate_assurance_fixture.py
python scripts/test_assurance_semantics.py
```

fixtureは`inconclusive`判定と`active`から`stale`への変更遷移を要求します。統合回帰はdefinitive outcomeとAttestationの成立・拒否条件をSchemaと意味検証の両方で確認します。合成試験データを実製品の証拠として使用してはなりません。

## 40点初稿で行わないこと

- 法令・規格の真正性や最新版であることを未確認のまま断定すること
- AIだけで`applicable`、`not_applicable`、`conforming`、認証取得済みを正式決定すること
- 実在しない試験報告、監査記録、証明書を`EvidenceItem`として作ること
- Authority、Source、Provision、ObligationをSysML Requirementへ直接変換すること
- ReqIF、OSCAL、SACM、LegalRuleML、Akoma Ntoso、XMIへの準拠や交換成功を、adapter検証なしに主張すること

## 成功条件

この実験のMVP成功条件は、正式な適合判定ではありません。少なくとも一つの対象事例で次を満たすことです。

1. 原典からEvidence RequirementまでIDで追跡できる。
2. 適用性判断に法域、市場、製品分類、用途、時点、仮定が残る。
3. Product系とProcess・Assurance・Documentation系の投影が混ざらない。
4. 実在する証拠と将来必要な証拠が混ざらない。
5. 重大な未確認事項が人の確認バックログへ送られる。
6. 元実験との比較で、誤った法規断定やトレース欠落が増えない。

実験手順と比較条件は[05_EXPERIMENT_PLAN.md](05_EXPERIMENT_PLAN.md)、実施済み検査は[07_VALIDATION_REPORT.md](07_VALIDATION_REPORT.md)に記録します。
