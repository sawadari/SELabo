import test from "node:test";
import assert from "node:assert/strict";
import { evaluate, makeSnapshot } from "../../../docs/engineering-discovery-chat/engine.js";

const sample=[{id:"SRC-1",text:"架空の車載ECU開発部署で派生機種が増え、変更影響を追跡できず回帰テストに時間がかかる"}];

test("unknown input returns questions without pretending to diagnose",()=>{
  const d=evaluate([{id:"SRC-1",text:"困っています"}]);
  assert.equal(d.direct.length,0);
  assert.ok(d.questions.length>=1 && d.questions.length<=3);
});
test("test/change symptoms yield explicit hypotheses within limits",()=>{
  const d=evaluate(sample);
  assert.ok(d.direct.some(f=>f.id==="F10"));
  assert.ok(d.direct.some(f=>f.id==="F6"));
  assert.ok(d.direct.length<=3);
  assert.ok(d.upstream.length<=4);
  assert.ok(d.questions.length<=3);
});
test("previously answered question is not asked again",()=>{
  const d=evaluate(sample);
  const asked=d.questions[0].id;
  const updated=evaluate(sample,[asked]);
  assert.equal(updated.questions.some(q=>q.id===asked),false);
});
test("Opportunity Data preserves user input as unconfirmed and keeps AI undecided",()=>{
  const d=evaluate(sample);
  const snapshot=makeSnapshot(sample,[],d,[],"CASE-1");
  for(const key of ["meta","capability_cells","unknowns"]) assert.ok(Object.hasOwn(snapshot,key));
  const cell=snapshot.capability_cells[0];
  assert.equal(cell.symptoms[0].origin,"user_candidate");
  assert.equal(cell.symptoms[0].confidence,"low");
  assert.equal(cell.ai_applicability.necessity,"undetermined");
  assert.equal(cell.authority_assurance.level,"undetermined");
  assert.deepEqual(cell.actionable_root_pains,[]);
  assert.deepEqual(cell.kpis,[]);
});
test("AI as a word alone does not imply a pain or prescribe AI",()=>{
  const d=evaluate([{id:"SRC-1",text:"AIを使いたい"}]);
  assert.equal(d.direct.length,0);
});
test("unknowns retain answered status",()=>{
  const d=evaluate(sample,["F6-1"]);
  const s=makeSnapshot(sample,["F6-1"],d,[],"CASE-1");
  const question=s.unknowns.find(q=>q.id==="F6-1");
  assert.equal(question?.status,"answered");
});
