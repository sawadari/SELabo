# ブラインドC1 strict評価：モバイルバッテリー

## 実行条件

- 実行日: 2026-08-22
- 入力: 許可された合成Q&A、階層型SEプロンプトの必要な契約・Schema、Compliance拡張01-09・README・Schema・validator/exporter・代表モデルのみ
- 隔離: 既存blind出力、review、remediatedモデルおよび他製品の評価出力は未参照
- 対象チェーン: 日本DENAN候補、UN 38.3/test-summary候補、日本の航空旅客携行候補の3件のみ

## 公式探索記録

実行したraw queryは次の3件であり、`candidate_model.json`の`regulatory_discovery_log`にも同一文字列、候補Source、採否理由、実行時点を記録した。全レコードの`query_log_state`は`complete`、人によるinventory確認は`pending`である。

1. `site:meti.go.jp モバイルバッテリー 電気用品安全法 PSE リチウムイオン蓄電池`
2. `site:unece.org UN 38.3 lithium battery test summary Manual of Tests and Criteria`
3. `site:mlit.go.jp モバイルバッテリー 航空機 持ち込み リチウムイオン電池 100Wh`

採用候補はMETI製品安全案内、UNECE UN Manual of Tests and Criteria Revision 8配布ページ、国土交通省2026年4月14日報道発表である。いずれも探索起点としての`adopted_candidate`であり、適用版、法的拘束経路、製品分類、事業者区分、便別条件は確定していない。

## モデル規模

|要素|件数|
|---|---:|
|Need|3|
|Requirement|3|
|Behavior|3|
|Structure|1|
|Verification Case|3|
|Validation Case|3|
|Source / Provision / Normative Statement|各3|
|Applicability / Obligation|各3|
|Engineering Projection|6|
|Evidence Requirement|3|
|Evidence Item|0|
|Assessment Result|3|
|Discovery Record|3|
|正規trace row|67|

## Assurance境界

- 全3件のAI適用判定は`uncertain`かつ`human_confirmation_state=pending`である。
- Evidence Itemは0件である。
- 全3件のAssessment Resultは`not_performed`である。
- AttestationおよびConformity Schemeは0件である。
- `assurance_outcome=not_performed`、`not_a_compliance_approval=true`であり、適合、認証、市場投入承認を主張しない。

## 検証結果

- `validate_candidate.py`: PASS (`ids=57`, `derived_relations=67`)
- `09_traceability.csv`: 67 data rows
- `export_compliance_views.py --check`: PASS (`files=5`)
- 生成物: `17_compliance_source_register.md`から`21_regulatory_discovery_log.md`までの5ファイル

## 評価

最小モデルとして3本の候補Source→Provision→Normative Statement→uncertain Applicability→candidate Obligation→Engineering Projection→Evidence Requirement→not-performed Assessment Resultの意味境界を保持した。構成・分類・数値仕様が未確定なため、次の人レビューではDENAN対象該当性、UN文書の適用版と国内輸送規則への取込み、日本の対象便と運送人追加条件を先に確定する必要がある。
