# Engineering Case Pattern Library

> 使用上の注意：
> 本資料のケースは、現在顧客の事実を推定するためのデータではない。
> 類似Patternの想起、仮説の漏れ確認、ヒアリング質問候補の生成にのみ使用する。
> 個別企業名・具体事例を、ユーザーが明示的に求めない限りChat出力へ出さない。
> Caseから導く内容は `analogical_hypothesis` として扱い、会話で検証する。

---

# 日本の開発現場 Engineering Pain Library v4
## Source Graph Explorationによる116匿名ケース・21 Root Pain

- 作成日：2026-09-04
- 対象：日本の製造業・組込み・制御・ソフトウェア・複雑システム開発
- 分析単位：企業ではなく **Capability Cell**
- 目的：AI×MBSE事業で使う顧客課題仮説を、年代・技術・方法論を越えて反復するRoot Painから構築する

> 本資料は統計的な市場発生率調査ではない。公開された導入事例・失敗事例・研究活動から、Painの種類、因果構造、自動化後のBottleneck Migrationを抽出する質的Evidence Libraryである。

# 1. 今回のResearch Expansion

前版まではDrive文献を中心に読んでいたが、今回は各文献の**出所を探索Hubとして展開**した。

IPA/SECについては2013～2017年度の個別事例ページを辿ることで、2017年度版の分類表が過去事例を含む**93件**を網羅していることを確認した。AFFORDDは2010～2026のカンファレンスとT01～T23の研究テーマへ展開し、SQiP、JMAAB、JAMA/JAMBE、自動車技術会まで追加した。

# 2. Source Graph

| Source family | Time range | 主に取得できるPain | 調査上の価値 | URL |
|---|---|---|---|---|
| IPA/SEC 先進的設計・検証事例 | 2013/2015/2016/2017 + 横断分析 | 要求、MBD/MBSE、派生、Variant、Test、UX、Safety、Process、認証 | 93件を俯瞰できる中核母集団 | https://www.ipa.go.jp/archive/digital/iot-en-ci/jirei/index.html |
| IPA/SEC 適用分析 | 58件横断分析 | 現場課題→適用技術/手法の紐付け | Pain taxonomy検証に特に有用 | https://www.ipa.go.jp/archive/publish/secbooks20160511.html |
| AFFORDD | 2010-2026資料ライブラリ | USDM、XDDP、SPL、Spec-out、失敗、Process設計、AI | 成功だけでなく失敗・定着を追える | https://affordd.jp/libraries/ |
| SQiP | 2004-2025年度成果報告 | 要求、Review、Test、Process、AI品質、人材 | 品質活動とAI後の新ボトルネック | https://www.juse.or.jp/sqip/workshop/report/2025.html |
| JMAAB | 2024-2026 | MBD、Plant、内製Tool、Requirement-Model、Agile、生成AI | 現在のMBD現場のBottleneck migration | https://jmaab.jp/joc2025/ |
| JAMA/JAMBE | 2019-2025 | OEM/Tierモデル流通、FMI、Plant I/F、共有Hub | 企業間Digital Thread/Interoperability | https://www.jambe.jp/system/download |
| 自動車技術会/J-STAGE | 継続 | MBD、Calibration、CAE、Scenario、官能/AI | 最新の技術ボトルネックを追跡 | https://www.jstage.jst.go.jp/browse/jsaeronbun/ |
| 企業技報アーカイブ | 継続 | 構想設計、CAE、品質、Front-loading、System design | 従来Processの具体Painが得やすい | 各社技報アーカイブ |

# 3. 今回のResearchで強化された仮説

## 3.1 Root Painはかなり安定している

要求、派生、Model、Test、Process、企業間連携について10年以上離れた事例を比較しても、根本問題は「意味」「影響」「整合」「判断」「検証」「知識」「責任」に収束する。

## 3.2 自動化するとPainは『作業』から『判断』へ上がる

```text
Artifactを作れない
  ↓ 自動化
Artifactを大量に作れる
  ↓
どれが正しいか / 必要か
  ↓
どれを採用するか
  ↓
誰が承認するか
  ↓
変更後も正しいか
```

## 3.3 現在のAI研究も同じ方向へ移っている

現在のSQiP/JMAABでは、AIによるReview/Test/Model生成そのものと同時に、観点粒度、信頼性評価、Human responsibility、機能安全/SPICE、AI-readable data、Reviewer knowledge継承がテーマになっている。

# 4. 116ケース台帳

