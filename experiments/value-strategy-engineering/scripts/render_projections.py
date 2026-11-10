#!/usr/bin/env python3
"""Project VSE candidate JSON into an inspectable candidate bundle. No LLM or network."""
import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from validate_vse import validate_model

ROOT=Path(__file__).resolve().parents[1]
OUTPUT_CONTRACT=json.loads((ROOT/'03_OUTPUT_CONTRACT.json').read_text(encoding='utf-8'))


def esc(t):
    return str(t).replace('|','\\|').replace('\n',' ')

def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+''.join('| '+' | '.join(map(esc,r))+' |\n' for r in rows)

def item_table(items, extra=None):
    if not items: return '（候補なし。未調査である可能性がある）\n'
    headers=['ID','名称','概要','出自','状態']+(extra[0] if extra else [])
    rows=[]
    for a in items:
        r=[a['id'],a['title'],a['description'],a['origin'],a['claim_state']+' / '+a['decision_state']]
        if extra:r += [str(a.get(key,'未確認')) for key in extra[1]]
        rows.append(r)
    return table(headers,rows)

def block(title,content):return '## '+title+'\n\n'+content+'\n'

def header(title,model):
    return f'# {title}\n\n> **候補データからの自動投影**｜対象：{model["meta"]["target_subject"]}｜実顧客・市場の実証結果ではない。\n\n'

def rel_view(model):
    return {r['id']:r for r in model['relations']}

def md_executive(d):
    t=header('VSE 初期レビュー・サマリー',d)
    t+=block('対象と目的',d['scope']['subject']+'\n\n'+d['scope']['purpose'])
    t+=block('対象境界', '**自社側で制御可能**：'+ '、'.join(d['scope']['controlled_by_organization'])+'\n\n**外部で制御できない**：'+'、'.join(d['scope']['external_and_uncontrolled']))
    t+=block('主要な顧客・業務課題',item_table(d['problems']))
    t+=block('主要な仮説',item_table(d['hypotheses'],(['反証条件'],['falsification_condition'])))
    t+=block('比較する代替案（現状維持を含む）',item_table(d['alternatives'],(['案の区分'],['option_kind'])))
    t+=block('大きな未確認事項', '\n'.join('- '+q['id']+'：'+q['question']+'（次の確認：'+q['verification_action']+'）' for q in d['open_questions']) if d['open_questions'] else '未収録')
    t+=block('成熟度と限界',f"Gate：`{d['quality_summary']['gate_state']}`（Tier：`{d['quality_summary']['review_tier']}`）。本サンプルは架空ケースであり、採用済み戦略でも市場実証でもない。\n\n未実施："+'、'.join(d['quality_summary']['not_performed']))
    return t

def md_actors(d):
    t=header('関係者・エコシステム',d)
    t+=block('関係者候補',item_table(d['actors'],(['境界','購買上の役割'],['control_boundary','buying_role'])))
    t+=block('顧客・外部環境の境界','外部Actorは自社が制御する要素ではない。購買役割は初期仮説であり、実際の組織構造は未確認。')
    return t

def md_problems(d):
    t=header('顧客・業務課題',d)
    t+=block('問題と現状・望ましい姿',item_table(d['problems'],(['現状','望ましい状態'],['current_state','desired_state'])))
    t+=block('購買と利用の分離','課題を認識する利用者と予算決定権者は異なり得る。確認済みの役割のみ確定する。')
    return t

def md_value(d):
    t=header('価値・仮説',d)
    t+=block('価値候補',item_table(d['values'],(['比較基準'],['comparison_baseline'])))
    t+=block('仮説と反証', item_table(d['hypotheses'],(['予測','反証条件','検証方法'],['prediction','falsification_condition','verification_plan'])))
    t+=block('証拠（出自が明確なもののみ）',item_table(d['evidence'],(['検証状態','限界'],['verification_status','limitations'])))
    t+=block('重要な制約','支持する出典があっても仮説の因果効果は証明されない。AIによる候補や仮想顧客の発言は、実顧客の観測と区別する。')
    return t

