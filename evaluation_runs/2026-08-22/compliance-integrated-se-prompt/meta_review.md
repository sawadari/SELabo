# 3製品C1横断Meta Review

## 結論

`compliance-integrated-se-prompt` v0.3.1は、Compliance情報を通常要求へ直接混入せず、Source、Provision、Normative Statement、Applicability、Obligation、Engineering Projection、Evidenceを分離して機械処理できる段階へ到達した。3製品のC1-remediatedはSchema、意味参照、決定的Trace、17–21同期に合格し、独立SE J1も未閉鎖High／Medium 0件で`pass_with_provisional_assumption`となった。

一方、製品適合の総合Gateは`revise`である。理由は次のとおりである。

- 3製品のApplicabilityはすべて人確認前で、Assessment Resultは`not_performed`である。
- C1-remediatedの原始検索queryは保存されておらず、法規inventoryの網羅性を再現できない。
- strict C1-blindでは製品別候補の自動発見と検索ログ保存は成立したが、独立Compliance J1がSource同一性、条項位置、義務主体、拘束根拠のHigh Findingを検出した。
- 実製品Evidence、適合性評価、Attestation、専門家による適用判断は未実施である。

したがって、Pilot判断は**修正継続**とする。メタモデルと安全側状態管理のsource patchは合格したが、自動探索結果をそのまま適合・法的inventoryとして採用してはならない。

## 実験枠

| 枠 | 目的 | 入力隔離 | 扱い |
|---|---|---|---|
| `C1-remediated` | B0の既知Findingと独立J1 Findingを修復し、メタモデル・validatorの成立性を評価 | 既知Findingを使用 | source patchの回帰評価 |
| `C1-blind` | 同じ製品担当を再利用し、既存ファイルを読まずに再生成 | ファイルのみ隔離 | 担当履歴が残るため参考run |
| `strict C1-blind` | 履歴を引き継がない新規サブエージェントで自動探索効果を評価 | 会話履歴、B0、remediated、review、他製品出力を隔離 | 効果判定の正本 |

strict runは[別枠README](../compliance-integrated-se-prompt-blind-c1-strict/README.md)と[独立Compliance J1](../compliance-integrated-se-prompt-blind-c1-strict/blind_c1_review.md)に記録した。

## C1-remediated最終状態

| 製品 | validator | Trace | export | 独立SE J1 | Compliance／Assurance境界 |
|---|---:|---:|---|---|---|
| スマート扇風機 | PASS、98 ID | 132 | PASS | `pass_with_provisional_assumption` | APP pending、Evidence 0、評価未実施 |
| 懐中電灯 | PASS、75 ID | 88 | PASS | `pass_with_provisional_assumption` | APP pending、Evidence 0、評価未実施 |
| モバイルバッテリー | PASS、146 ID | 197 | PASS | `pass_with_provisional_assumption` | APP pending、Evidence 0、評価未実施 |

独立Compliance J1では初回Finding 9件がclosed、1件がpartially closedで、3製品のsource-patch Closure GateはPASSした。ただしlegacy Discoveryの網羅性未証明と人によるApplicability確認待ちのため、Compliance総合は`revise`である。

独立Assurance J1ではsource-patchと3製品のFalse Pass防止境界がPASSした。合成fixtureは`inconclusive`と`active → stale`を再現し、統合回帰は正例4件・負例65件にPASSした。外部原典取得の真正性は人確認依存、実製品Assuranceは`not_performed`である。

## strict C1-blind結果

| 製品 | ID / Trace | raw query / RDL | 自動発見した主要候補 | 独立Compliance J1 |
|---|---:|---:|---|---|
| スマート扇風機 | 54 / 70 | 17 / 4 | DENAN、長期使用表示、Wi-Fi条件付き電波法 | `revise`、Medium 1 |
| 懐中電灯 | 50 / 61 | 12 / 3 | 充電式携帯電灯のDENAN候補、重大製品事故報告、JISC候補 | `revise / fail`、High 1 |
| モバイルバッテリー | 57 / 67 | 3 / 3 | METI電池安全案内、UN 38.3、航空旅客携行 | `revise / fail`、High 4・Medium 1 |

全10 Discovery recordは`query_log_state=complete`である。全8 APPは`uncertain / pending`、Evidence ItemとAttestationは0件、Assessment Resultは全件`not_performed`で、False conformity/certification claimは0件だった。

ただし独立J1は次を検出した。

- スマート扇風機：電波法第4条と第38条の7の義務主体・表示条項を混在させた。
- 懐中電灯：充電式携帯電灯の施行令別表位置を誤記した。
- モバイルバッテリー：DENAN行政案内を直接法規義務へ昇格、UN Manualへtest-summary提供義務を誤帰属、文書義務をProduct Requirementへ誤投影、MLIT報道発表をdirect regulation扱い、航空候補を部分抽出した。

この結果から、自動探索は「製品に応じた候補を見つけ、人へ返す」用途には有効だが、「適用法規を網羅し、正しい条項・主体・拘束根拠まで確定する」用途には不十分と判定する。

## Meta FindingのClosure

| Finding | 最終状態 | 根拠 |
|---|---|---|
| `META-C1-FND-001` 非Product投影の格納先未定義 | `closed` | 共通`projection_targets[]`と種別一致検査を実装 |
| `META-C1-FND-002` 改善効果の帰属不能 | `evaluated` | strict C1-blindを別枠実施。自動探索の有効性と意味品質不足を分離 |
| `META-C1-FND-003` 独立Reviewer不足 | `closed_for_pilot` | Compliance、SE、Assuranceの独立J1とstrict blind独立Compliance J1を実施 |
| `META-C1-FND-004` Assurance後段未評価 | `partially_closed` | 合成fixtureと65負例まで完了。実製品Evidenceは未実施 |
| `META-C1-FND-005` 出力投影未評価 | `partially_closed` | 09と17–21は3製品で同期PASS。元Bundle全体と外部adapterは未実施 |
| `META-C1-FND-006` 関係正本が不明 | `closed` | 型付き直接参照を正本、`relations[]`を補助とし決定生成 |

## 次の段階

1. strict blindのHigh Findingは生出力の評価証拠として保持し、自動修正で上書きしない。
2. C2では、専門家確認済みの市場、構成、製品分類、事業者役割、原典inventoryを入力する。
3. Source／Provisionの権限者確認者と確認日時を記録し、外部原典snapshotの真正性確認方法を決める。
4. 実在または公開可能な製品Evidenceを使い、Evidence Item、Assessment Result、変更失効を評価する。
5. 元SE Bundle全体とReqIF、OSCAL、SACM、LegalRuleML、Akoma Ntoso、SysML adapterを別実験で検証する。

このMeta Reviewは製品適合、PSE表示可否、UN 38.3適合、航空輸送可否、認証取得または市場投入承認を意味しない。