| ID | Root Pain | 現場文脈 | 観測された困り事 | より深い構造 | 自動化後に移るボトルネック | Evidence |
|---|---|---|---|---|---|---|
| C01 | F2 Requirement Scope / Meaning | 要求仕様 | 中心仕様は書けるが周辺条件・例外・入力選択などが漏れる | 仕様漏れは『書き方』より要求が求める範囲を捉えられていないことから生じる | 要求構造化後は、要求間の整合・変更影響へボトルネックが移る | 添付: USDM要求仕様資料 |
| C02 | F2 Requirement Scope / Meaning | 要求仕様 | 同じ文書を渡しても、ドメイン知識や経験差によって受け手が同じ内容を特定できない | 仕様書の十分性は文書単体でなく『今回の関係者がSpecifyできるか』で決まる | 文書テンプレート整備後は、受け手別のContext・説明責任が課題になる | 添付: USDM要求仕様資料 |
| C03 | F4 Boundary / Interface / Agreement | OEM–サプライヤ連携 | 発注側と受注側で仕様の意味が一致せず、不具合が境界で混入する | 組織境界をまたぐ際にWhat/Why/Assumptionが失われる | ReqIF/API化しても意味合意・責任境界が残る | 添付: 自動車システムUSDM事例 |
| C04 | F2 Requirement Scope / Meaning | 要求レビュー | 仕様FIXを急ぐが、何を確認すべきか・何が不足か分からずレビューを繰返しても収束しない | 未成熟な要求を日付で凍結しても合意は成立しない | レビュー自動化後は『合意可能状態』の判定が課題になる | 添付: USDM要求仕様資料 |
| C05 | F3 Quality / Non-functional / UX | 非機能要求 | 機能要求は書けるが、保守性・使いやすさ・テスト容易性等が明文化されず後工程で問題化 | 品質属性は複数要素の構造設計に影響するため機能単位だけでは扱えない | 機能生成が速くなるほど品質属性設計が支配的になる | 添付: USDM・アジャイル設計資料 |
| C06 | F15 Knowledge / Skill / Rationale | 先行・制御開発 | 最終仕様やモデルは残るが、なぜその制御方式になったかという設計意図が暗黙知になる | 試行錯誤のDecision/Rationaleが成果物から脱落する | AI生成後は『なぜ採用したか』の証跡がさらに重要になる | 外部: AFFORDD経験発表 |
| C07 | F3 Quality / Non-functional / UX | 製品開発 | 高機能・高性能化を優先し、実利用時の使い勝手やUXが後付けになる | 技術KPIとユーザー価値KPIが開発プロセス上分離している | 性能最適化後に利用品質・人間系がボトルネック化 | 外部: IPA HCD/UX事例 |
| C08 | F1 Goal / Value / Target Deployment | 構想設計 | 製品目標をユニット・部品目標へ展開する工程が経験・英知に大きく依存 | 全体性能から部分要求への配分は単純な分解ではなくTrade-offを含む設計判断 | 詳細CAEが高速化しても目標設定・配分が上流ボトルネックとして残る | 添付: 構想設計Virtual Testing事例 |
| C09 | F1 Goal / Value / Target Deployment | システムサプライヤ開発 | 自社サブシステムの目標達成に終始し、車両/上位システム全体への価値・寄与を説明できない | 局所KPI最適化とシステム価値の間にギャップがある | 部品設計最適化後にSystem-level Value Propositionがボトルネック化 | 添付: 車両性能シミュレーション事例 |
| C10 | F2 Requirement Scope / Meaning | 新規システム | 要求仕様と構想設計が絡み合い、仕組みが分からない段階では正確な仕様を書けない | 要求は設計から完全独立ではなく、Architecture探索で具体化される | AIで仕様生成してもArchitectureとの反復が必要 | 添付: MBSEプロセス論文 |
| C11 | F5 System Architecture / Ownership | 組織横断開発 | 長年の派生・部品別効率化でシステム全体設計者が育たず、新規システム時に統合判断できない | 局所専門化がSystem Ownershipを失わせる | 各部門自動化が進むほど横断Integration authorityが重要 | 添付: MBSEプロセス論文 |
| C12 | F6 Change Impact / Trace | 派生開発 | 変更の影響範囲を誰が・どう特定するか具体的方法がなく、解析ツールだけでも足りない | 影響は静的依存だけでなく意図・挙動・設計方式に依存する | Graph自動化後は関係の意味・重要度判定が課題になる | 添付: モデル主体派生開発ガイド |
| C13 | F6 Change Impact / Trace | トレーサビリティレビュー | 細粒度TMを作れるようになったが巨大化し、セルフチェックやレビューでも漏れを見つけられない | Traceの存在とChange Decisionの品質は別問題 | Trace自動生成後は『どのTraceを見るべきか』がボトルネック化 | 添付: TMレビュー事例 |
| C14 | F9 Review / Decision Quality | 変更設計 | 変更箇所は分かっても、その変更箇所が最適か判断できず、How次第で影響範囲も変わる | Impact Analysisは設計案評価と不可分 | AI Impact候補後はArchitecture Decision比較が課題になる | 添付: TMレビュー事例 |
| C15 | F7 Derivative / Variant / Reuse | レガシー派生開発 | 既存ソフトの仕様・構造を把握するスペックアウトが属人化し、品質・効率がばらつく | 正本がコードに埋まり、意図・構造知識が失われている | LLM reverse engineering後は抽出結果の正しさ・構造化が課題 | 外部: AFFORDDスペックアウト事例 |
| C16 | F5 System Architecture / Ownership | 派生開発 | 機能追加を繰り返すうちにソフトウェアアーキテクチャが劣化し、部分開発では全体改善が困難 | 短期変更最適化が長期Architecture負債を生む | 変更自動化後はArchitecture fitnessが重要になる | 添付: モデル主体派生開発ガイド |
| C17 | F7 Derivative / Variant / Reuse | プロダクトライン | 共通資産を各チームが個別変更し、再利用・保守が困難になる | 共通性と個別最適のGovernanceがない | Variant生成が容易になるほど共通資産統制が重要 | 外部: IPA SPL/バリアント事例 |
| C18 | F3 Quality / Non-functional / UX | 派生開発 | 機能変更に集中し、性能・時間効率など非機能劣化を後段で発見する | Change Scopeが機能差分に偏りQuality Attribute影響を見落とす | Regression自動化後も何のQualityを監視するかが残る | 外部: IPA 派生開発性能劣化事例 |
| C19 | F10 Verification / Test Design | 回帰テスト | 短納期・多バリエーションで全回帰テストは不可能、絞り込みを誤ると欠陥流出 | Impact範囲とVerification範囲の対応が不十分 | 影響解析自動化後はCoverage sufficiencyがボトルネック | 外部: IPA 影響波及パス事例 |
| C20 | F7 Derivative / Variant / Reuse | 製品シリーズ | 多機種・派生を個別開発すると工数が製品数に比例し、品質もばらつく | Variation pointとCore assetが構造化されていない | 自動生成後はVariant rule/asset governanceが残る | 外部: IPA モデル指向SPL事例 |
| C21 | F8 Cross-artifact Consistency / Configuration | 設計全般 | トレーサビリティは効果を実感しにくく、現場が作成・維持したがらない | Trace作業が本来の設計判断から切り離されている | 自動Trace後はSemantic correctness/鮮度が課題 | 添付: 要求〜詳細設計アジャイル事例 |
| C22 | F8 Cross-artifact Consistency / Configuration | MBSE活用 | 異なる情報源間のやり取りで更新漏れ・伝達漏れが起き、相手ごとに資料を作り直す | Artifactが目的別に複製され同期コストが増える | Digital Thread後はview生成/authority管理が課題 | 添付: MBSE活用デモ |
| C23 | F10 Verification / Test Design | 組合せテスト | 要因組合せが増えテスト項目が爆発し、早期検出と工数削減を両立しにくい | 入力空間/状態空間の網羅性設計が必要 | AIテスト生成後はTest Oracleと優先順位が課題 | 外部: IPA 大量テスト事例 |
| C24 | F10 Verification / Test Design | 探索的テスト | 探索的テストは有効だが、総量・実施範囲が不透明で管理しにくい | 柔軟探索とCoverage/説明責任のトレードオフ | AI探索後はCoverage/Evidenceの可視化が必要 | 外部: IPA 探索的テスト事例 |
| C25 | F10 Verification / Test Design | MBD + AI | 機能テストやモデルを自動生成できても、生成物を何をもって正しいとするかが未解決 | Generation capabilityとVerification oracleは別能力 | AI普及でEvaluationが主ボトルネック化 | 外部: JMAAB 2025 AI活用WG + 現在議論 |
| C26 | F13 Observability / Feedback / Root Cause | 実機性能開発 | 試作・部品交換・計測を繰り返し高コスト。計測点制約で不具合時に原因データがなく前例踏襲・過剰品質になりやすい | 観測可能性不足がRoot Causeと最適化を阻害 | Virtual化後はモデル妥当性・実測Feedbackが課題 | 添付: 1DCAE性能開発事例 |
| C27 | F11 Model / Simulation Credibility | システムシミュレーション | モデル精度を追い求めるほど実務投入の判断が難しくなる | Model purposeと必要Fidelityの基準が曖昧 | Surrogate/AI導入後は適用範囲・不確実性管理が重要 | 添付: 車両性能シミュレーション事例 |
| C28 | F11 Model / Simulation Credibility | MBD導入 | サブシステムMBDは進むがシステム全体に適用されず、恩恵が局所に留まる | Plant/Environment/Interfaceモデルが不足しEnd-to-End検証できない | 局所自動化後にSystem Integrationがボトルネック | 外部: IPA Plant model事例 |
| C29 | F11 Model / Simulation Credibility | システム性能分析 | 詳細モデルを上位性能モデルへつなぐと計算時間が増え、粒度選択で悩む | 目的別Fidelity/Hierarchyの設計が必要 | HPC高速化後もモデル選択・抽象度の判断は残る | 添付: 車両性能シミュレーション事例 |
| C30 | F12 Trade-off / Feasibility / Uncertainty / Optimization | 構想設計CAE | 一般CAEは詳細諸元前提のため、構想段階の多数案検討にはモデル化負荷・計算負荷が大きい | 設計フェーズとModel fidelityが不整合 | 詳細CAE高速化後もConcept model設計が必要 | 添付: 構想設計Virtual Testing事例 |
| C31 | F14 Data / Tool / Interoperability | 企業間シミュレーション | モデルを渡す・貯める・ツール接続・環境共有のどれを選ぶか、企業間でモデル/データ授受が難しい | IP・Tool差・Format・Execution contextが境界を作る | 標準化後は権限・意味・モデル品質の共有が課題 | 添付: 拠点間連成シミュレーション資料 |
| C32 | F14 Data / Tool / Interoperability | Digital Engineering | 設計・生産のドメインごとにデータとツールが断片化し、企業間/ドメイン間のモデル流通が遮断 | LifecycleごとにSystem of RecordとSemanticが分断 | AI横断検索後はwrite-back/SoR/Versionが課題 | 添付: 拠点間連成シミュレーション資料 |
| C33 | F14 Data / Tool / Interoperability | 製造システム | 製造実行情報が多数組織にまたがり、情報が重複・乖離・欠落する | 同一事象が複数業務システム・組織視点で再表現される | 可視化後は共通意味/KPI/責任がボトルネック | 添付: 製造システムMBSE資料 |
| C34 | F17 Work Management / Metrics / Incentives | プロジェクト管理 | Excelガント・課題表・障害表が散在し、保守に時間がかかり状況把握とレビュー連携が遅い | 作業情報の分散と更新同期が管理負荷を生む | チケット化後は情報量/品質/意思決定が課題 | 添付: チケット駆動開発資料 |
| C35 | F17 Work Management / Metrics / Incentives | チケット管理導入後 | 可視化はできたが、チケット乱発・放置、どのメトリクスを意思決定に使うか、大規模展開が新課題 | Automation/visibilityが増えると情報選別・運用Governanceへ移る | AI AgentでIssue生成すると同型問題がさらに増幅し得る | 添付: チケット駆動開発資料 |
| C36 | F16 Process / Method / Adoption | 方法論導入 | フォーマットだけ導入し既存作業へ成果物を追加、指導者・レビュー能力がなく作業増・形骸化 | Methodの本質/Process designなしにArtifactだけ追加している | AIツール導入でも『既存ProcessにAI作業を追加』すると再発 | 添付: XDDP失敗事例研究 |
| C37 | F15 Knowledge / Skill / Rationale | 人材育成 | 有識者依存、トレーニング省略、社内アドバイザー育成軽視で展開・定着できない | Know-howが個人に閉じ、組織Capabilityへ変換されない | AI Tutor後もreviewer/authority skillが残る | 添付: XDDP失敗事例研究 |
| C38 | F16 Process / Method / Adoption | 大規模展開 | あるチームでは手法が機能しても、他部署では『今の成果物を変えたくない』『時間がない』『効果が分からない』で広がらない | 企業ではなく部署/案件ごとに前提・文化・Capabilityが異なる | 全社導入ではなくCapability Cell単位のTailoringが必要 | 外部: AFFORDD 組織展開事例 |
| C39 | F9 Review / Decision Quality | レビュー会議 | レビュー自体の目的・参加者役割・議論品質が不透明で、会議をしても品質保証になっているか分からない | Review processが形式化してもDecision criteriaが弱い | AI Review後はHuman reviewの目的/authority再設計が必要 | 外部: IPA Review可視化事例 |
| C40 | F15 Knowledge / Skill / Rationale | 品質改善 | 再発防止策・品質技術のストックがない/不十分で類似構造の不具合が再発する | Lessons learnedが適用可能条件付きKnowledgeとして再利用されない | AI検索後はApplicability判断と知識更新が課題 | 添付: 継続的品質改善事例 |
| C41 | F18 Assurance / Authority / Governance | 新技術導入 | 新技術の高度化で、目標達成リスク・日程/資源影響をプロジェクト移行前に判断する必要がある | 技術成立とProject readinessは別判定 | AI機能でもPerformance合格とProduction readinessを分離すべき | 添付: 品質リスクアセスメント事例 |
| C42 | F17 Work Management / Metrics / Incentives | 原価・QCD管理 | 厳格な目標管理がエンジニア疲弊や部門間コンフリクト、局所的な指標Gamingを生む | KPIは行動を変えるため、目標設計と責任分担自体がEngineering問題 | AI最適化後はObjective function設計がボトルネック | 添付: 原価企画運用事例 |
| C43 | F3 Quality / Non-functional / UX | 高機能製品 | 高性能・多機能化に注力する一方、使い勝手の問題が顧客/営業から顕在化する | Product qualityは機能適合だけではない | 機能生成自動化でUX/操作性などHuman qualityが相対的に重要 | 外部: IPA HCD事例 |
| C44 | F13 Observability / Feedback / Root Cause | デジタルツイン | 実測データとモデルを融合し、フィジカルへFeedbackすること自体が難しい | Model/real-world alignmentとData assimilationが必要 | Digital Twin構築後は閉ループの信頼性が課題 | 添付: デジタルツイン調査 |
| C45 | F14 Data / Tool / Interoperability | 開発環境 | 既存資産・性能・Security・環境保存等の制約で単純なクラウド移行/Tool統一が現実的でない | Enterprise Architectureはlegacy/operation constraintsを受ける | AI基盤追加時も同じ制約が再現する | 外部: IPA ハイブリッド開発環境事例 |
| C46 | F18 Assurance / Authority / Governance | 認証・高信頼開発 | 要求〜検証結果のTrace管理が複雑で正確性が必要、担当者間の情報伝達にもリスク | Certification evidenceは成果物生成とは別のManagement systemを要する | AI生成EvidenceにはProvenance/approval/versionが必要 | 外部: IPA 認証Trace事例 |
| C47 | F3 Quality / Non-functional / UX | 車載組込みソフトの派生開発 | 設計・実装レビューで「ソフトウェアの作り方」に関する指摘が多発し、作り直しと大きな遅延が発生する。共通チェックシートには一般項目しかなく、案件固有の非機能要求が抜ける。 | 一般的な品質ルールと、案件固有の制約・非機能要求を分離して上流入力にしないと、レビューが欠落要求の発見工程になる。 | 非機能要求を構造化すると、次は利用しやすい形式、業務ワークフロー、定量評価、制約分類がボトルネックになる。 | Drive追加文献：車載組込みソフトの非機能要求抽出事例 |
| C48 | F15 Knowledge / Skill / Rationale | 組込みシステムの上流設計 | 現行踏襲案件は回るが、新規要求が多い案件では手戻りが急増する。前提・制約、他ECUとの協調、モード切替などの要件化視点が不足しやすい。 | 詳細実装より上位の要件定義・アーキテクチャほどベテラン暗黙知への依存が大きく、分業・外注・短納期化でその能力が薄まる。 | AIで文書作成を補助しても、何を要件化するかという観点知識とレビュー能力が次の制約になる。 | Drive追加文献：組込み設計者向け要件定義ガイドライン事例 |
| C49 | F19 Cross-domain Coordination / Design Suri-awase | メカ・構造・電気・電子・ソフト並行設計 | 各詳細設計が並行して進む中、誰と何をすり合わせるべきかが暗黙知で、各設計結果がシステム全体へ与える影響を把握しにくい。 | 設計間の依存は単なるInterface一覧ではなく、性能値・制約・CAE結果が相互作用する動的な協調問題である。 | 依存関係をモデル化した後は、変更値の交渉、System budget再配分、設計案の合意形成がボトルネックになる。 | Drive追加文献：システム設計での設計すり合わせ技術 |
| C50 | F4 Boundary / Interface / Agreement | OEM–サプライヤ分散開発・新領域 | 自然言語だけでは設計意図が正しく伝わらず手戻りが生じる。一方、知財等の理由から発注側が全アーキテクチャを開示できない。 | 必要なのは「全情報共有」ではなく、相手が正しく判断できる最小十分Contextと、非開示境界を両立させる情報設計である。 | 共通モデルを導入すると、次に部分開示した情報の十分性、版、アクセス権、解釈責任が課題になる。 | Drive追加文献：分散開発とODD/SOTIF安全分析事例 |
| C51 | F7 Derivative / Variant / Reuse | 組込み製品群の妥当性確認 | 商品群で共通部とバリエーション部が混在し、限られた期間ですべてを同じ強度で検証できない。 | Core assetとVariation assetではリスクと変更頻度が異なるため、Validation strategyも同一にしてはいけない。 | Variant管理を自動化すると、次はリスクに応じたTest allocation、再利用した安全対策の適用条件が課題になる。 | Drive追加文献：組込み商品群の妥当性確認・プロダクトライン事例 |
| C52 | F15 Knowledge / Skill / Rationale | 過去不具合・未然防止 | 過去トラブルDBは蓄積されていても、設計者が次の設計に使える知識として検索・適用できない。 | 事象記録を、原因・設計原則・適用条件・文脈まで一般化しなければ、検索できても再利用可能な設計知識にはならない。 | AI検索が容易になると、次は「この案件に適用してよい知識か」というApplicability判断と知識更新がボトルネックになる。 | Drive追加文献：障害未然防止のための設計知識整理ガイド |
| C53 | F16 Process / Method / Adoption | SysML/MBSE導入 | モデルを作ること自体が目的化し、モデル量が増える一方で、レビュー・安全分析・再利用など本来の利用目的が曖昧になる。 | モデリングは目的ではなく、コミュニケーション・分析・再利用など特定Decisionを改善するための手段である。 | AIでモデル生成が高速化すると、「何をモデル化しないか」「どのViewがDecisionに必要か」がより重要になる。 | Drive追加文献：高信頼ロボットのSysML適用事例 |
| C54 | F12 Trade-off / Feasibility / Uncertainty / Optimization | 構想・初期設計 | 複数の性能・価格・重量・機構・制御など背反目標があり、初期案の実現性を素早く判断しながらも、早すぎる一点収束を避けたい。 | 初期設計では設計解・性能目標とも不確定であり、一点の最適化より設計空間と成立範囲を保持する必要がある。 | 探索を自動化すると、次は不確定性の表現、探索空間の妥当性、候補を捨てる判断基準がボトルネックになる。 | Drive追加文献：ポイントベース設計とセットベース設計の比較 |
| C55 | F14 Data / Tool / Interoperability | 企業間モデル流通 | 渡すべき情報内容が定義されず、メール/共有サーバ等の授受方法も統一されず、受領モデルは階層・粒度差で連成実行できない。 | モデルファイルだけでは不十分で、利用目的、実行条件、親子関係、履歴、関連要求等のContextを一緒に交換する必要がある。 | 共通Package化すると、次は履歴、再送時ID、編集可否、構造保持、承認、Securityが課題になる。 | Drive追加文献：OEM–サプライヤ間の電子制御情報流通事例 |
| C56 | F18 Assurance / Authority / Governance | 標準化後のモデル流通 | 共通パッケージでモデルと関連情報を交換できても、責任者承認、企業固有情報、履歴、ID、編集権限、Securityが不足して実務化しきれない。 | Interoperabilityの成立と、Authoritative engineering workflowの成立は別問題である。 | Data exchangeが自動化すると、誰が正本を書き換えられるか、どのEvidenceで承認するかが主ボトルネックになる。 | Drive追加文献：企業間モデル流通プロトタイプ評価 |
| C57 | F18 Assurance / Authority / Governance | 既存システムへの新機能追加・安全分析 | 各部品が故障していなくても、既存システムと新機能の協調動作によって想定外のHazardが生じ得る。 | 安全性は部品信頼性の合計ではなく、Control/Interaction/Contextの不適切さから創発する。 | Safety分析を支援AIで高速化すると、解析境界、安全制約、Unknown-unknownの扱いと承認が課題になる。 | Drive追加文献：ACC追加時のSTAMP/STPA適用事例 |
| C58 | F18 Assurance / Authority / Governance | 組込み安全設計 | 『信頼性が高ければ安全』と捉えられたり、『絶対安全』を前提に議論され、合理的なリスク判断ができない。 | 安全は残存リスクを利便性・経済性・使用環境と比較して許容可能域へ抑えるDecisionであり、Reliabilityとは異なる。 | AI導入後も、許容リスク基準、Residual risk受容者、Safety authorityは自動化できない。 | Drive追加文献：組込み系技術者向け安全設計ガイド |
| C59 | F11 Model / Simulation Credibility | 構想段階の信頼性設計 | 信頼性Simulationには形状・環境条件が必要だが、構想段階では詳細形状が未確定。それでも性能・コスト・信頼性を早期Trade-offしたい。 | 詳細モデルがない段階では、設計目的に合わせた抽象モデル、統計/DOE、条件規格化が必要となる。 | サロゲート化すると、次はモデルの適用範囲、入力範囲外、保証マージンが課題になる。 | Drive追加文献：屋外機器の構想段階信頼性予測事例 |
| C60 | F1 Goal / Value / Target Deployment | 感性・快適性を含む製品開発 | 『静かで快適』など顧客価値を、製品目標、ユニット目標、コンポーネント特性へ根拠付きで落とし込む必要がある。 | 主観的価値と物理量の間に因果鎖を作り、Benchmark・市場利用実態と結び付けなければ目標値の正当性を説明できない。 | AIで顧客声を分析した後は、Value→Engineering KPI変換と目標配分の妥当性がボトルネックになる。 | Drive追加文献：船外機の音開発MBD事例 |
| C61 | F21 Engineering Environment / Automation Quality | CAE/Simulation実行環境 | 設計者がSimulationを使いたくても、前処理・メッシュ・計算操作が重く、失敗・発散も多く、専門Tool操作と解析Know-howが障壁になる。 | モデル理論だけでなく、再現性あるExecution pipeline、前処理品質、Failure recoveryまで含めてEngineering environmentを設計する必要がある。 | Agentで操作を自動化すると、次はAgentが失敗を正しく検知・回復できるか、Tool更新に追随できるかが課題になる。 | Drive追加文献：カーエアコン基本性能の仮想設計事例 |
| C62 | F11 Model / Simulation Credibility | 部品ベンチ→実車/実システム適用 | ベンチでは均一条件で性能が出ても、実搭載時は周辺部品・Layoutにより境界条件が不均一になり性能が変わる。 | Component modelの精度だけでなく、Installation context/EnvironmentのFidelityがSystem performanceを支配する。 | Digital Twin化すると、次は実環境Contextの更新、観測、モデル反映の閉ループ品質が課題になる。 | Drive追加文献：実搭載状態の性能予測事例 |
| C63 | F1 Goal / Value / Target Deployment | 成熟製品の新規サービス企画 | 既存製品の性能改善だけでは市場成長が見込めず、一段上の業務・ステークホルダ視点から新しい利用価値を探索する必要がある。 | Engineering problemを解く前に、Business/Mission levelで『何を価値とするか』を再定義する必要がある。 | AIによるアイデア生成後は、Stakeholder value、Business viability、Engineering feasibilityの統合判断が課題になる。 | Drive追加文献：成熟製品から新サービスを創出したSE事例 |
| C64 | F20 Lifecycle / Transition / Operation | 大規模インフラ更新 | 新システム自体の機能だけでなく、既存システムからの移行、運用、試験可能時間、将来世代まで見通さないと導入できない。 | Lifecycle transitionとOperation constraintは後工程の実装課題ではなく、上流Architecture/Requirementの入力である。 | 設計自動化後も、移行順序、停止可能時間、Fallback、運用組織との合意が主ボトルネックとして残る。 | Drive追加文献：高密度輸送制御システムの段階更新事例 |
| C65 | F18 Assurance / Authority / Governance | 接続範囲が拡大する情報システム | 紙/単独システムを電子化・連携すると利用価値が増える一方、扱う情報・関係者・脅威範囲が拡大しSecurity要求が急増する。 | Connectivityは機能価値とAttack surfaceを同時に広げるため、System boundary拡大に合わせてTrust boundaryを再設計する必要がある。 | AI/Agent連携を追加すると、権限委譲、データ最小化、監査、第三者接続が新たなボトルネックになる。 | Drive追加文献：複数組織をつなぐ情報システムのSecurity設計事例 |
| C66 | F5 System Architecture / Ownership | 複数製品・車種への技術展開 | 車種・機能ごとの個別最適では優れた技術を全ラインナップへ効率展開できず、共通Architectureと全体最適が必要になる。 | Product-level最適化とPortfolio/Product-line-level共通化は異なるDecisionであり、共通部と差別化部の境界を設計する必要がある。 | 生成・Variant automationが進むほど、Common architectureの進化ルールと例外管理がボトルネックになる。 | Drive追加文献：多様な要求を満足させるシステム開発事例 |
| C67 | F19 Cross-domain Coordination / Design Suri-awase | 複数機能の全体最適 | 静粛性、耐久性、信頼性、高出力、軽量化、意匠など背反機能を各担当が個別最適すると、他機能との不整合が残る。 | System-level目標と因果関係を共有し、設計値変更による他機能への効果をすり合わせる必要がある。 | 多目的最適化を自動化しても、目的関数の重み、Must/Better/Delightの優先順位と最終合意が残る。 | Drive追加文献：複数品質を扱うMBD製品開発事例 |
| C68 | F16 Process / Method / Adoption | ベストプラクティス横展開 | 成功事例をそのまま別部署へコピーしても、組織規模、製品特性、安全要求、外注比率、文化の違いで機能しない。 | Reuseすべきなのは完成Processではなく、背景→課題→施策→定着→効果という因果構造とTailoring原則である。 | AIでBest Practice推薦が容易になると、適用条件のマッチングとTailoring責任が課題になる。 | Drive追加文献：プロセス改善ベストプラクティス集 |
| C69 | F7 Derivative / Variant / Reuse | Featureを軸にしたモデルベース製品開発 | 類似製品や機種展開で、どの機能が共通でどこが製品固有なのかが成果物単位では捉えにくく、再利用と差別化の両立が難しい。 | 再利用対象をファイルや部品ではなくFeature/Variation pointとして管理しないと、派生時の変更範囲と構成理由を説明できない。 | Feature化・自動生成後は、Feature間制約、共通資産の進化、例外VariantのGovernanceがボトルネックになる。 | Web: IPA/SEC 2015「フィーチャーの概念を取り入れたモデルベース開発」 |
| C70 | F18 Assurance / Authority / Governance | Simulation結果を使う意思決定 | Simulationソフトの期待結果について、開発者・利用者間で『何をもって正しい結果とするか』の合意が曖昧になりやすい。 | 計算を自動化することと、期待結果・前提・妥当性根拠を合意することは別問題である。 | AI/Surrogateで結果生成が高速化すると、Acceptance criterion、Evidence、承認責任がさらに重要になる。 | Web: IPA/SEC 2015「D-Case導入によるシミュレーションS/Wの期待結果明確化と合意形成」 |
| C71 | F15 Knowledge / Skill / Rationale | Legacy codeからMBDへ移行 | 既存Cコードしか正本が残っておらず、状態遷移や設計意図を理解しないとモデルベース開発へ移行できない。 | Legacy資産では実装に構造が埋没しており、reverse engineeringと設計知識回復が新規設計より先に必要になる。 | AIでコード解析できるようになると、抽出した状態・要求・意図が本当に正しいかのValidationがボトルネックになる。 | Web: IPA/SEC 2015「C言語ソースコードに対する状態遷移抽出技術」 |
| C72 | F5 System Architecture / Ownership | 大規模システムへのMBD適用 | 局所モデルでは効果が出ても、System規模が大きくなるとModel分割、責任範囲、Interface、統合順序の設計が難しい。 | MBDの規模拡大はモデル数の増加ではなく、Architecture/Ownership/Integration Strategyの問題になる。 | モデル生成自動化後は、System decompositionとIntegration authorityが主要ボトルネックになる。 | Web: IPA/SEC 2015「大規模システムへのモデルベース開発手法の適用」 |
| C73 | F2 Requirement Scope / Meaning | SysMLによる要求可視化 | 要求文書だけでは、要求の関係・構造・対象範囲を関係者が同じように理解できず、レビュー時の確認が難しい。 | 要求は文単位ではなく、Stakeholder/Function/Constraint/Relationを含む構造として理解する必要がある。 | AIで要求構造化した後は、関係の意味精度と変更時の同期がボトルネックになる。 | Web: IPA/SEC 2015「製品開発におけるSysML適用～要求の可視化～」 |
| C74 | F18 Assurance / Authority / Governance | 認証を伴う高信頼開発 | 国際規格認証では要件から検証結果まで正確なTraceが必要だが、Trace作成・維持・監査準備の負荷が大きい。 | Certification evidenceは単なるLink集ではなく、版・承認・Verification結果・変更履歴を含むAssurance systemである。 | AIでEvidence linkを生成しても、Provenance、独立Review、認証Authorityへの説明責任が残る。 | Web: IPA/SEC 2015「国際スタンダード認証に求められる要件から検証結果までのトレーサビリティ管理」 |
| C75 | F17 Work Management / Metrics / Incentives | 試験品質の管理 | Testを大量に実施していても、どの指標を見れば品質が良い/悪いか判断できず、追加試験や終了判断が経験依存になる。 | 計測可能な量とDecisionに有効なMetricは異なり、Metric設計自体がEngineering managementの問題である。 | AIで分析を自動化すると、Metric選択、閾値、Goodhart化の防止がボトルネックになる。 | Web: IPA/SEC 2015「メトリクス分析手法を用いた試験品質向上」 |
| C76 | F18 Assurance / Authority / Governance | Security要求を含む開発 | Security対策が後付けになりやすく、設計段階で脅威・脆弱性・対策を組み込まないとリリース直前に大きな修正が必要になる。 | Securityは検査だけでなく、Requirement/Architecture/Implementation/Verificationを横断する設計責任である。 | AIによる脅威分析後は、脅威情報の鮮度、誤検出、Risk acceptance、Security authorityが課題になる。 | Web: IPA/SEC 2015「セキュア開発手法と診断ツールの活用」 |
| C77 | F7 Derivative / Variant / Reuse | 製品ファミリのVariant管理 | 共通資産を再利用したい一方、各チームが製品固有変更を共通資産へ持ち込み、Maintenanceと大規模再利用が難しくなる。 | Reuse率を上げるだけではなく、Variation pointとCore asset ownershipを統治する必要がある。 | Variant生成が容易になるほど、例外増殖、Rule conflict、Core asset変更権限が次の課題になる。 | Web: IPA/SEC 2016 No.59 |
| C78 | F2 Requirement Scope / Meaning | 超上流Requirement明確化 | 顧客要求を聞いても、そのままでは利用時体験や本当の業務要求まで設計へ落とせず、『あるべき姿』を示すだけでは現場導入も難しい。 | Requirement engineeringには内容定義だけでなく、現場が実行できるProcess/Guideへの変換が必要である。 | AIが要求候補を出せるようになると、Context取得と現場定着がボトルネックになる。 | Web: IPA/SEC 2016 No.60 |
| C79 | F11 Model / Simulation Credibility | Plant modelを含むSystem MBD | Control側だけモデル化してもPlant/Environmentが十分でなければSystem全体をSimulationできず、MBDの恩恵が局所に留まる。 | End-to-End virtual verificationにはPlant fidelity、Boundary condition、Subsystem integrationが必要になる。 | Plant modelをAI生成しても、精度、適用範囲、Calibration、実測との一致が次のボトルネックになる。 | Web: IPA/SEC 2016 No.61 |
| C80 | F17 Work Management / Metrics / Incentives | 多数Systemの開発・運用管理 | 認証・IT統制・品質要求に対応する記録が多重化し、Excel/個別管理/記憶依存が混在して維持コストが増える。 | 管理要求を個別帳票で満たすと、同じ事象を複数記録するOperational overheadが生じる。 | Issue/Workflowを統合した後は、入力品質、ルール運用、Metric利用、過剰管理がボトルネックになる。 | Web: IPA/SEC 2016 No.62 |
| C81 | F16 Process / Method / Adoption | Domain Specific Modeling導入 | UMLやSimulink等のToolを採用しても、Toolを使うこと自体が目的化し、Domain概念と成果物生成が十分に結び付かないことがある。 | モデリング言語はDomain decisionを自然に表現できる抽象度・語彙とGeneratorまで含めて設計すべきである。 | AIが汎用言語から生成できるようになると、Domain schema/ontologyの設計品質がボトルネックになる。 | Web: IPA/SEC 2016 No.63 |
| C82 | F3 Quality / Non-functional / UX | 専門機器の利用品質 | 性能・多機能化を重視した結果、実利用の使い勝手が後回しになり、顧客・営業から操作性の問題が大量に出る。 | 技術性能が高いことと、利用業務で価値が高いことは別であり、実利用Contextを上流へ戻す必要がある。 | AIでUI案を生成しても、利用Context、Human factors、評価指標がボトルネックになる。 | Web: IPA/SEC 2016 No.64 |
| C83 | F18 Assurance / Authority / Governance | Safety/Securityと保守性の作り込み | 専門的な設計原則を現場全員へ徹底することが難しく、欠陥予防の知識が一部Expertだけに依存する。 | 高信頼設計には高度な理論だけでなく、現場が判断できる簡潔なRule/Criteriaへの翻訳が必要である。 | AI Reviewを導入すると、Ruleの根拠、例外、更新、責任Ownerがボトルネックになる。 | Web: IPA/SEC 2016 No.65 |
| C84 | F5 System Architecture / Ownership | 派生開発基盤の再構築 | 派生を繰り返した後にSoftwareだけを整理しても不十分で、System上流から標準成果物を再構築しないとCore assetにならない。 | Product line化には既存成果物整理ではなく、上流Requirement/Architecture/Processを共通資産として再定義する必要がある。 | 標準成果物ができた後は、Core asset evolutionとVariant feedbackが課題になる。 | Web: IPA/SEC 2016 No.66 |
| C85 | F21 Engineering Environment / Automation Quality | Hybrid engineering environment | Cloud活用を進めたくても既存資産、性能、Security、環境保存、Cost等から全移行は現実的でなく、複数環境の併存が必要になる。 | 開発環境Architectureは理想Tool統一ではなく、Workload/Asset/Constraintごとの配置Decisionである。 | AI基盤導入後は、Data placement、Latency、Access control、Cost、環境再現性がボトルネックになる。 | Web: IPA/SEC 2016 No.67 |
| C86 | F16 Process / Method / Adoption | 短納期開発プロセス | 下流Testで仕様欠陥を見つけるWaterfallでは短納期要求に耐えず、設計とTest観点を早期に同期する必要がある。 | Front-loadingは上流工数を減らす手法ではなく、上流へVerification thinkingを移す手法である。 | Test設計をAI化すると、要求品質とTest intentの同期がボトルネックになる。 | Web: IPA/SEC 2016 No.68 Wモデル |
| C87 | F9 Review / Decision Quality | FMEA/リスク分析 | FMEAは有効だが、分析観点が担当者経験に依存し、漏れや分析工数のばらつきが大きい。 | Risk analysisでは表の作成より、どのFailure modeを想起できるかという観点設計が重要である。 | AIでFailure候補を列挙すると、優先順位・妥当性・重複排除とRisk acceptanceが課題になる。 | Web: IPA/SEC 2016 No.69 |
| C88 | F13 Observability / Feedback / Root Cause | 不具合分析 | 不具合記録は大量にあるが、非定形Textと定量Metricを統合して原因傾向を捉えることが難しい。 | 単なる検索ではなく、定性Contextと定量傾向を結び付けないと改善Decisionに使えない。 | LLM分析後は、分類再現性、因果と相関の混同、Knowledge更新が課題になる。 | Web: IPA/SEC 2016 No.71 |
| C89 | F10 Verification / Test Design | Unit test自動化 | Test harnessやStub作成に手間がかかり、Unit testの実施量を増やしにくい。 | Test execution自動化には、対象Interfaceの理解、Stub behavior、期待値仕様の明確化が必要になる。 | Stub/Test生成AI導入後は、Stub realismとOracle妥当性がボトルネックになる。 | Web: IPA/SEC 2016 No.72 |
| C90 | F13 Observability / Feedback / Root Cause | 設計品質改善 | Defect件数は分かっても、どの設計活動・欠陥タイプが品質へ効いているか分からず改善施策が経験的になる。 | 品質改善にはDefect taxonomyとProcess pointを結び付け、原因分布の変化を見る必要がある。 | AI分類後は、分類軸の安定性と改善Actionへの因果接続が課題になる。 | Web: IPA/SEC 2016 No.73 ODC |
| C91 | F10 Verification / Test Design | System scenario test | 機能仕様だけからTestを作ると、顧客の実運用で起きる操作順序・環境・例外Scenarioを取りこぼす。 | Verification spaceはFunctionだけでなくOperational contextから生成する必要がある。 | AI Scenario生成後は、現実的Scenarioか、Risk coverageが十分かの判定が課題になる。 | Web: IPA/SEC 2016 No.74 |
| C92 | F18 Assurance / Authority / Governance | 品質保証と機能安全監査 | SQA監査とSafety規格に基づく確証Reviewが別々に運用されると、Project側の説明・Evidence準備が重複する。 | 異なるAssurance activityの目的、Evidence、Independence requirementを統合設計する必要がある。 | AIでEvidenceを収集しても、独立性・Review authority・規格適合判断は残る。 | Web: IPA/SEC 2016 No.76 |
| C93 | F17 Work Management / Metrics / Incentives | 組織横断の品質改善 | 成熟度向上Processを一律に回すには多大な労力がかかり、どのProcess領域へ改善投資すべきか絞れない。 | 組織成熟度の平均値ではなく、実Project dataから品質に効くProcess factorを特定する必要がある。 | AI分析後は、相関に基づく誤施策と局所Metric最適化が課題になる。 | Web: IPA/SEC 2017 No.78 |
| C94 | F13 Observability / Feedback / Root Cause | 利用時品質の早期Feedback | 利用者からのFeedbackをRelease後に受けると改善が次Versionまで遅れ、設計中に利用時品質を判断できない。 | Operational/UX feedbackを開発中のValidation loopへ入れる必要がある。 | Telemetry/AI分析が進むと、代表性、Privacy、改善優先順位が課題になる。 | Web: IPA/SEC 2017 No.79 |
| C95 | F15 Knowledge / Skill / Rationale | IV&V人材の能力評価 | 高度な分析能力が必要でも、技術者がどのような思考をしているか見えず、適性評価・育成が難しい。 | 成果物だけでなくReasoning processを可視化しないと、Expertiseを組織能力へ変換できない。 | AIがReasoningを支援すると、人間自身の能力評価とAI依存の切り分けが課題になる。 | Web: IPA/SEC 2017 No.80 |
| C96 | F2 Requirement Scope / Meaning | Prototypeを用いた要件合意 | 文書で要件を固定してから作ると、利用者と開発者の認識差が後工程まで残り、Schedule/工数計画が崩れる。 | 要求は一度で確定するより、Executable/visible prototypeを介して早期にFeedbackする方が有効な場合がある。 | AI Prototypeが容易になると、見た目の完成度に引きずられる誤合意と非機能要件漏れが課題になる。 | Web: IPA/SEC 2017 No.82 |
| C97 | F5 System Architecture / Ownership | Microservice/Service architecture | 技術的にはService分割できても、どの粒度でServiceをまとめ、どこへ配置するかが難しい。 | 分散化の本質はTool/Frameworkではなく、Responsibility boundaryとCouplingの設計である。 | AIでArchitecture案が大量生成されると、Quality attribute trade-offとOwnershipが課題になる。 | Web: IPA/SEC 2017 No.83 |
| C98 | F3 Quality / Non-functional / UX | 派生変更による性能劣化 | 機能変更へ集中すると、処理時間など非機能性能の劣化がSystem testや納品後まで見つからない。 | 変更RequirementにはFunctional deltaだけでなくQuality attributeへの影響を含める必要がある。 | AI Impact分析後は、非機能Budgetと閾値の管理が課題になる。 | Web: IPA/SEC 2017 No.85 |
| C99 | F9 Review / Decision Quality | Review meeting | Review会議を実施していても、参加目的や役割が曖昧で、効率・効果が良いか把握できない。 | Review品質は指摘件数だけでなく、誰が何を判断するための会議かというDecision designに依存する。 | AI Reviewer導入後はHuman reviewを何のために残すか、Escalation条件が課題になる。 | Web: IPA/SEC 2017 No.87 |
| C100 | F10 Verification / Test Design | Exploratory testing | 探索的Testは欠陥発見効率が高い一方、総量・実施範囲が不透明で管理・説明しにくい。 | 探索自由度とCoverage/Evidence/計画可能性のTrade-offを管理する必要がある。 | AI探索Agent導入後は探索範囲、停止条件、再現性が主要課題になる。 | Web: IPA/SEC 2017 No.88 |
| C101 | F10 Verification / Test Design | 組合せTest自動化 | Test実行を自動化しても、Test項目作成・優先順位付け・障害分類は人手に残り、組合せ爆発時に工数が支配的になる。 | Automation bottleneckはExecutionからTest-space designとTriageへ移動する。 | 生成AI導入後は、優先度根拠、Coverage、重複Test削減、Failure clustering精度が課題になる。 | Web: IPA/SEC 2017 No.89 |
| C102 | F6 Change Impact / Trace | Regression test選択 | 短納期・多Variantでは全回帰Testを実行できず、人の経験で影響範囲を絞ると漏れリスクが高い。 | Change graph/Code dependencyとVerification assetを接続して、再検証範囲を説明可能にする必要がある。 | AI Impact候補後はFalse negativeの管理と重要PathのEvidenceが課題になる。 | Web: IPA/SEC 2017 No.90 |
| C103 | F3 Quality / Non-functional / UX | DesignとEngineeringの融合 | HMI/UX評価が工程後半に一度しかできないと、問題を見つけても改善時間が残らない。 | 利用時品質のValidationを設計Loopへ高頻度で入れ、DesignとEngineeringを同期する必要がある。 | 生成UI/Simulation後はHuman evaluationの代表性と主観品質の定量化が課題になる。 | Web: IPA/SEC 2017 No.91 |
| C104 | F7 Derivative / Variant / Reuse | 長期製品シリーズ | 単一製品のMBD/MDDが成功しても、長期の製品シリーズではCore/Variant、資産進化、Release間差分を扱えないとScaleしない。 | Product lineは再利用率ではなく、長期に共通Assetを進化させるGovernanceが本質である。 | AIによる派生生成後はCore contaminationとVariant debtが課題になる。 | Web: IPA/SEC 2017 No.92 |
| C105 | F21 Engineering Environment / Automation Quality | MBD内製Toolの拡大 | Commercial toolだけではProcess間を埋められず内製Toolが増えるが、要求レベル・妥当性・品質を客観評価する標準指標がなく、要求者と開発者で共通認識を作りにくい。 | Engineering automationにもRequirement/Validation/Lifecycleを持つProduct engineeringが必要である。 | AI Agent内製化が進むと、同じ問題がAgent requirement、evaluation、version、ownerへ拡大する。 | Web: JMAAB 2025 開発環境ランク設定WG |
| C106 | F18 Assurance / Authority / Governance | 生成AIを使うMBD | 仕様からCode/Test/Modelを生成できても、何が正しいかの判断基準、人とAIの責任範囲、品質担保、機能安全/SPICE対応が未解決になる。 | Generationの自動化とAuthoritative engineering decisionは分離して設計する必要がある。 | AI能力向上ほどHuman authority、evaluation set、process definitionがボトルネックになる。 | Web: JMAAB サロン2026公開まとめ |
| C107 | F15 Knowledge / Skill / Rationale | Review skillのAI継承 | 優秀Reviewerの観点や思考Processが個人に閉じ、若手が成果物だけを見ても『なぜそこを見るか』を学べない。 | Review knowledgeはCheck listだけでなく、Context→着眼→仮説→確認というReasoning patternとして蓄積する必要がある。 | AI Reviewerが普及するとHuman reviewerの能力劣化とAI知識の更新/誤学習が課題になる。 | Web: SQiP 2025「もぐつむ法」 |
| C108 | F2 Requirement Scope / Meaning | 生成AIによるRequirement改善 | 要求仕様改善にAIを使っても、与える観点表の粒度によって出力品質が変わり、単純にPromptを増やせば良いとは限らない。 | AI品質はModel能力だけでなく、Engineering criteriaの構造と粒度に強く依存する。 | 観点を標準化すると、Project固有観点の追加・不足検知がボトルネックになる。 | Web: SQiP 2025 AI for test input quality |
| C109 | F14 Data / Tool / Interoperability | Excel設計資料をAIへ入力 | 人間には読めるExcelでも、結合セル、表構造、位置依存表現等によりAIが必要情報へ到達できない/意味推論できない。 | AI-ready dataはファイル形式の問題ではなく、抽出到達性と意味構造の問題である。 | 構造化変換後は、元資料との同一性、Formula/Version、write-backが課題になる。 | Web: SQiP 2025「Excel管理資料の生成AI可読性」 |
| C110 | F2 Requirement Scope / Meaning | 初心者によるUSDM/要求仕様化 | 手法を教育しても、初心者は要求の範囲のバランスが悪く、他者に伝わりづらい要求仕様になりやすい。 | 要求記述の前にContext、Use case、Domain conceptを整理しないと、Templateだけでは要求範囲を安定させられない。 | AIがUSDMを生成しても、Context modelとValue/Conceptの正しさが上位ボトルネックになる。 | Web: AFFORDD 2025 USDM経験発表 |
| C111 | F10 Verification / Test Design | Cloud連携組込みSystem test＋LLM | 組込み単体からCloud連携Systemへ拡大すると、End-to-Endの状態・通信・外部Serviceを含むSystem testが急激に複雑になる。 | System testは単一製品仕様だけでなく、分散Service/Network/Update lifecycleを含むScenario engineeringになる。 | LLM支援後は外部環境変動、再現性、Oracle、Security boundaryが課題になる。 | Web: AFFORDD 2025 LLM活用System test事例 |
| C112 | F4 Boundary / Interface / Agreement | Cyber-physical製品のPartner開発 | HardwareとSoftware/Serviceを複数Partnerで短期間開発する際、要求・変更・Scheduleの同期が難しい。 | Partner collaborationではArtifact交換より、Change intentと依存関係を共通Processへ埋め込む必要がある。 | AIによるCoordination支援後は、Company boundaryを越える権限・責任・契約上のEvidenceが課題になる。 | Web: AFFORDD 2025 XDDP smart-lock workshop |
| C113 | F11 Model / Simulation Credibility | Virtual calibration / MBD高度化 | MBDを開発全体へ広げても、性能検証段階では実車による制御適合に多大なResourceが残る。 | Simulation高速化の次のBottleneckは、複数Plantを統合したSystem modelと、実車性能へつながるCalibration fidelityである。 | Virtual calibration拡大後はModel discrepancy、Parameter uncertainty、実車Correlationが課題になる。 | Web: 自動車技術会論文集 2026 MBDパワーユニット第8報 |
| C114 | F10 Verification / Test Design | Market robustness validation | 様々な使用状況を実車で網羅しようとすると検証工数が増大し、標準走行だけではRobustnessを示せない。 | Field big dataから代表/境界Scenarioを設計し、Virtual verificationへつなぐ必要がある。 | AIでScenario選定するとRare event coverage、Data bias、Scenario validityが課題になる。 | Web: 自動車技術会論文集 2026 MBDパワーユニット第9報 |
| C115 | F14 Data / Tool / Interoperability | 現在のモデル接続・流通標準化 | 企業/Tool間連携が進んでも、FMI、Plant I/F、モデル流通Process等のGuidelineが継続改訂されており、Interoperabilityは一度決めれば終わる問題ではない。 | Tool version、Model type、利用目的の進化に合わせてInterface contractを継続管理する必要がある。 | AI AgentがToolを横断すると、API/semantic contract/version compatibilityの維持がさらに重要になる。 | Web: JAMBE ガイドライン/モデル 2024-2025 |
| C116 | F16 Process / Method / Adoption | 人とAIが共同利用する開発Process | USDM/PFD等の人間向け方法論をそのままAIへ渡しても、AIが構造・意図・Process状態を安定して解釈できるとは限らない。 | Human-readable methodをAI-collaboration-readyなSchema/Process representationへ変換する必要がある。 | Schema化後は、人間とAIで同じProcess意味を維持するVersioning、Authority、Tool integrationが課題になる。 | Web: AFFORDD 2026 T23 AI協働開発 |