def md_alts(d):
    t=header('戦略代替案の比較',d)
    t+=block('比較する問題と選択肢',item_table(d['alternatives'],(['比較問題ID','種類','選択状態','トレードオフ'],['comparison_problem_id','option_kind','selection_status','tradeoffs'])))
    t+=block('判断の基準',item_table(d['decisions'],(['比較基準','見直し条件'],['criteria','revisit_trigger'])))
    t+=block('非選択と不確実性','代替案の優劣は仮の比較基準に依存する。採用済みと表示するには人間の決裁と根拠が必要。')
    return t

def md_execution(d):
    t=header('実行・営業・提供体制',d)
    t+=block('施策候補',item_table(d['interventions'],(['対象顧客ID','費用状態'],['target_actor_ids','cost_status'])))
    t+=block('能力と制約',item_table(d['capabilities'],(['利用可能性'],['availability'])))
    t+=block('外部活動の制限','顧客への連絡・実験・施策実行は自動で開始しない。実行前に人間が条件・権限・機密を確認する。')
    return t

def md_validation(d):
    t=header('実験・観測計画',d)
    t+=block('検証候補',item_table(d['experiments'],(['対象仮説','方法','主要指標','判断基準','交絡候補','実施状態'],['target_hypothesis_ids','method','primary_measure','decision_rule','confounders','status'])))
    t+=block('結果（計画と実測を区別）',item_table(d['outcomes'],(['観測状態','値','帰属'],['observation_status','value','attribution_status'])))
    t+=block('因果についての注意','観察や前後比較のみで施策の効果を確定しない。比較群・交絡・測定条件を考慮する。')
    return t

def md_decisions(d):
    t=header('判断記録',d)
    t+=block('判断候補',item_table(d['decisions'],(['判断状態','選択案','決定者ActorID','再評価条件'],['decision_status','chosen_alternative_id','decision_authority_actor_id','revisit_trigger'])))
    return t

def md_risks(d):
    t=header('リスクと仮定',d)
    t+=block('リスク候補',item_table(d['risks'],(['原因','事象','結果','対策候補'],['cause','event','consequence','mitigation_candidate'])))
    uncertain=[x for coll in ['objectives','actors','problems','values','hypotheses','alternatives','capabilities','decisions','interventions'] for x in d.get(coll,[]) if x.get('claim_state')=='assumed']
    t+=block('未検証の仮定',item_table(uncertain))
    return t

def md_quality(d,validation):
    q=d['quality_summary'];t=header('品質検査レポート',d)
    t+=block('Gateと評価Tier',f"Gate：`{q['gate_state']}`、Tier：`{q['review_tier']}`。構造検査成功は戦略成果の保証ではない。")
    t+=block('サンプルモデル内の検査記録',table(['規則','状態','内容'],[[a['rule_id'],a['status'],a['detail']] for a in q['checks']]))
    t+=block('今回の静的検査',f"結果：{'pass' if validation['ok'] else 'fail'} / errors={validation['error_count']} / warnings={validation['warning_count']}\n\n"+'\n'.join('- '+x for x in validation['errors']+validation['warnings']))
    t+=block('未実施検査','\n'.join('- '+x for x in q['not_performed']))
    t+=block('日本語と意味の評価', f"linguistic_quality={q.get('linguistic_quality','not_assessed')} / semantic_validity={q.get('semantic_validity','not_assessed')}")
    return t

def md_backlog(d):
    t=header('人間による確認事項',d)
    t+=block('未解決質問',table(['ID','優先度','質問','確認者候補','確認方法','影響ID'],[
       [x['id'],x['priority'],x['question'],x['owner_role'],x['verification_action'],', '.join(x['impact_refs'])] for x in d['open_questions']]))
    t+=block('権限境界','人間の承認・調査許可・法務判断・顧客連絡はAIが代行しない。')
    return t

