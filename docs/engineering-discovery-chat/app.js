import { evaluate, makeSnapshot } from "./engine.js";

const byId = id => document.getElementById(id);
const feed = byId("feed");
const input = byId("message-input");
const target = byId("answer-target");
const output = byId("result-body");
const status = byId("status");
const tabs = [...document.querySelectorAll("[data-view]")];
const state = {
  messages: [], answeredIds: [], history: [], diagnosis: null, snapshot: null,
  view: "hypothesis", pendingQuestion: null,
  opportunityId: "OP-"+Date.now().toString(36)
};
const notConfirmed = "入力情報はユーザーからの未検証情報です。実際の顧客事実としての確認・承認は行っていません。";
function el(tag,text,className) {
  const node=document.createElement(tag);
  if(text!==undefined && text!==null) node.textContent=String(text);
  if(className) node.className=className;
  return node;
}
function section(parent,number,title) {
  const node=el("section",null,"result-section");
  const head=el("h3");
  head.append(el("span",number,"number"),document.createTextNode(title));
  node.append(head);
  parent.append(node);
  return node;
}
function addList(parent,items) {
  const list=el("ul");
  for(const item of items) list.append(el("li",item));
  parent.append(list);
}
function addLine(parent,text,className) { parent.append(el("p",text,className)); }
function current() { return state.snapshot?.capability_cells[0] || null; }
function showQuestion(parent,q) {
  const item=el("div",null,"question");
  item.append(el("p",q.question),el("small",q.why));
  const button=el("button","この質問に回答する");
  button.type="button";
  button.addEventListener("click",()=>{
    state.pendingQuestion=q;
    target.hidden=false;
    target.textContent="回答対象："+q.question;
    input.placeholder="この質問への回答を入力してください";
    input.focus();
    setStatus("回答を送ると、仮説を更新し、この質問を再表示しません。");
  });
  item.append(button);
  parent.append(item);
}
function showHypothesis() {
  output.replaceChildren();
  const d=state.diagnosis, cell=current();
  const s1=section(output,"01","入力された情報（未検証）");
  addList(s1,state.messages.map(m=>m.text));
  addLine(s1,notConfirmed,"hint");

  const s2=section(output,"02","Direct Pain 候補");
  if(!d.direct.length){
    addLine(s2,"症状を分類できませんでした。課題の内容を具体化する質問から開始します。");
  } else for(const f of d.direct){
    const item=el("div",null,"pain-item");
    item.append(el("strong",f.id+"  "+f.name));
    item.append(el("small","入力に対応した語："+f.matched.join(" / ")+" · 確度：未評価（候補）"));
    s2.append(item);
  }
  const s3=section(output,"03","Engineering Decision と上流原因の候補");
  addLine(s3,d.top ? "対象判断の仮説："+d.top.decision : "何を決める仕事が詰まっているかは未確認です。");
  if(d.upstream.length) addList(s3,d.upstream.map(f=>f.id+" "+f.name+"（上流原因の候補）"));
  else addLine(s3,"上流原因は未確認です。","hint");
  addLine(s3,"Actionable Root Painの確定には、顧客が変更可能か・効果測定できるかの確認が必要です。","hint");

  const s4=section(output,"04","次に確認すること（最大3問）");
  if(d.questions.length) d.questions.forEach(q=>showQuestion(s4,q));
  else addLine(s4,"今回の質問候補にはすべて回答済みです。必要に応じて新しい症状や背景を入力してください。");

  const s5=section(output,"05","AI適用判断・Offering");
  addLine(s5,"AIの必要性：未判断。まずProcess / Role / Rule、決定論的Automation、既存Toolで解決できるかを確認します。");
  addLine(s5,"Offering候補："+cell.offering_hypotheses.map(o=>o.offering_family).join(" + "));
  addLine(s5,"AI/Automation導入後の次ボトルネック：未評価。Authority / Assurance：未定義。","hint");
}
function showCausal() {
  output.replaceChildren();
  const d=state.diagnosis;
  const s1=section(output,"01","因果の検証経路");
  const path=d.top ?
    "観測症状（入力情報）\n  ↓\n"+d.top.id+" "+d.top.name+
    "\n  ↑ 上流要因候補（未検証）\n"+(d.upstream.length?d.upstream.map(f=>f.id+" "+f.name).join("\n"):"未特定")+
    "\n  ↓\nActionable Root Pain（未確定）\n  ↓\nBusiness Consequence（未確認）" :
    "症状・判断・上流原因を特定する情報が不足しています。";
  s1.append(el("div",path,"flow"));
  addLine(s1,"矢印は原資料の一般化された仮説経路です。今回の顧客について因果関係が確認された意味ではありません。","disclaimer");
  const s2=section(output,"02","原因を判別する質問");
  d.questions.forEach(q=>showQuestion(s2,q));
  if(!d.questions.length) addLine(s2,"未回答の候補質問はありません。");
  const s3=section(output,"03","不足している判断情報");
  addList(s3,["対象Capability Cellと決定責任者","現行の作業・回避策・Data / Tool","Lead Time・品質・リスクのBaseline","原因の改善可能性と測定可能性"]);
}
function showProposal() {
  output.replaceChildren();
  const d=state.diagnosis, cell=current();
  const items=[
    ["背景","入力情報を参照（顧客事実としての確認は未実施）"],
    ["現状の困り事",state.messages.map(m=>m.text).join(" / ")],
    ["課題構造",d.top ? d.top.id+" "+d.top.name+"（直接Painの仮説）":"未確認"],
    ["改善対象Engineering Decision",d.top?d.top.decision+"（候補）":"未確認"],
    ["Actionable Root Pain","未確定：原因の改善可能性を要検証"],
    ["改善アプローチ","業務・責任・ルール改善→既存Tool→必要時にAIを比較（具体策は未確認）"],
    ["AI・MBSE・MBD・CAE・Toolの役割","未確認：対象業務と利用中のToolを確認後に分担"],
    ["PoC候補","優先する原因仮説を一つ選び、設計判断に対する改善効果を測る（仮案）"],
    ["KPI","未確認：Decision Lead Time、手戻り、判断漏れ等のBaseline取得が必要"],
    ["Projected Bottleneck","未確認：AI等の施策選定後に再評価"],
    ["本番化条件","未確認：人の承認、品質評価、証跡、構成管理、セキュリティ"],
    ["次の確認事項",d.questions.map(q=>q.question).join(" / ")||"追加情報を入力してください"],
    ["Offering候補",cell.offering_hypotheses.map(o=>o.offering_family).join(" + ")+"（適用判断は未実施）"]
  ];
  items.forEach(([title,value],i)=>{
    const s=section(output,String(i+1).padStart(2,"0"),title);
    addLine(s,value||"未確認");
  });
  addLine(output,"この提案骨子は定型項目への投影です。LLMによる提案生成ではありません。","disclaimer");
}
function showPoc() {
  output.replaceChildren();
  const d=state.diagnosis;
  const items=[
    ["検証したい仮説",d.top ? d.top.name+" が判断業務のボトルネックとなっているかを検証する（候補）":"未確認"],
    ["Baseline","未測定：現行Lead Time・品質・手戻りの記録が必要"],
    ["Target Decision",d.top?d.top.decision:"未確認"],
    ["Input Data / Model / Tool","未確認：顧客の利用可能なデータと権限を棚卸し"],
    ["AI / Automation Scope","未定：No-AI、既存Tool、Native AI、専用AIを比較"],
    ["Human Review","必須：顧客の担当者・承認者は未確認"],
    ["Evaluation","現行手順と候補手法を、同条件・同データで比較"],
    ["Acceptance Criteria","未設定：精度・速度・誤判定・レビュー工数の基準値が必要"],
    ["Projected Bottleneck","未確認：局所自動化後に残る判断・レビュー負荷を測定"],
    ["Production Path","未確認：権限・運用責任・安全性と正本更新範囲の定義"],
    ["Exit Criteria","未設定：継続・見直し・中止の判定基準を事前合意"]
  ];
  items.forEach(([title,value],i)=>{
    const s=section(output,String(i+1).padStart(2,"0"),title);addLine(s,value);
  });
  addLine(output,"これはPoC設計のチェックリスト投影であり、効果検証済みの計画ではありません。","disclaimer");
}
function renderResults() {
  if(!state.snapshot) return;
  const byView={hypothesis:showHypothesis,causal:showCausal,proposal:showProposal,poc:showPoc};
  byView[state.view]();
  byId("export-btn").disabled=false;
  byId("copy-btn").disabled=false;
}
function renderFeed() {
  feed.replaceChildren();
  feed.append(el("div","対象部門、製品・システム、開発上の困り事、今の対応方法など、分かっている範囲で教えてください。未確認情報でも構いません。","message assistant"));
  for(const m of state.messages){
    const bubble=el("div",null,"message user");
    bubble.append(el("span",m.question ? "回答： "+m.question : "入力 "+m.id,"message-meta"),document.createTextNode(m.text));
    feed.append(bubble);
  }
  if(state.diagnosis){
    const text=state.diagnosis.top ?
      "暫定分類： "+state.diagnosis.top.id+" "+state.diagnosis.top.name+"。原因はまだ確定していません。右側の質問に回答すると仮説を更新します。" :
      "現在の文章から具体的なPainを分類できませんでした。右側に、次に確認したい項目を表示しています。";
    feed.append(el("div",text,"message assistant"));
  }
  feed.scrollTop=feed.scrollHeight;
}
function setStatus(message) { status.textContent=message||""; }
function submit() {
  const text=input.value.trim();
  if(!text){setStatus("案件情報または質問への回答を入力してください。");input.focus();return;}
  const question=state.pendingQuestion;
  state.messages.push({id:"SRC-"+(state.messages.length+1),text,question:question?.question||null});
  if(question && !state.answeredIds.includes(question.id)) state.answeredIds.push(question.id);
  const previous=state.diagnosis?.top?.id||null;
  state.diagnosis=evaluate(state.messages,state.answeredIds);
  const current=state.diagnosis.top?.id||null;
  state.history.push({
    timestamp:new Date().toISOString(),element_id:"PAIN-"+(current||"unknown"),
    change:state.history.length===0?"created":"revised",
    reason:previous && previous!==current ? "追加入力により直接Pain候補が変更された" : "入力を追加して仮説を再計算（妥当性確認ではない）"
  });
  state.snapshot=makeSnapshot(state.messages,state.answeredIds,state.diagnosis,state.history,state.opportunityId);
  state.pendingQuestion=null;
  target.hidden=true;
  target.textContent="";
  input.value="";
  input.placeholder="状況の追加情報または次の質問への回答を入力してください";
  setStatus("暫定仮説を更新しました。確度は未評価です。");
  renderFeed();
  renderResults();
}
function contentAsMarkdown() {
  const d=state.diagnosis;
  if(!d) return "";
  const cell=current();
  const lines=["# Engineering Discovery — 暫定スナップショット","",
    "**方式**：ブラウザ内ルールベース（LLM未使用）",
    "**根拠**：ユーザー入力は未検証情報。診断は仮説であり、確定事実ではない。","",
    "## 入力情報"];
  state.messages.forEach(m=>lines.push("- "+m.text));
  lines.push("","## Direct Pain 候補");
  if(!d.direct.length)lines.push("- 未特定");
  d.direct.forEach(f=>lines.push("- "+f.id+" "+f.name+"（候補）"));
  lines.push("","## Engineering Decision",d.top ? "- "+d.top.decision+"（仮説）" : "- 未確認",
    "","## 上流原因候補");
  if(!d.upstream.length)lines.push("- 未確認");
  d.upstream.forEach(f=>lines.push("- "+f.id+" "+f.name+"（未検証）"));
  lines.push("","## Actionable Root Pain","- 未確定：改善可能性と測定可能性を要検証",
    "","## 次に確認すること");
  d.questions.forEach(q=>lines.push("- "+q.question+"（理由："+q.why+"）"));
  if(!d.questions.length)lines.push("- 未回答の候補質問なし");
  lines.push("","## AI必要性","- 未判断。No-AI代替との比較が必要。",
    "","## Offering候補","- "+cell.offering_hypotheses.map(o=>o.offering_family).join(" + ")+"（候補）",
    "","## Projected Bottleneck / Authority","- 未評価／未定義");
  return lines.join("\n");
}
function exportJSON() {
  if(!state.snapshot)return;
  const json=JSON.stringify(state.snapshot,null,2);
  const url=URL.createObjectURL(new Blob([json],{type:"application/json;charset=utf-8"}));
  const anchor=document.createElement("a");anchor.href=url;anchor.download="engineering-opportunity-snapshot.json";
  document.body.append(anchor);anchor.click();anchor.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
  setStatus("Opportunity Data候補をJSONで出力しました。");
}
async function copyMarkdown() {
  if(!state.snapshot)return;
  try {await navigator.clipboard.writeText(contentAsMarkdown());setStatus("診断スナップショットをコピーしました。");}
  catch {setStatus("クリップボードへのコピーが拒否されました。HTTPS接続とブラウザ権限を確認してください。");}
}
function reset() {
  if(state.messages.length && !window.confirm("入力内容と暫定仮説を破棄して新しい案件を開始しますか？"))return;
  Object.assign(state,{messages:[],answeredIds:[],history:[],diagnosis:null,snapshot:null,view:"hypothesis",pendingQuestion:null,opportunityId:"OP-"+Date.now().toString(36)});
  input.value="";target.hidden=true;target.textContent="";
  byId("export-btn").disabled=true;byId("copy-btn").disabled=true;
  output.replaceChildren();
  const empty=el("div",null,"empty");
  empty.append(el("div","◎","empty-icon"),el("h3","最初の入力を待っています"),el("p","文章を受け取ると、仮説と追加の確認事項を生成します。"));
  output.append(empty);
  tabs.forEach(t=>{const active=t.dataset.view==="hypothesis";t.classList.toggle("active",active);t.setAttribute("aria-pressed",String(active));});
  setStatus("");
  renderFeed();
}
tabs.forEach(tab=>tab.addEventListener("click",()=>{
  state.view=tab.dataset.view;
  tabs.forEach(t=>{const active=t===tab;t.classList.toggle("active",active);t.setAttribute("aria-pressed",String(active));});
  renderResults();
}));
byId("analyze-btn").addEventListener("click",submit);
byId("sample-btn").addEventListener("click",()=>{
  input.value="架空の車載ECU開発部署。派生機種が増え、仕様変更後の回帰テスト範囲が分からず、テストケース作成に時間がかかっている。MBDを利用しているが変更影響の追跡方法は未確認。";
  input.focus();
  setStatus("架空サンプルです。ボタンを押して分析を開始してください。");
});
byId("reset-btn").addEventListener("click",reset);
byId("export-btn").addEventListener("click",exportJSON);
byId("copy-btn").addEventListener("click",copyMarkdown);
input.addEventListener("keydown",event=>{
  if((event.ctrlKey||event.metaKey) && event.key==="Enter"){event.preventDefault();submit();}
});