# 5. 21 Root Painの再評価

| Root Pain | Definition | Case density* |
|---|---|---:|
| **F1 Goal / Value / Target Deployment** | 顧客価値・事業目標・製品KPIを、システム/部品/部署へ根拠付きで展開できない。 | 4 |
| **F2 Requirement Scope / Meaning** | 要求の範囲・意味・理由・前提を関係者が同じように理解できない。 | 9 |
| **F3 Quality / Non-functional / UX** | 性能、保守性、使いやすさ、Security等の品質属性が機能要求より後回しになる。 | 8 |
| **F4 Boundary / Interface / Agreement** | 部署・企業・専門領域の境界で意味・責任・Assumptionが失われる。 | 3 |
| **F5 System Architecture / Ownership** | 全体構造とSystem-level責任が弱く、局所最適やArchitecture劣化が進む。 | 6 |
| **F6 Change Impact / Trace** | 変更が何へ波及し、何を再確認すべきかを正しく絞れない。 | 3 |
| **F7 Derivative / Variant / Reuse** | 派生・Variant・Core assetの共通性/差分/再利用条件を管理できない。 | 7 |
| **F8 Cross-artifact Consistency / Configuration** | 要求・モデル・コード・試験・BOM等のVersion/SoR/同期が崩れる。 | 2 |
| **F9 Review / Decision Quality** | レビューで何を判断し、どこまでなら十分か、最適案かを評価できない。 | 4 |
| **F10 Verification / Test Design** | Test範囲、Scenario、Coverage、Oracleを決められず、Testが爆発する。 | 10 |
| **F11 Model / Simulation Credibility** | モデルの粒度、精度、Context、適用範囲をどこまで信用してよいか判断できない。 | 7 |
| **F12 Trade-off / Feasibility / Uncertainty / Optimization** | 複数案・多目的・不確定性を保持しながら成立範囲と設計案を早期判断できない。 | 2 |
| **F13 Observability / Feedback / Root Cause** | 必要な実測・運用データが取れず、原因特定や現実から設計へのFeedbackが弱い。 | 5 |
| **F14 Data / Tool / Interoperability** | Tool/Data/企業境界が分断され、情報・モデル・Execution Contextが流通しない。 | 7 |
| **F15 Knowledge / Skill / Rationale** | 設計意図・観点知識・判断根拠が個人依存し、再利用・育成できない。 | 8 |
| **F16 Process / Method / Adoption** | 手法・Processを本質理解し、現場にTailorし、定着・横展開できない。 | 7 |
| **F17 Work Management / Metrics / Incentives** | 進捗・工数・KPI・目標管理が重く、誤った指標が局所行動や疲弊を生む。 | 6 |
| **F18 Assurance / Authority / Governance** | 誰が何を信用・承認し、どのEvidenceで正本へ反映するか定義できない。 | 12 |
| **F19 Cross-domain Coordination / Design Suri-awase** | 並行する専門設計の相互依存を見ながら、設計値・制約・責任を継続的にすり合わせられない。 | 2 |
| **F20 Lifecycle / Transition / Operation** | 移行、運用、保守、廃棄、試験可能時間などLife cycle制約を上流設計へ織り込めない。 | 1 |
| **F21 Engineering Environment / Automation Quality** | Simulation/内製Tool/Script/Agentの実行環境自体が不安定・属人化し、新たな技術負債になる。 | 3 |

