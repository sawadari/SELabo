# 検証報告

## 対象版

- Experiment：`compliance-integrated-se-prompt`
- Version：`0.3.1`
- Date：`2026-08-22`

## v0.3.1修正

- Process、Assurance、Organization、Documentation、Supplier投影の共通正本`projection_targets[]`を追加した。
- EngineeringProjectionの`projection_kind`と参照先型の一致をSchema外の意味検証へ追加した。
- 型付き直接参照を関係正本、`relations[]`を補助関係専用とし、`09_traceability.csv`を決定的に生成する規則を追加した。
- 合成Evidence fixtureで、Evidence Itemが存在しても判定材料不足なら`inconclusive`とし、構成変更後は`active`から`stale`へ遷移する経路を追加した。
- Need Validation、版付き構成、責任ロール、探索ログ、Reviewer別Gateを正本へ追加した。
- Evidence、Assessment Activity、Assessment Result、Attestationの成立条件とSource失効伝播を意味検証へ追加した。
- definitive outcomeに、権限確認済みApplicability確認者、公式取得またはユーザー提供のSource版識別、ユーザー確認済みベースライン構成を必須化した。
- issued Attestationに、Schemeの全Obligation・Evidence、decision authority、Scheme適合対象との一致、有効期限を必須化した。
- JSON Schemaの日付・日時Format検証を有効化し、不正な期限文字列を有効期限なしとして通さない。
- Validation Caseの代表Scenario、Discovery Logの参照とquery記録状態、Conformity Scheme参照の意味検証を追加した。
- Behaviorのperformer候補と保持Structure／ownerの一致を検査し、異なる人の運用責任を1つのStructureへ混在させない規則を追加した。

## 実施済み

| 検査 | 結果 |
|---|---|
| JSON設定、Schema、代表fixtureの構文解析 | PASS |
| 元Schemaとv0.3.1拡張Schemaを合成した代表fixture | PASS、14 ID、16導出関係 |
| スマート扇風機モデル | PASS、98 ID、132導出関係 |
| 懐中電灯モデル | PASS、75 ID、88導出関係 |
| モバイルバッテリーモデル | PASS、146 ID、197導出関係 |
| 3製品のNeed Validation | PASS、14/14 |
| 3製品の構成・責任ロール参照 | PASS |
| ObligationからEngineeringProjection・Evidence Requirementへの到達 | PASS、16/16 |
| 3製品の`09_traceability.csv`決定生成 | PASS |
| 合成Evidence Itemのartifact SHA-256照合 | PASS |
| 合成Assessment Resultの安全側判定 | PASS、`inconclusive` |
| 構成変更時の証拠状態遷移 | PASS、`active → stale` |
| Assurance統合回帰 | PASS、正例4ケース・負例65ケース |
| 追加5成果物の正本からの生成・完全一致検査 | PASS、3/3製品 |
| strict C1-blindの3製品validator | PASS、54/50/57 ID、70/61/67導出関係 |
| strict C1-blindのDiscovery Log | PASS、10/10 recordが`query_log_state=complete` |
| strict C1-blind独立Compliance J1 | FAIL / revise、Source・Provision・投影のHigh 5件、Medium 2件 |

## ChatGPT・プロンプト専用回帰の扱い

ChatGPT利用時の回帰テストは、[10_CHATGPT_PROMPT_ONLY_REGRESSION.md](10_CHATGPT_PROMPT_ONLY_REGRESSION.md)のR01～R10を固定入力とし、外部検索、Python、Web、コード実行、コネクタ、その他のツールを使わず、期待不変条件を人が判定する。ツール呼出しや未提供情報の補完は、そのケースの`FAIL`とする。本レポート中の既存の「統合回帰 PASS」はオフラインスクリプトによる開発者QAであり、ChatGPTプロンプト回帰のPASSとは分けて扱う。

R01～R10の実行結果は、使用モデル、プロンプト版、実行日時、判定者、`tools_used=none`、ケース別PASS/FAILを別途記録する。回帰ケースの実行結果は本版パッケージの法的正確性や製品適合を示さない。

## 開発者向けオフラインQAの実行コマンド（任意）

ChatGPTのプロンプト専用回帰では、以下のコマンドを実行しない。これらは開発者が任意で行うオフラインQAである。

```powershell
python scripts/validate_candidate.py <candidate_model.json> --trace-csv <09_traceability.csv>
python scripts/validate_assurance_fixture.py
python scripts/test_assurance_semantics.py
```

## 実験で確認済み

- 3製品を別サブエージェントで生成した`C1-remediated`評価
- Applicability 9/9を`uncertain`、`human_confirmation_state=pending`かつ人確認必須として保持
- Evidence ItemとAttestationを根拠なく生成しない境界
- 3製品すべてで法的適用、適合、認証取得の確定主張が0件
- v0.2モデルに対するCompliance、SE、Assurance独立レビューの分離実行
- 履歴を引き継がない新規サブエージェントによる3製品strict C1-blindと独立Compliance J1

## 未実施

- 専門家が確認した入力を使うC2
- 元出力Bundle全体とSysML投影の一致検査
- ReqIF、OSCAL、SACM、LegalRuleML、Akoma Ntoso、SysMLツールとのadapter検証
- 実製品の証拠を使う適合性評価、監査、申請、承認

## 解釈

この報告は、v0.3.1の候補モデル、参照、投影先型、Trace生成、Reviewer Gateと合成Assurance経路が機械的に扱えることを示します。strict C1-blindでは製品別候補と検索ログを自動生成できましたが、独立J1は法令正本、Provision位置、義務主体、拘束根拠の誤りを検出しました。したがって、法的正確性、inventory網羅性、規格適合性、認証取得可能性、製品安全または市場投入可否を示すものではありません。
