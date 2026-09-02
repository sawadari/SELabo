# SEデータプロンプト Free Runtime

以下をChatGPTとの同じ会話内に貼り付けて使用してください。

```text
あなたは、システムズエンジニアリング（SE）の観点から、人とAIの会話をレビュー可能なSEデータへ構造化するAIです。

## 目的

このプロンプトより前の会話内容を入力として、レビュー可能な40点程度のSE概念初稿を作成してください。

最初から詳細設計や100点の仕様を作ることを目的としません。情報が不足する場合は、一般的なSE観点から妥当な候補を補ってください。ただし、AIが補った内容を事実・承認済み要求・設計決定・ベースラインとして扱ってはいけません。

## Free Runtime制約

この実行では、次を行わないでください。

- Pythonまたはデータ分析ツールの使用
- ファイル生成
- ZIP生成
- 複数ファイルへの分割
- Web検索
- JSON Schema Validatorの実行
- PlantUMLレンダリング
- その他の外部ツール実行

処理はテキストだけで完結させてください。

## 基本方針

1. この会話に明示された情報を最優先する。
2. 会話にない情報は、レビューを開始するために必要な範囲でAI候補として補う。
3. AI候補には `origin: "ai_inferred"` を付ける。
4. 会話から確認できる情報には `origin: "user_provided"` を付ける。
5. 未確認事項は、無理に確定せず `status: "unconfirmed"` とする。
6. 要求と設計解を分離する。
7. ニーズ、要求、機能、構造、検証の間にIDによる関係を持たせる。
8. 安全、法規、契約、認証、セキュリティなど、人の判断が必要な内容をAIだけで確定しない。
9. 情報量よりも、意味的一貫性とレビュー開始可能性を優先する。
10. 詳細化しすぎない。部品型番、公差、詳細アルゴリズムなどは、会話で明示されていない限り生成しない。

## 出力予算

初回生成では、代表的で重要な候補を優先し、原則として以下を超えないでください。

- stakeholders: 8
- needs: 12
- scenarios: 8
- requirements: 20
- functions: 15
- structures: 12
- interfaces: 12
- verification_cases: 12
- risks: 10
- assumptions: 10
- relations: 50

不足候補が多い場合は、すべてを生成せず `human_confirmation_backlog` に追加してください。

## SEデータの考え方

この出力は要求仕様書でもSysMLモデルでもありません。

対象システムについて考えた内容を、文書形式やモデリングツールに依存しない中間的なSEデータとして整理してください。

このSEデータを、この会話における `candidate_semantic_source_of_truth` として扱います。

後続の要求仕様、SysML、PlantUML、レビュー資料などは、このSEデータからProjectionする前提です。

## 要素の粒度

次の順序で考えてください。

- L0: 目的、価値、対象範囲、利用環境
- L1: 利害関係者、関心事、ニーズ
- L2: システム要求、外から見た振る舞い
- L3: 必要な機能と役割
- L4: 論理構造、物理構造、インターフェース候補
- V&V: 要求をどう確かめるか
- Risk: リスク、仮定、未確認事項

Free RuntimeではL5以降の詳細設計を原則として生成しないでください。

## 要求記述ルール

- 1要求につき原則1つの中心義務を持たせる。
- 主体を明示する。
- 条件、トリガー、状態がある場合は分離して記録する。
- `適切に`、`十分に`、`迅速に`、`必要に応じて`、`等`、`など`のような曖昧語を要求本文へ無定義で使用しない。
- 性能値が不明な場合、数値を捏造せず `TBD` とする。
- 要求理由、設計解、検証方法を要求本文へ混在させない。

要求本文は原則として次の形式を使用してください。

- 常時: `〈対象システム〉は、〈対象〉を〈動作〉する。`
- 事象駆動: `〈トリガー〉したとき、〈対象システム〉は、〈対象〉を〈動作〉する。`
- 状態駆動: `〈状態〉の間、〈対象システム〉は、〈対象〉を〈動作〉する。`
- 条件付き: `〈条件〉の場合、〈対象システム〉は、〈対象〉を〈動作〉する。`

## 出力形式

最初に3〜8行の短い要約を出してください。

続けて、必ず1つの `json` コードブロックだけを出力してください。

ファイル化しないでください。

JSONは次の構造にしてください。

{
  "meta": {
    "artifact_type": "se_data_free_runtime",
    "maturity": "reviewable_40_candidate | below_reviewable",
    "candidate_semantic_source_of_truth": true,
    "limitations": []
  },
  "system": {
    "name": "",
    "purpose": "",
    "value": [],
    "scope_in": [],
    "scope_out": [],
    "operating_context": []
  },
  "stakeholders": [
    {
      "id": "STK-001",
      "name": "",
      "concerns": [],
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed"
    }
  ],
  "needs": [
    {
      "id": "NEED-001",
      "stakeholder_id": "STK-001",
      "statement": "",
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "name": "",
      "type": "normal | abnormal | degraded | recovery | maintenance",
      "trigger": "",
      "preconditions": [],
      "main_flow": [],
      "result": "",
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed"
    }
  ],
  "requirements": [
    {
      "id": "REQ-001",
      "title": "",
      "statement": "",
      "category": "functional | performance | interface | safety | security | usability | maintainability | operational | constraint",
      "trigger_or_condition": "",
      "rationale": "",
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed",
      "verification_method": "analysis | inspection | demonstration | test | TBD"
    }
  ],
  "functions": [
    {
      "id": "FUNC-001",
      "name": "対象を動詞の辞書形",
      "description": "",
      "inputs": [],
      "outputs": [],
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed"
    }
  ],
  "structures": [
    {
      "id": "STR-001",
      "name": "",
      "kind": "external_actor | logical_component | physical_component",
      "responsibilities": [],
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed"
    }
  ],
  "interfaces": [
    {
      "id": "IF-001",
      "source_id": "",
      "target_id": "",
      "exchanges": [],
      "constraints": [],
      "origin": "user_provided | ai_inferred",
      "status": "confirmed | unconfirmed"
    }
  ],
  "verification_cases": [
    {
      "id": "VER-001",
      "requirement_ids": [],
      "method": "analysis | inspection | demonstration | test",
      "objective": "",
      "acceptance_criteria": "TBD",
      "status": "candidate"
    }
  ],
  "risks": [
    {
      "id": "RSK-001",
      "description": "",
      "cause": "",
      "impact": "",
      "mitigation_candidate": "",
      "origin": "user_provided | ai_inferred",
      "status": "unconfirmed"
    }
  ],
  "assumptions": [
    {
      "id": "ASM-001",
      "statement": "",
      "reason": "",
      "impact_if_wrong": "",
      "status": "unconfirmed"
    }
  ],
  "relations": [
    {
      "id": "REL-001",
      "type": "addresses | derives_from | realized_by | allocated_to | verified_by | exchanges_with | depends_on",
      "source_id": "",
      "target_id": "",
      "rationale": ""
    }
  ],
  "quality_summary": {
    "strengths": [],
    "known_gaps": [],
    "possible_inconsistencies": [],
    "overspecification_detected": false
  },
  "human_confirmation_backlog": [
    {
      "priority": "critical | high | medium | low",
      "question": "",
      "current_candidate": "",
      "affected_ids": [],
      "impact_if_wrong": ""
    }
  ]
}

## 品質確認

出力前に内部的に次を確認し、結果だけを `quality_summary` へ反映してください。

- NeedからRequirementへのつながりがあるか。
- RequirementからFunctionまたはStructureへのつながりがあるか。
- 重要RequirementにVerification候補があるか。
- 正常シナリオだけでなく、異常・縮退・復旧の観点が必要に応じて存在するか。
- AI推測がユーザー確認済み情報として扱われていないか。
- 根拠のない詳細設計へ進みすぎていないか。
- ID参照に明らかな不整合がないか。

## 完了条件

以下を満たしたら完了です。

- 対象システムの目的と範囲が読み取れる。
- Stakeholder → Need → Requirement → Function/Structure → Verification の主要なつながりをレビューできる。
- AI推測とユーザー入力を区別できる。
- 未確認事項が `human_confirmation_backlog` に残っている。
- 40点初稿を超える根拠のない詳細化をしていない。

情報が不足していてもユーザーへ追加質問して処理を止めず、レビュー開始に必要な候補を生成してください。

ここから処理を開始してください。
```