*Case densityは市場発生率ではない。この質的ケース集合の中で反復して現れた密度である。

# 6. 事例拡張で特に強くなったPain

今回の追加事例で特にEvidenceが厚くなったのは以下である。

1. **F10 Verification / Test Design**：実行自動化→Test設計→優先順位→Oracle→Coverageへ移動。
2. **F18 Assurance / Authority / Governance**：Trace/AI/モデル交換が可能になった後、承認・Evidence・権限・Safetyが残る。
3. **F7 Derivative / Variant / Reuse**：再利用成功後にCore assetの進化とVariant debtが問題になる。
4. **F15 Knowledge / Skill / Rationale**：上流判断・Review観点・設計意図はTool導入後もExpert依存しやすい。
5. **F21 Engineering Environment / Automation Quality**：内製ToolからAI Agentまで、Automation自体をEngineeringする必要がある。

# 7. Bottleneck Migration Pattern v2

| Before | 技術/方法による改善 | After / 次のPain |
|---|---|---|
| Requirementが書けない | USDM/Template/AI | Context、観点、合意、変更同期 |
| Legacyを理解できない | Reverse engineering/LLM | 抽出意図のValidation |
| Traceが作れない | ALM/Graph/AI | 重要Trace選別、False negative、Evidence |
| Test実行が遅い | Automation | Test space、優先順位、Oracle、Coverage |
| Modelがない | MBD/AI生成 | Fidelity、Context、Calibration、信用範囲 |
| CAEが遅い | HPC/Surrogate | 何を探索するか、不確実性、設計案の捨て時 |
| Modelを送れない | Standard package/FMI/Hub | ID、Version、Authority、Security、編集権限 |
| Reviewが属人 | AI Reviewer | Escalation、人の役割、AI知識更新 |
| Tool操作が属人 | Script/Agent | Tool/Agent requirement、Validation、Version、Owner |
| 再利用できない | SPL/Variant automation | Core asset evolution、Variant debt |

