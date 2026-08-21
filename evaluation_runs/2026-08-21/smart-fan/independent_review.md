# Smart Fan Independent Review

## 結論

- `gate_state: below_reviewable`。レビュー材料は豊富だが、Need IDの未定義と主要要素の属性欠落により、主要Traceと出自・状態を独立に再現できない。
- `hard_blocker: true`。未管理の重要なTrace／provenance欠落がある。一方、承認済み・正本・ベースライン扱い、根拠なしの確定数値、法規・安全の確定主張、L6/L7過剰詳細化は確認されない。
- 最小修正後に再評価可能。`human_confirmation_required: true`、特に安全停止、静音条件、通信断時の責任境界、電源・保守条件は人の確認が必要。

## 評価メタデータ

|項目|判定|
|---|---|
|reviewer|independent reviewer（生成時の自己整理とは別会話）|
|evaluation_date|2026-08-21（Asia/Tokyo）|
|gate_version|`17_FORTY_POINT_GATE.md`|
|protocol_version|`18_AI_EVALUATION_PROTOCOL.md`|
|対象|`evaluation_runs/2026-08-21/smart-fan/chat_and_candidate.md`のみ|

## 40点Gate評価

|評価軸|状態|根拠／件数|
|---|---|---|
|Stakeholder → Need|`weak`|5/5行は対応しているが、Need候補表に`SF-NEED-01`〜`05`の定義・IDがなく、Trace側の参照を明示検証できない。|
|Need → Requirement|`missing`（明示Trace）|`SF-TR-01`〜`05`のNeed参照は行順なら推測できるが、定義済みNeed IDへの明示リンクは0/5。|
|Requirement → Behavior / Structure|`weak`|5/5行に候補はあるが、意味の整合が十分なのは3/5。REQ-01のモード集合とBEH-01の状態、REQ-03の静音条件が未定義。|
|Requirement → V&V candidate|`weak`|5/5行にV&V候補はあるが、受入れ尺度・危険状態・停止閾値・測定条件が未確定で、十分なのは2/5。|
|主要要素の`origin`/`claim_state`/`decision_state`|`missing`|StakeholderとRequirementには付くが、Behavior、Structure、V&V候補（少なくとも15要素）には個別属性がない。100%を確認できない。|
|1要求1義務|`weak`|REQ-04は「停止または再開」を一つに束ね、厳密には4/5=80%（初期目安85%未満）。REQ-03も測定可能な条件が未定義。|
|過剰詳細化|`sufficient`|部品型番、公差、詳細アルゴリズム、実装クラス等の創作はない。|

主要Traceの明示的な判定は、Need→Requirement `0/5`、Requirement→Behavior/Structure `3/5 sufficient`、Requirement→V&V `2/5 sufficient`。行の存在だけを数えた自己整理の`5/5`とは区別する。

## Hard Blocker

|ID|判定|内容|
|---|---|---|
|HB-01|該当|Need IDが定義されず、必要性のTraceを独立に再現できない。重要なTrace評価軸の欠落。|
|HB-02|該当|Behavior / Structure / V&V候補の個別`origin`・`claim_state`・`decision_state`がなく、主要要素100%の出自・状態を確認できない。|
|HB-03|非該当|合成Q&Aを承認済み要求・正本・ベースラインとして扱っていない。|
|HB-04|非該当|安全・法規・契約の確定主張や、根拠なしの影響大数値は見当たらない。|
|HB-05|非該当|L6/L7の部品型番・公差・詳細実装の創作はない。|

## 重大Finding

|finding_id|severity / type|evidence|なぜ40点を阻害するか|最小修正案|requires_human|
|---|---|---|---|---|---|
|IR-SF-FND-0001|high / trace_gap|`SF-TR-01`〜`05`、Need候補表|Need→Requirementの根拠がIDで解決できず、要求の「なぜ」を確認できない。|Need表に`SF-NEED-01`〜`05`を明示追加し、各TraceでStakeholder→Need→RequirementをID参照する。|false|
|IR-SF-FND-0002|high / provenance_gap|`SF-BEH-01`〜`05`、`SF-STR-01`〜`04`、`SF-V-01`〜`05`|主要要素の出自・主張状態・判断状態が欠落し、候補と事実を同じ粒度で監査できない。|各Behavior／Structure／V&V候補に`origin: ai_context_inference`、`claim_state: assumed`、`decision_state: proposed`を付与する。|false|
|IR-SF-FND-0003|high / semantic_trace_gap|`SF-REQ-01`/`SF-BEH-01`、`SF-REQ-03`/`SF-BEH-03`|REQ-01の「運転モード」とBEH-01の手動・自動状態の範囲が不一致。REQ-03の静音モード選択経路・送風条件も未定義。|モード集合と遷移を候補として列挙し、静音モードを含めるかを人が選択した後、RequirementとBehaviorを同じ集合へ最小修正する。|true|
|IR-SF-FND-0004|medium / requirement_quality|`SF-REQ-03`、`SF-REQ-04`、`SF-V-02`、`SF-V-03`|REQ-04は停止と再開を束ね、REQ-03とV&Vは条件・尺度が曖昧。検証可能性を確定できない。|REQ-04を停止／再開へ分割する候補を提示し、音圧・風量・危険状態・停止時間・測定条件は数値を創作せず人が確定する。|true|

## 人の確認と日本語二層評価

`human_confirmation_required: true`。合成Q&Aは`ai_context_inference / assumed / proposed`であり、`user_confirmed`へ昇格できない。最低限、(1)カバー開放・接触時の適用規格と停止性能、(2)静音モードの音圧・風量・測定条件、(3)通信断時のローカル操作・認証責任、(4)電源方式・保守復帰・タイマー条件を確認する。

|層|判定|理由|
|---|---|---|
|`linguistic_quality`|`weak`|文の主語・動詞は概ね明確だが、「必要な送風」「静音モードで定義した送風条件」「規定した危険状態」などの定義・尺度がない。REQ-04は複数義務を束ねる。|
|`semantic_validity`|`unknown_with_reason`|入力が実利用者の回答ではなく合成回答で、性能値・安全分類・法規適用・受入れ尺度の根拠がない。文章が整っていても工学的妥当性は確定できない。|

## 判定上の注意

本レビューは承認、設計承認、規格適合、安全認証、ベースライン化を意味しない。上記の最小修正と人の確認後、同じGate版で再評価する。