def md_graph(d):
    t=header('図の投影仕様',d)
    t+='## 要素と関係のグラフ（候補）\n\n図は全要素の一部のみ示す。因果状態と出典状態はJSONを正本とする。\n\n```mermaid\nflowchart LR\n'
    choices={x['id']:x for coll in ['objectives','problems','hypotheses','alternatives','experiments'] for x in d.get(coll,[])}
    for a in list(choices.values())[:22]:
        label=(a['id']+': '+a['title']).replace('"','').replace('[','').replace(']','')
        t+=f'  {a["id"].replace("-","_")}["{label}"]\n'
    for r in d['relations']:
        if r['source_id'] in choices and r['target_id'] in choices:
            t+=f'  {r["source_id"].replace("-","_")} -->|{r["relation_type"]}| {r["target_id"].replace("-","_")}\n'
    t+='```\n\n## 解釈上の注意\n\nこの図のエッジは型付きの候補関係。`causally_influences`は仮説・観測・実験推定を区別する。図の近接や矢印は因果効果の証明にならない。\n'
    return t

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def render(data:dict, outdir:Path, validation:dict):
    outdir.mkdir(parents=True,exist_ok=True)
    contents={
      '01_executive_summary.md':md_executive(data),
      '02_source_scope_glossary.json':json.dumps({k:data[k] for k in ['source_fragments','scope','glossary']},ensure_ascii=False,indent=2)+'\n',
      '03_stakeholders_ecosystem.md':md_actors(data),
      '04_customer_problems.md':md_problems(data),
      '05_value_and_hypotheses.md':md_value(data),
      '06_strategy_alternatives.md':md_alts(data),
      '07_execution_and_sales.md':md_execution(data),
      '08_validation_plan.md':md_validation(data),
      '11_decision_register.md':md_decisions(data),
      '12_risk_assumption_register.md':md_risks(data),
      '13_quality_report.md':md_quality(data,validation),
      '14_human_confirmation_backlog.md':md_backlog(data),
      '15_visualization_specs.md':md_graph(data)}
    for path,body in contents.items(): (outdir/path).write_text(body,encoding='utf-8')
    # Canonical data. Preservation of the semantic source: this is a literal serialization of supplied data.
    (outdir/'10_vse_model.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (outdir/'09_traceability.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['relation_id','source_id','target_id','relation_type','certainty','causal_status','basis'])
        for r in data['relations']:
            w.writerow([r['id'],r['source_id'],r['target_id'],r['relation_type'],r['certainty'],r.get('causal_status',''),r['basis']])
    expected=[item['path'] for item in OUTPUT_CONTRACT['required_files']]
    man={
       'artifact_type':'vse_candidate_projection_bundle','schema_version':'1.0.0',
       'project_slug':data['meta'].get('project_slug'),'target_subject':data['meta']['target_subject'],
       'source_of_truth':'10_vse_model.json','gate_state':data['quality_summary']['gate_state'],
       'model_generated_at':data['meta']['generated_at'],
       'synthetic_case':data['meta']['synthetic_case'],
       'expected_files':expected,'validation':{'static_validation_ok':validation['ok'],'errors':validation['errors'],
          'unperformed':['実顧客調査','人の正式意思決定','因果効果確認','実在専門家の評価']},
       'limitations':['本レポートは候補データからの機械的投影であり、新たな市場検証ではない。']}
    (outdir/'00_manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    inventory={'manifest_version':'1.0.0','source_of_truth':'10_vse_model.json','model_sha256':sha(outdir/'10_vse_model.json'),
        'files':[{'path':p,'sha256':sha(outdir/p),'size_bytes':(outdir/p).stat().st_size} for p in expected if p != '16_generation_manifest.json'],
        'hash_exclusions':['16_generation_manifest.json (self-reference)']}
    (outdir/'16_generation_manifest.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    missing=[p for p in expected if not (outdir/p).is_file()]
    if missing:raise ValueError('missing output files '+str(missing))
    return expected


def main():
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--strict',action='store_true');args=p.parse_args()
    data=json.loads(args.model.read_text(encoding='utf-8'))
    validation=validate_model(data,require_jsonschema=args.strict)
    if not validation['ok']:
        raise ValueError('Source VSE candidate failed validation: '+' | '.join(validation['errors']))
    files=render(data,args.output_dir,validation)
    print(f'Rendered {len(files)} files to {args.output_dir}')

if __name__=='__main__':main()