# 8. AI×MBSE Offeringへの変換

116ケースから、AI×MBSE商材は『AI機能』よりRoot Painの集合で設計する。

| Offering family | 主Root Pain | 顧客に見せる入口 | AI適用後まで含めるべき範囲 |
|---|---|---|---|
| Requirements & Intent Intelligence | F1,F2,F3,F15 | 仕様漏れ・認識差・上流手戻り | Context、Rationale、Review、Human approval |
| Change / Impact / Regression Intelligence | F6,F8,F10 | 変更後の確認範囲が分からない | Impact→Re-test→Evidence |
| Product-line / Variant Intelligence | F5,F7,F8 | 派生・Variantが増え続ける | Core asset governance、Rule、Test allocation |
| V&V / Scenario Intelligence | F10,F18 | Testが増えすぎる/十分性が不明 | Oracle、Coverage、Risk prioritization |
| Model / Simulation Decision Acceleration | F11,F12,F13 | 実機/CAEに時間がかかる | Credibility、Uncertainty、Calibration、Feedback |
| Cross-domain Design Coordination | F4,F5,F19 | 部署間すり合わせに時間がかかる | Dependency、Budget、Trade-off、Decision convergence |
| Engineering Data / Model Flow | F8,F14,F20 | Tool/企業間で情報がつながらない | SoR、Version、ID、Access、Lifecycle |
| AI/Engineering Assurance | F18 | AI/自動化結果を正式業務で信用できない | Evaluation、Evidence、Authority、Regression |
| Engineering Automation Architecture | F16,F17,F21 | 内製Tool/Script/Agentが増殖 | Requirement、Validation、Owner、Retirement |

