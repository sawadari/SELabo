# Engineering Pain Causal Model

## 1. 位置づけ

本ファイルは顧客事実を記載した資料ではありません。

日本の開発事例・方法論・MBD/MBSE/要求/派生/Test/CAE/品質/Process/AI事例から一般化した、
顧客Discovery用の仮説生成・因果診断Knowledgeです。

個別顧客へ適用する際は、必ず会話で検証してください。

---

# 2. Engineering Pain Family

## L1 Intent / Value

### F1 Goal / Value / Target Deployment
顧客価値・事業目標・製品KPIをSystem/Subsystem/Componentへ根拠付きで展開できない。

### F2 Requirement Scope / Meaning
要求の範囲・意味・理由・前提が関係者間で一致しない。

### F3 Quality / Non-functional / UX
性能、保守性、使いやすさ、安全、Security等の品質属性が後付けになる。

## L2 Structure / Boundary / Variability

### F4 Boundary / Interface / Agreement
組織・企業・Domain境界で意味、責任、Assumptionが失われる。

### F5 System Architecture / Ownership
System全体構造とSystem-level Ownerが弱く、局所最適やArchitecture劣化が起きる。

### F7 Derivative / Variant / Reuse
派生・Variant・Core assetの共通性、差分、Reuse条件を管理できない。

### F20 Lifecycle / Transition / Operation
移行、運用、保守、停止可能時間、廃止等のLifecycle制約を上流設計へ入れられない。

## L3 Knowledge / Data / Process Infrastructure

### F14 Data / Tool / Interoperability
Tool、Data、企業境界が分断され、Engineering contextが流通しない。

### F15 Knowledge / Skill / Rationale
設計意図、判断観点、Reasoning、Know-howが個人依存する。

### F16 Process / Method / Adoption
手法・Processを本質理解し、現場へTailor・定着・横展開できない。

### F21 Engineering Environment / Automation Quality
Simulation、Script、内製Tool、Agent等の実行環境自体が新しい技術負債になる。

## L4 Propagation / Coordination

### F6 Change Impact / Trace
変更が何へ波及し、何を再確認すべきかを絞れない。

### F8 Cross-artifact Consistency / Configuration
Requirement、Model、Code、Test、BOM等のVersion・SoR・同期が崩れる。

### F19 Cross-domain Coordination / Design Suri-awase
複数Domainが並行設計する中で、値・制約・性能Budgetを継続的にすり合わせられない。

## L5 Evaluation / Verification

### F9 Review / Decision Quality
Reviewで何を判断し、どこまでなら十分か、最適案かを評価できない。

### F10 Verification / Test Design
Scenario、Coverage、Test範囲、Oracle、Regressionを決められない。

### F11 Model / Simulation Credibility
Modelの粒度、精度、Context、適用範囲をどこまで信用できるか判断できない。

### F12 Trade-off / Feasibility / Uncertainty / Optimization
複数案、多目的、不確定性を扱いながら成立性を早期判断できない。

### F13 Observability / Feedback / Root Cause
実測・市場・運用Dataが不足し、原因特定や現実からModel/設計へのFeedbackが弱い。

## L6 Management / Assurance

### F17 Work Management / Metrics / Incentives
進捗、工数、KPI、目標管理が重く、誤った指標が局所行動や疲弊を生む。

### F18 Assurance / Authority / Governance
誰が何を信用し、どのEvidenceで承認し、正本へ反映するかが曖昧。

---

# 3. 主要因果関係

```text
F1 → F2
F1 → F12

F2 → F4
F2 → F5
F2 → F9
F2 → F10

F3 → F5
F3 → F10
F3 → F18

F4 → F19
F4 → F14
F4 → F18

F5 → F6
F5 → F7
F5 → F19
F5 → F12

F7 → F6
F7 → F8
F7 → F10

F14 → F8
F14 → F6
F14 → F21

F15 → F2
F15 → F5
F15 → F9

F16 → F15
F16 → F21

F20 → F5
F20 → F10

F19 → F6
F19 → F9
F19 → F12

F6 → F8
F6 → F9
F6 → F10

F8 → F9
F8 → F10
F8 → F18

F13 ↔ F11

F11 → F10
F11 → F12
F11 → F18

F12 → F9

F21 → F9
F21 → F10
F21 → F18

F9 → F17
F10 → F17
F10 → F18
```

これは統計的因果推定ではありません。
複数事例で反復したEngineering mechanismをDiscovery用にモデル化したものです。

---

# 4. 症状からの主な分岐

## 「Testが多すぎる」

直接：F10

上流候補：

- F7 Variant
- F6 Change Impact
- F2/F3 Requirement / Quality
- F11 Model Credibility
- F20 Operational Scenario

## 「Review指摘が多い」

直接：F9

上流候補：

- F2 Requirement不足
- F3 Non-functional不足
- F15 Expert観点依存
- F8 Version/Consistency

## 「変更影響が分からない」

直接：F6

上流候補：

- F5 Architecture
- F7 Variant
- F14 Data/Tool分断
- F15 Rationale不足

## 「ベテランがいないと止まる」

直接：F15

次に確認：

- Requirement観点か
- Architecture判断か
- Review観点か
- Risk/Trade-off判断か

## 「Toolがバラバラ」

直接：F14

本当の困り事候補：

- Search
- Sync
- Impact
- Configuration
- Automation maintenance
- Authority

## 「Modelはあるが使われない」

直接：F16

上流/周辺候補：

- F1 Decision use case不明
- F15 Reviewer/Modeler依存
- F14/F8 他Toolとの分断
- F21 更新・自動化負荷

## 「Simulation結果を信用できない」

直接：F11

関連：

- F13 Observability
- F10 V&V
- F18 Acceptance / Evidence

## 「派生が増えて回らない」

直接：F7

下流：

- F6 Impact
- F8 Configuration
- F10 Regression

## 「部署間すり合わせ会議が多い」

直接：F19

上流：

- F4 Boundary
- F5 Architecture

下流：

- F12 Trade-off
- F9 Decision

## 「AI PoCは動いたが本番化できない」

直接：F18

上流候補：

- F14/F8 Data/SoR
- F16 Process
- F21 Agent/Tool quality
- F15 Reviewer skill
- Acceptance criteria不足

---

# 5. Actionable Root Pain

原因を無限に遡らない。

以下を満たす地点をActionable Root Pain候補とする。

1. 改善すると複数の下流症状が軽減する
2. 顧客の当該Capability Cellで変更可能
3. Before/Afterを測定できる
4. PoC/Offeringへ具体化可能
