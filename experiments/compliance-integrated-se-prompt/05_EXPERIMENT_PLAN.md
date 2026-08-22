# Compliance Layer統合の実験計画

## この実験で確かめること

法規・規格・認証の情報を通常のSE要求へ直接混ぜず、Compliance Layerとして分離すると、40点初稿のレビュー可能性とトレーサビリティが改善するか確かめます。正式な法的適用性や認証取得の正しさをAI実験だけで証明する計画ではありません。

## 比較条件

同じ入力、同じAIモデル、同じ実行上限で次を比較します。

| 条件 | 内容 |
|---|---|
| B0 | 元の`hierarchical-se-prompt`だけを使用する |
| C1-blind | 履歴を引き継がない新規実行へ合成Q&Aだけを入力し、元実験と本Compliance拡張を使用する。B0 Finding、既存C1モデル、レビュー結果、他製品出力を見せない |
| C1-remediated | 元実験と本Compliance拡張に、既知Findingの修復指示を追加する。改善効果の帰属には使わない | 
| C2 | C1に、専門家が確認した市場・製品分類・適用原典一覧を追加する | 
| P0 | ChatGPT上の固定ケースをツールなしで実行するプロンプト専用回帰。法規の正確性ではなく、未確認情報を断定しない振る舞いの回帰を確認する | 

C1とC2では、取得していない規格本文をAIへ推測させません。C2はCompliance Layerの有無ではなく、入力品質が与える影響を分けて観察する条件です。

同じ生成担当を再利用して既存ファイルだけを隠したrunは、担当履歴を隔離できないためC1-blindの効果判定へ含めず、参考runとして区別します。

法規候補の自動探索を評価するrunでは、製品名だけで法令を決めず、構成候補、市場、法域、用途、ライフサイクルから公式台帳・所管官庁・発行主体を検索します。実行したquery、探索先、採用・除外・保留候補を保存し、`query_log_state=complete`のrunと過去ログを再構成したrunを混ぜません。人がinventoryを確認するまでは探索の完全性を成功指標にしません。

P0では法規候補の自動探索を行わず、与えられた原典と固定入力だけを使用します。`regulatory_discovery_log`に実行済みqueryを作らず、探索未実施と完全性非主張を品質報告に残します。ツール呼出しはP0の対象外であり、呼出しが発生したケースは失敗です。

P0の固定ケース、期待不変条件、判定記録は[10_CHATGPT_PROMPT_ONLY_REGRESSION.md](10_CHATGPT_PROMPT_ONLY_REGRESSION.md)に定義します。P0のPASSはプロンプト振る舞いの回帰であり、C1、C2の法的正確性や適合判定を意味しません。

## Pilot対象

最初は法規構造の異なる3事例以上を使います。

1. 製品特性と試験証拠を中心とする事例
2. 開発プロセス、組織、記録を含む事例
3. 型式承認、第三者評価または継続適合を含む事例

実在プロジェクトの機密情報を使う場合は、公開記録と分けます。原典の利用条件を確認し、規格本文を評価記録へ転載しません。

## 1実行で記録する項目

- 入力本文と提供した原典の一覧
- 先行Finding・既存モデル・レビュー結果へのアクセス可否
- AIモデル、プロンプト版、Schema版、実行日時
- 原典を実際に取得・確認した範囲
- 法規探索のraw query、公式探索先、採用・除外・保留候補、`query_log_state`
- Source、Provision、NormativeStatement、ApplicabilityAssessment、Obligation、EngineeringProjectionの件数
- `uncertain`な適用性の件数
- Product系、Process系、Assurance系、Documentation系、Evidence系の投影件数
- 原典からEvidenceRequirementまで到達できた経路数
- 投影のないObligation数
- mandatoryだがEvidenceRequirementのないObligation数
- 存在確認済みEvidenceItem数と、誤って生成された架空EvidenceItem数
- 人が採用、修正、却下した適用性・解釈・投影の件数
- 初稿生成時間、専門家レビュー時間、SEレビュー時間
- 重大Finding、False Pass、False Certification Claim
- P0のケース別期待不変条件、`tools_used=none`、ツール呼出し件数、人のPASS/FAIL判定

## Reviewerの役割

- Compliance Reviewer：原典、版、条項、拘束根拠、適用性、Obligationを確認する。
- SE Reviewer：EngineeringProjection、要求品質、設計・V&Vへの接続を確認する。
- Assurance Reviewer：評価活動、Evidence Requirement、Evidence Item、Assessment Resultを確認する。
- Meta-Judge：Reviewer間の不一致と重大な見逃しを記録する。

同じ人が複数役を担当する場合も、判定欄は分けます。AI評価だけで合格にしません。

## 成功指標

C1またはC2がB0に対して次を満たすか比較します。

- 原典、適用性、Obligation、工学要求の概念混同が減る。
- Process・Organization要求をProduct要求に誤分類する件数が減る。
- 原典から工学要求とEvidence Requirementまでの有効な追跡経路が増える。
- 架空の条項、証拠、適合・認証主張が増えない。
- 重大な未確認事項が人の確認バックログへ現れる。
- 専門家の修正理由が対象IDへ結び付く。

## Stop Rule

次の場合、その実行はCompliance初稿として`below_reviewable`に分類します。

- 原典または条項を捏造した。
- AIだけで正式な適用・適合・認証を決定した。
- applicableまたはuncertainな重大Obligationが追跡不能である。
- Product要求とProcess・Organization要求の区別がレビュー不能である。
- Evidence RequirementとEvidence Itemを区別できない。

40点Gateを通過しても、正式な法務判断、規格解釈、適合性評価、認証申請は別の活動として人が開始します。

## Pilot後の判断

- 継続：重大な虚偽を増やさず、追跡性またはレビュー時間が改善する。
- 修正：概念境界は有効だが、Schema、プロンプト、出力投影のどれかに再現性のある欠陥がある。
- 中止：Compliance Layerによって誤った権威付けやFalse Certification Claimが増え、人のレビューでも安定して検出できない。

P0のプロンプト専用回帰は、オフラインスクリプトの実行を必要としない。スクリプトは開発者が任意で行う構造・意味QAであり、P0の判定核にはしない。