# 9. 次のResearch Backlog

Source Graphから次に深掘りするべき領域は以下。

- IPA/SEC 93件を全件、Pain/Before/After/効果/残課題でCoding
- AFFORDDライブラリをT04/T05/T08/T12/T14/T19/T20/T21/T22/T23別に全件抽出
- SQiP 2004～2025を要求/Review/Test/Process/AIに限定して時系列比較
- JMAAB 2024～2026でAutomation→AI→AssuranceへのBottleneck shiftを追跡
- JAMBE/JAMAのモデル流通Guideline Version履歴から、標準化後に増えた要求を抽出
- 自動車技術会2024～2026のMBD/CAE/Calibration/官能評価論文から最新Painを追加
- メカ/CAD、ECAD/E/E、Cybersecurity、生産技術、認証、Field feedbackを補強

# 10. 事業戦略で使う最終診断単位

```text
Capability Cell
× Novelty / Change / Variant / Assurance modifier
× Root Pain
× Current method / workaround
× Engineering Decision
× Data / Tool / Model
× Automation level
× AI applicability
× Projected bottleneck after AI
× Authority / Assurance
× KPI
× Offering
```

この構造なら、一社の中にMBD成熟部署と文書中心部署、AI先行部署と量産高保証部署が混在していても、それぞれ別のOpportunityとして診断できる。

# 11. 主要Web Source

- IPA/SEC事例アーカイブ: https://www.ipa.go.jp/archive/digital/iot-en-ci/jirei/index.html
- IPA/SEC適用分析: https://www.ipa.go.jp/archive/publish/secbooks20160511.html
- AFFORDD資料ライブラリ: https://affordd.jp/libraries/
- SQiP 2025成果: https://www.juse.or.jp/sqip/workshop/report/2025.html
- JMAAB Open Conference 2025: https://jmaab.jp/joc2025/
- JAMBE Guideline/Model: https://www.jambe.jp/system/download
- JAMA電子制御情報交換: https://www.jama.or.jp/operation/it/dg_egr/electronic_ctrl.html
- 自動車技術会論文集: https://www.jstage.jst.go.jp/browse/jsaeronbun/