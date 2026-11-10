#!/usr/bin/env python3
"""Validate VSE candidate JSON. No network requests, no external writes.

Usage: python scripts/validate_vse.py examples/b2b_alm/10_vse_model.json --strict
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'schemas/vse_model.schema.json'
RELATION_PATH = ROOT / 'schemas/relation_type_contract.json'
ID_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]*-[0-9]{4,}$')


def validate_model(data: dict[str, Any], *, require_jsonschema: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[str] = []
    try:
        import jsonschema
    except ImportError:
        if require_jsonschema:
            errors.append('JSON Schema検査にはjsonschemaが必要です (pip install jsonschema)')
        else:
            warnings.append('JSON Schema検査は未実施（jsonschemaが未導入）')
    else:
        try:
            schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
            validator = jsonschema.Draft202012Validator(schema)
            for err in sorted(validator.iter_errors(data), key=lambda x: list(map(str, x.absolute_path))):
                errors.append(f'Schema {"/".join(map(str,err.absolute_path))}: {err.message}')
            if not errors:
                checks.append('schema:pass')
        except Exception as e:
            errors.append(f'Schema自体を処理できません: {e}')
    contract = json.loads(RELATION_PATH.read_text(encoding='utf-8'))
    collection_prefix = contract['collection_id_prefix']
    ids: dict[str, str] = {}
    sources: dict[str, Any] = {}
    coll_map: dict[str, dict[str, dict[str,Any]]] = {}
    for src in data.get('source_fragments', []):
        if not isinstance(src, dict):
            errors.append('source_fragmentsにobjectでない項目がある');continue
        srcid=src.get('id')
        if srcid in ids: errors.append(f'ID重複: {srcid}')
        ids[srcid]='source_fragments';sources[srcid]=src
        if not str(srcid).startswith('SRC-'): errors.append(f'ソースIDのprefix不正: {srcid}')
        if not src.get('is_synthetic', True) and src.get('classification')=='embedded_instruction_candidate':
            warnings.append(f'埋込命令候補をデータとして保持: {srcid} （実行しないこと）')
    for collection, prefix in collection_prefix.items():
        coll_map[collection]={}
        for el in data.get(collection, []):
            if not isinstance(el, dict): errors.append(f'{collection}: object以外の要素');continue
            eid=el.get('id')
            if eid in ids: errors.append(f'ID重複: {eid}')
            ids[eid]=collection;coll_map[collection][eid]=el
            if not str(eid).startswith(prefix+'-') or not ID_PATTERN.fullmatch(str(eid)):
                errors.append(f'{collection}のID形式/prefix不正: {eid}')
            for ref in el.get('source_refs',[]):
                if ref not in sources: errors.append(f'{eid}: source_refs不存在: {ref}')
            if el.get('origin')=='user_confirmed' and not el.get('source_refs'):
                errors.append(f'{eid}: user_confirmedに出典が無い')
            if el.get('origin','').startswith('ai_') and el.get('claim_state')=='observed':
                errors.append(f'{eid}: AI推定をobservedと扱っている')
            if el.get('decision_state')=='user_confirmed' and el.get('human_confirmation_required') is True:
                errors.append(f'{eid}: 人確認未了なのにuser_confirmed')
            if el.get('owner_actor_id') is not None and el.get('owner_actor_id') not in data_ids(data.get('actors',[])):
                errors.append(f'{eid}: owner_actor_idが存在しない')
    if data.get('meta',{}).get('synthetic_case'):
        for src in data.get('source_fragments',[]):
            if src.get('is_synthetic') is not True:
                errors.append('synthetic_caseなのにsource_fragmentsに非架空の入力が混在')
        for outcome in data.get('outcomes',[]):
            if outcome.get('observation_status')=='observed':
                warnings.append(f'{outcome.get("id")}: 架空事例にobserved。現実証拠と扱わない')
    for problem in data.get('problems',[]):
        if problem.get('customer_actor_id') not in coll_map['actors']:
            errors.append(f'{problem.get("id")}: customer_actor_idが存在しない')
    for val in data.get('values',[]):
        for aid in val.get('beneficiary_actor_ids', []):
            if aid not in coll_map['actors']: errors.append(f'{val.get("id")}: beneficiary_actor_id不存在: {aid}')
    for alt in data.get('alternatives',[]):
        if alt.get('comparison_problem_id') not in coll_map['problems']:
            errors.append(f'{alt.get("id")}: comparison_problem_idが存在しない')
        if alt.get('selection_status')=='selected_confirmed' and alt.get('decision_state')!='user_confirmed':
            errors.append(f'{alt.get("id")}: selected_confirmedとdecision_stateが矛盾')
    for dec in data.get('decisions',[]):
        ch=dec.get('chosen_alternative_id')
        au=dec.get('decision_authority_actor_id')
        if ch is not None and ch not in coll_map['alternatives']:errors.append(f'{dec.get("id")}: chosen_alternative不存在')
        if au is not None and au not in coll_map['actors']:errors.append(f'{dec.get("id")}: authority_actor不存在')
        if dec.get('decision_status')=='approved':
            if dec.get('decision_state')!='user_confirmed' or au is None or dec.get('human_confirmation_required'):
                errors.append(f'{dec.get("id")}: 承認済みの証拠/責任者状態が不整合')
            if data.get('meta',{}).get('synthetic_case'):
                errors.append(f'{dec.get("id")}: 架空事例で実承認済みを断定')
    for it in data.get('interventions',[]):
        for aid in it.get('target_actor_ids',[]):
            if aid not in coll_map['actors']:errors.append(f'{it.get("id")}: target_actor不存在: {aid}')
        if it.get('execution_owner_id') is not None and it.get('execution_owner_id') not in coll_map['actors']:
            errors.append(f'{it.get("id")}: execution_owner不存在')
    for ev in data.get('evidence',[]):
        if ev.get('source_fragment_id') not in sources:errors.append(f'{ev.get("id")}: source_fragment_id不存在')
        if ev.get('verification_status')=='independently_checked' and sources.get(ev.get('source_fragment_id'),{}).get('is_synthetic'):
            warnings.append(f'{ev.get("id")}: 架空ソースは独立検証された市場根拠にならない')
    for exp in data.get('experiments',[]):
        for hid in exp.get('target_hypothesis_ids',[]):
            if hid not in coll_map['hypotheses']:errors.append(f'{exp.get("id")}: 仮説不存在: {hid}')
        for oid in exp.get('result_outcome_ids',[]):
            if oid not in coll_map['outcomes']:errors.append(f'{exp.get("id")}: 結果Outcome不存在: {oid}')
        if exp.get('status')=='completed' and not exp.get('result_outcome_ids'):
            warnings.append(f'{exp.get("id")}: 完了実験の結果が未記載')
    for item in data.get('open_questions',[]):
        for ref in item.get('impact_refs',[]):
            if ref not in ids:errors.append(f'{item.get("id")}: open_questions impact_refs不存在: {ref}')
    rel_ids=set()
    for rel in data.get('relations',[]):
        rid=rel.get('id')
        if rid in ids or rid in rel_ids:errors.append(f'関係ID重複: {rid}')
        rel_ids.add(rid)
        if not str(rid).startswith('REL-'):errors.append(f'関係ID形式不正: {rid}')
        src,tgt=rel.get('source_id'),rel.get('target_id')
        if src not in ids or tgt not in ids:
            errors.append(f'{rid}: 存在しないsource_id/target_id: {src} -> {tgt}');continue
        if src==tgt:errors.append(f'{rid}: 自己参照を避ける')
        rule=contract['contracts'].get(rel.get('relation_type'))
        if rule is None:errors.append(f'{rid}: 関係型が未定義');continue
        sf,tf=src.split('-')[0],tgt.split('-')[0]
        if '*' not in rule['source'] and sf not in rule['source']:errors.append(f'{rid}: source型が不適切: {sf}')
        if '*' not in rule['target'] and tf not in rule['target']:errors.append(f'{rid}: target型が不適切: {tf}')
        if rel.get('relation_type')=='causally_influences':
            if 'causal_status' not in rel:errors.append(f'{rid}: causal_statusが必要')
            elif rel['causal_status']=='experimentally_estimated' and not any(e.get('status')=='completed' for e in data.get('experiments',[])):
                errors.append(f'{rid}: 完了実験なしにexperimentally_estimated')
        elif rel.get('causal_status') is not None:
            warnings.append(f'{rid}: 因果関係以外にcausal_statusが付いている')
        for sref in rel.get('source_refs',[]):
            if sref not in sources:errors.append(f'{rid}: relation source_refs不存在: {sref}')
    if len(data.get('alternatives',[]))>0 and not any(a.get('option_kind')=='status_quo' for a in data.get('alternatives',[])):
        errors.append('戦略代替案があるのにstatus_quoが無い。除外理由がある場合は人間に確認')
    for exp in data.get('experiments',[]):
        for hid in exp.get('target_hypothesis_ids',[]):
            if not any(r.get('relation_type')=='tests' and r.get('source_id')==exp.get('id') and r.get('target_id')==hid for r in data.get('relations',[])):
                warnings.append(f'{exp.get("id")}: target_hypothesis_ids={hid}のtests関係が無い')
    if data.get('quality_summary',{}).get('gate_state')=='reviewable_40_candidate':
        if not data.get('hypotheses') or not data.get('experiments') or not data.get('decisions') or len(data.get('alternatives',[]))<2:
            errors.append('Gate通過だが重要仮説/実験/比較代替案が不足')
    for collection in ['findings','open_questions','change_log']:
        for item in data.get(collection,[]):
            iid=item.get('id')
            if iid in ids or iid in rel_ids:errors.append(f'{collection}: ID重複 {iid}')
            ids[iid]=collection
            if collection=='change_log' and item.get('target_id') not in ids:  # createdの場合に要素が先に定義されている前提
                errors.append(f'{iid}: change target不存在')
    checks.append('id_and_reference_validation:pass' if not errors else 'id_and_reference_validation:fail')
    warnings.extend([
        '未実施：実在顧客への確認、需要・競合・ROIの実証',
        '未実施：専門家による内容妥当性と独立AI Reviewer',
        '未実施：施策の因果効果・実務成果の検証',
    ])
    return {'ok':not errors,'error_count':len(errors),'warning_count':len(warnings),'errors':errors,'warnings':warnings,'checks':checks,
            'counts':{x:len(data.get(x,[])) for x in collection_prefix}}


def data_ids(items:list[dict[str,Any]])->set[str]:
    return {i.get('id') for i in items if isinstance(i,dict)}


def main():
    p=argparse.ArgumentParser(description='VSE Candidate Model static validator')
    p.add_argument('model',type=Path)
    p.add_argument('--strict',action='store_true',help='require jsonschema installed')
    p.add_argument('--json',action='store_true',help='return JSON report')
    args=p.parse_args()
    try: model=json.loads(args.model.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'ERROR: cannot read JSON: {e}',file=sys.stderr);sys.exit(2)
    report=validate_model(model,require_jsonschema=args.strict)
    if args.json:
        print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print('PASS' if report['ok'] else 'FAIL',f"errors={report['error_count']}",f"warnings={report['warning_count']}")
        for line in report['errors']:print('ERROR:',line)
        for line in report['warnings']:print('NOTE:',line)
    sys.exit(0 if report['ok'] else 1)

if __name__=='__main__': main()
