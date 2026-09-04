# AI Applicability, Bottleneck & Offering Patterns

## 1. AI Necessity Gate

AI適用を前提にしない。

次の順に確認する。

```text
Process / Role / Rule改善で十分か
        ↓
決定論的Automationで十分か
        ↓
既存Engineering Toolで十分か
        ↓
Native AIで十分か
        ↓
Customer AIが必要か
        ↓
Custom AIが必要か
```

No-AIが最適なら、それを結論候補として扱う。

---

## 2. AI適用Pattern

### A1 Extract
文書・表からRequirement、Parameter、Assumption、Variant等を抽出。

### A2 Review
曖昧性、Missing、Contradiction、Rule違反、Model品質を確認。

### A3 Retrieve
過去Requirement、Change、Design、Test、Evidenceを検索。

### A4 Relate / Graph
Requirement→Function、Change→Impact、Requirement→Test等の関係候補。

### A5 Generate Candidate
Requirement、Model、Test、Scenario、Script、Report等の候補生成。

### A6 Analyze / Reason
Impact、Gap、Risk、Consistency、Coverageの分析。

### A7 Predict / Surrogate
CAE/MBDの代理予測。

### A8 Optimize / Explore
Design space探索、多目的最適化、Candidate ranking。

### A9 Execute / Agent
Tool操作、Simulation実行、Issue作成等。

---

## 3. Authority Boundary

### L0 Read / Support
Search、Summary、Draft。
Humanが全面確認。

### L1 Engineering Candidate
Requirement、Impact、Test、Model候補。
Evidence/Reviewを要求。

### L2 Engineering Action
Tool実行、Simulation、Issue作成、変更案作成。
Human Approvalを要求。

### L3 Authoritative Change
Baseline、Released BOM、Safety criteria、Production設定等。
AI単独変更は原則不可。
Configuration、Approval、Auditを要求。

---

## 4. Bottleneck Migration Pattern

| AI/Automation対象 | まず減る作業 | 次に起こりやすいPain |
|---|---|---|
| Requirement生成 | Draft作成 | Context、合意、Review、Trace |
| Requirement Review | Check作業 | False positive、Decision criteria |
| Trace生成 | Link作成 | Semantic correctness、重要Link選別 |
| Impact分析 | 探索 | False negative、重要度、採否Decision |
| Test生成 | Case作成 | Oracle、Coverage、優先順位 |
| Test実行 | Execution | Test-space設計、Triage |
| Model生成 | Modeling | Consistency、Purpose、Credibility |
| CAE高速化 | 計算待ち | Design space、Uncertainty、Trade-off |
| RAG | Search | Applicability、Freshness、Rationale |
| Tool Agent | 操作 | Failure recovery、Authority、Version、Owner |
| Digital Thread | 情報取得 | SoR、Semantic、Write-back、Governance |

---

## 5. Offering Pattern

Offeringは固定製品ではなく、Actionable Root Painに応じたSolution Patternとして扱う。

### O0 Engineering Decision & Bottleneck Assessment
対象：
全案件の入口。

内容：
Current Bottleneck、Decision、Pain、KPI、Data/Tool、AI necessity、Projected Bottleneckを特定。

### O1 Requirements & Intent Intelligence
主Pain：
F1/F2/F3/F15

内容：
Requirement構造化、Intent/Rationale、曖昧性/Missing Review、Context、Trace候補。

### O2 Change Impact & Consistency Intelligence
主Pain：
F5/F6/F8

内容：
Change Impact、Semantic Diff、Stale artifact、Re-verification候補、Decision evidence。

### O3 Variant & Configuration Intelligence
主Pain：
F5/F7/F8/F10

内容：
Feature/Variant、Rule、Core asset、Configuration、Regression scope。

### O4 Verification & Scenario Intelligence
主Pain：
F2/F3/F6/F10/F18

内容：
Requirement-to-Test、Scenario、Boundary、Coverage gap、Regression selection、Evidence。

### O5 Model & Simulation Decision Acceleration
主Pain：
F11/F12/F13/F19

内容：
Model credibility、Surrogate、DOE、Optimization、Trade-off、Calibration、Feedback。

### O6 Engineering Data & Model Flow
主Pain：
F4/F6/F8/F14/F20

内容：
SoR、ID、Version、Semantic、Cross-tool relation、API/Adapter、Model flow。

### O7 Engineering AI Assurance & Agent Governance
主Pain：
F18/F21

内容：
Evaluation、Golden set、Human approval、Access、Regression、Audit、Agent authority。

### O8 Method / Process / Adoption Engineering
主Pain：
F15/F16/F17/F21

内容：
Guideline、Process tailoring、Training、Review method、Tool/Agent development governance。

### O9 Cross-domain Design Coordination
主Pain：
F4/F5/F12/F19

内容：
Dependency、Design parameter coordination、System budget、Trade-off、Decision convergence。

---

## 6. Offering Bundle例

### Testが多い
原因により変える。

- Variant原因：O3 + O4
- Change原因：O2 + O4
- Requirement原因：O1 + O4
- Model credibility原因：O5 + O4 + O7

### Change Impact
O2 + 必要に応じてO6 + O4。

### AI Test
O1 + O4 + O7。
Test生成単体で終わらせない。

### AI×CAE
O5 + O7。
実測Feedbackが弱ければO6またはData整備も含める。

### Engineering Agent
O6 + O7 + O8。
Agentだけを単体導入しない。

### MBSE導入/高度化
O0 + O9 + O8。
必要なDecision use caseに応じてO1/O2/O4/O5/O6を追加。
