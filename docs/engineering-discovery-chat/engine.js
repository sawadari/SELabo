// Engineering Discovery — deterministic, browser-only experimental engine.
// This is intentionally NOT an LLM, causal estimator, or customer-fact verifier.
// Source methodology: experiments/engineering-discovery-chat/{02,04,05,06}.
export const FAMILIES = [
  {id:"F1",name:"Goal / Value / Target Deployment",terms:["顧客価値","目標展開","目標配分","製品目標","価値指標"],upstream:[],decision:"どの目標を各システムへ配分するか",offering:"O1"},
  {id:"F2",name:"Requirement Scope / Meaning",terms:["要求","仕様","曖昧","仕様漏れ","合意できない"],upstream:["F1","F15"],decision:"この要求の意味・範囲を承認してよいか",offering:"O1"},
  {id:"F3",name:"Quality / Non-functional / UX",terms:["非機能","性能劣化","機能安全","使いやすさ","品質属性"],upstream:["F1","F2"],decision:"必要な品質属性が十分に設計へ反映されているか",offering:"O1"},
  {id:"F4",name:"Boundary / Interface / Agreement",terms:["インタフェース","インターフェース","企業間","部署間","受け渡し","責任境界"],upstream:["F2","F5"],decision:"境界条件と責任分担について合意できるか",offering:"O6"},
  {id:"F5",name:"System Architecture / Ownership",terms:["アーキテクチャ","全体設計","システム構成","オーナー不在","owner不在"],upstream:["F1","F2","F15"],decision:"このシステム構成と設計責任を採用してよいか",offering:"O9"},
  {id:"F6",name:"Change Impact / Trace",terms:["変更影響","影響範囲","変更管理","変更後","トレース","追跡","波及"],upstream:["F5","F7","F14","F15"],decision:"この変更を採用し、何を再確認すべきか",offering:"O2"},
  {id:"F7",name:"Derivative / Variant / Reuse",terms:["派生","バリアント","variant","機種","再利用","製品系列","品種"],upstream:["F5","F2"],decision:"この派生構成・再利用範囲を承認してよいか",offering:"O3"},
  {id:"F8",name:"Cross-artifact Consistency / Configuration",terms:["整合","バージョン","版管理","二重管理","同期","構成管理","正本"],upstream:["F14","F6","F7"],decision:"要求・モデル・試験結果の版と整合を信用できるか",offering:"O2"},
  {id:"F9",name:"Review / Decision Quality",terms:["レビュー","審査","評価会","指摘","判断基準"],upstream:["F2","F8","F15"],decision:"何を根拠に設計・変更を承認するか",offering:"O8"},
  {id:"F10",name:"Verification / Test Design",terms:["テスト","試験","検証","回帰","coverage","カバレッジ","テストケース"],upstream:["F7","F6","F2","F11"],decision:"変更後にどこまで試験すれば十分か",offering:"O4"},
  {id:"F11",name:"Model / Simulation Credibility",terms:["シミュレーション","モデル精度","モデル妥当性","plant","プラントモデル","モデルが信用"],upstream:["F13","F18"],decision:"このモデルの結果を今回の判断に利用してよいか",offering:"O5"},
  {id:"F12",name:"Trade-off / Feasibility / Optimization",terms:["トレードオフ","成立性","最適化","設計案","不確実性","設計空間"],upstream:["F1","F5","F11"],decision:"どの設計代替案を採用すべきか",offering:"O5"},
  {id:"F13",name:"Observability / Feedback / Root Cause",terms:["実測","フィードバック","不具合原因","原因特定","観測","ログ"],upstream:["F11","F15"],decision:"どの証拠から原因と改善策を判断するか",offering:"O5"},
  {id:"F14",name:"Data / Tool / Interoperability",terms:["ツール間","連携できない","データ連携","データ分断","転記","excel","ツールがバラバラ"],upstream:["F4","F8"],decision:"どの情報を正本として流通させるか",offering:"O6"},
  {id:"F15",name:"Knowledge / Skill / Rationale",terms:["属人","ベテラン","暗黙知","設計意図","ノウハウ","知識継承"],upstream:["F16"],decision:"設計判断の根拠を誰が再利用・確認できるか",offering:"O8"},
  {id:"F16",name:"Process / Method / Adoption",terms:["定着しない","運用されない","モデルが使われない","形骸化","プロセス改善","導入効果"],upstream:["F1","F15","F14"],decision:"この業務手法をどの判断業務に適用すべきか",offering:"O8"},
  {id:"F17",name:"Work Management / Metrics / Incentives",terms:["進捗管理","工数","メトリクス","kpi","日程遅延","管理負荷"],upstream:["F9","F10","F16"],decision:"どの指標で進捗と改善を判断するか",offering:"O8"},
  {id:"F18",name:"Assurance / Authority / Governance",terms:["承認権限","ガバナンス","監査","認証","エビデンス","保証","本番化できない"],upstream:["F8","F21","F16"],decision:"誰がどの証拠で成果物の正当性を承認するか",offering:"O7"},
  {id:"F19",name:"Cross-domain Coordination",terms:["すり合わせ","ドメイン横断","部門調整","部署横断","調整会議","性能配分"],upstream:["F4","F5"],decision:"関係部署間でどの設計パラメータを合意するか",offering:"O9"},
  {id:"F20",name:"Lifecycle / Transition / Operation",terms:["運用制約","ライフサイクル","保守","移行","廃止","停止時間"],upstream:["F1","F4"],decision:"運用・移行条件を満たす方式を採用できるか",offering:"O6"},
  {id:"F21",name:"Engineering Environment / Automation Quality",terms:["自動化環境","内製ツール","環境の品質","エージェント","実行環境","技術負債"],upstream:["F14","F16"],decision:"この自動化環境を継続利用してよいか",offering:"O7"}
];
const byId = new Map(FAMILIES.map(f=>[f.id,f]));
const defaultQuestions = [
  ["Q0-1","対象Capability Cell（部門・製品・開発工程）はどこですか？","分析単位を特定するため"],
  ["Q0-2","いま発生している困り事と、業務・品質への影響は何ですか？","観測症状と事業影響を区別するため"],
  ["Q0-3","その場面で、誰が何を決められずにいますか？","Engineering Decisionを特定するため"]
];
const specializedQuestions = {
  F10:[
    ["F10-1","テスト増加の主因は、派生機種、仕様変更、状態組合せ、運用シナリオのどれですか？","上流原因F7/F6/F2などを判別するため"],
    ["F10-2","変更後に再実施するテスト範囲は、現在どの情報から決めていますか？","変更影響と検証範囲の接続を確認するため"],
    ["F10-3","期待値（Oracle）とCoverageの合否基準は明文化されていますか？","テスト生成以前の判断基準を確認するため"]],
  F6:[
    ["F6-1","影響範囲の特定に、構造関係・トレース・担当者の経験のどれを使っていますか？","上流の構造と情報分断を判別するため"],
    ["F6-2","変更後に何を再確認するか、誰が最終決定しますか？","Engineering DecisionとAuthorityを特定するため"],
    ["F6-3","影響漏れは主に製品間、部署間、成果物間のどこで起きていますか？","Capability Cell境界を確認するため"]],
  F7:[
    ["F7-1","派生間の共通資産と差分は、どの形式で管理していますか？","Variant/Reuseの根拠を確認するため"],
    ["F7-2","製品ごとの例外変更は誰が承認しますか？","共通資産の統治を確認するため"],
    ["F7-3","派生が増えた際、何の業務時間が最も増えていますか？","直接Painと事業影響を確認するため"]],
  F14:[
    ["F14-1","どのツール・情報間で、転記・検索・同期のどれが詰まっていますか？","分断の実害を特定するため"],
    ["F14-2","各情報の正本と変更責任者は決まっていますか？","System of Recordを確認するため"],
    ["F14-3","情報の連携後、どの設計判断を速くしたいですか？","ツール連携の目的を特定するため"]],
  F16:[
    ["F16-1","新手法のどの作業が、現行業務へ追加負荷になっていますか？","導入形骸化の原因を判別するため"],
    ["F16-2","利用者が手法を使う際に、どの判断へ役立つと認識していますか？","Decision use caseを確認するため"],
    ["F16-3","対象部署の教育・運用責任と改善KPIは明確ですか？","定着条件を確認するため"]],
  F11:[
    ["F11-1","シミュレーションは、何を判断する目的で利用していますか？","必要なモデル忠実度を判別するため"],
    ["F11-2","モデル妥当性を確認する実測・検証証拠はありますか？","Model Credibilityを確認するため"],
    ["F11-3","モデル精度が不足する運用条件や適用範囲は明らかですか？","不確実性の境界を確認するため"]],
  F15:[
    ["F15-1","経験者が不在だと止まるのは、要求・構造・レビュー・リスク判断のどれですか？","知識の所在と判断内容を特定するため"],
    ["F15-2","設計結果だけでなく、その採用理由は残っていますか？","Rationaleの記録状況を確認するため"],
    ["F15-3","知識共有後に成果の正しさを誰が確認しますか？","人の承認境界を確認するため"]],
  F18:[
    ["F18-1","どの成果物・判断に人の最終承認が必要ですか？","AI Authority Boundaryを確定するため"],
    ["F18-2","承認時に求められる証拠と構成管理は何ですか？","Assurance要件を確認するため"],
    ["F18-3","本番運用を妨げている要因は品質、責任、権限、運用のどれですか？","実用化障壁を分けるため"]],
  F19:[
    ["F19-1","部門間で合意できない設計パラメータとその責任者は誰ですか？","すり合わせ対象を具体化するため"],
    ["F19-2","全体最適と部門最適が衝突するときの判断基準はありますか？","Architecture/Authority課題を判別するため"],
    ["F19-3","依存関係や制約値はどの成果物で共有していますか？","情報フローを確認するため"]]
};
function allQuestionCandidates(directs) {
  const primary = directs.length ? directs.map(d=>d.id) : [];
  const result=[], seen=new Set();
  for(const familyId of [...primary,"default"]){
    const list = specializedQuestions[familyId] || (familyId==="default" ? defaultQuestions : []);
    for(const [id,question,why] of list) {
      if(!seen.has(id)){result.push({id,question,why,familyId});seen.add(id);}
    }
  }
  return result;
}
export function evaluate(messages, answeredIds = []) {
  const combined=messages.map(m=>m.text||"").join("\n").toLocaleLowerCase("ja");
  const ranked=FAMILIES.map(f=>{
    const found=f.terms.filter(word=>combined.includes(word.toLocaleLowerCase("ja")));
    return {...f,score:found.length,matched:found};
  }).filter(f=>f.score>0).sort((a,b)=>b.score-a.score || a.id.localeCompare(b.id,"en",{numeric:true}));
  const direct=ranked.slice(0,3);
  const top=direct[0] || null;
  const upstream=top ? top.upstream.map(id=>byId.get(id)).filter(Boolean).slice(0,4) : [];
  const candidates=allQuestionCandidates(direct);
  const answered=new Set(answeredIds);
  const next=candidates.filter(q=>!answered.has(q.id)).slice(0,3);
  return {direct,top,upstream,questions:next,allQuestions:candidates,matchedFamilies:ranked};
}
export function makeSnapshot(messages,answeredIds,diagnosis,history,opportunityId) {
  const now=new Date().toISOString();
  const scope=messages.length ? messages[0].text.slice(0,120) : "未特定";
  const evidenceRefs=messages.map(m=>m.id);
  const directPains=diagnosis.direct.map((f,index)=>({
    id:"PAIN-"+f.id,family_id:f.id,statement:f.name+" に関する症状の可能性（要検証）",
    role:"direct",confidence:"low",evidence_refs:evidenceRefs
  }));
  const upstreamPains=diagnosis.upstream.map(f=>({
    id:"CAUSE-"+f.id,family_id:f.id,statement:f.name+" が上流原因となっている可能性（要検証）",
    role:"upstream_candidate",confidence:"low",evidence_refs:evidenceRefs
  }));
  const causal=diagnosis.top && diagnosis.upstream.length ? [{
    id:"CAUSAL-1",chain:[diagnosis.upstream[0].id,diagnosis.top.id],
    statement:diagnosis.upstream[0].name+" → "+diagnosis.top.name+" の因果関係が存在するかは未確認",
    confidence:"low",discriminating_questions:diagnosis.questions.map(q=>q.question)
  }] : [];
  const offeringIds=["O0",...new Set(diagnosis.direct.map(f=>f.offering))];
  return {
    meta:{opportunity_id:opportunityId,title:"Engineering Discovery 暫定案件",version:"web-rules-0.1",status:"discovery",last_updated:now,overall_confidence:"low"},
    source_registry:messages.map((m,i)=>({id:m.id,type:"user_input",title:"ユーザー入力 "+(i+1),origin:"user_candidate",evidence_strength:"low"})),
    capability_cells:[{
      id:"CELL-001",scope,department_role:"未確認",product_system:"未確認",development_phase:"未確認",
      symptoms:messages.map(m=>({id:"SYM-"+m.id,statement:m.text,origin:"user_candidate",confidence:"low",evidence_refs:[m.id],status:"active"})),
      business_consequences:[],
      engineering_decisions:diagnosis.direct.slice(0,2).map(f=>({id:"DEC-"+f.id,statement:f.decision,confidence:"low"})),
      pain_hypotheses:[...directPains,...upstreamPains],
      causal_hypotheses:causal,
      actionable_root_pains:[],
      current_methods:[],
      environment:{data_sources:[],tools:[],models:[],systems_of_record:[],versions_configuration:[],security_constraints:[],sharing_boundaries:[]},
      current_bottleneck:diagnosis.top ? diagnosis.top.name+" の可能性（未確定）" : "未確認",
      ai_applicability:{necessity:"undetermined",patterns:[],rationale:"ルール／プロセス改善、既存Tool、Native AI、Customer AI、Custom AIを比較する情報が不足",alternatives:["Process / Role / Rule改善","決定論的Automation","既存Engineering Tool","Native AI","Customer AI","Custom AI"]},
      projected_bottleneck:"未確認：AI導入が妥当と判断された後に評価",
      authority_assurance:{level:"undetermined",human_approver:"未確認",evidence_required:[],audit_required:true},
      kpis:[],
      business:{sponsor:"未確認",economic_buyer:"未確認",timing:"未確認",budget_status:"未確認"},
      offering_hypotheses:offeringIds.map((id,i)=>({id:"OFFER-"+id,offering_family:id,rationale:"Pain候補からの機械的な候補であり適用可否は未検証",sequence:i+1,confidence:"low"}))
    }],
    unknowns:diagnosis.allQuestions.map(q=>({
      id:q.id,question:q.question,why_it_matters:q.why,priority:"high",
      status:answeredIds.includes(q.id)?"answered":"open"
    })),
    hypothesis_history:history
  };
}
