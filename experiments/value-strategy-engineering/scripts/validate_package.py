#!/usr/bin/env python3
"""Verify hashes, source examples and generated files of a VSE distribution package."""
import hashlib
import json
import sys
from pathlib import Path
from validate_vse import validate_model

ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    err=[]
    manifest_file=ROOT/'package_manifest.json'
    if not manifest_file.is_file():
        print('ERROR: no package_manifest.json');return 1
    manifest=json.loads(manifest_file.read_text(encoding='utf-8'))
    listed={x['path']:x for x in manifest['files']}
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name!='package_manifest.json'}
    if set(listed)!=actual:err.append(f'ファイル一覧不一致 missing={set(listed)-actual} extras={actual-set(listed)}')
    for rel,x in listed.items():
        p=ROOT/rel
        if not p.is_file():err.append(f'missing {rel}');continue
        if sha(p)!=x['sha256']:err.append(f'hash mismatch {rel}')
    required=[item['path'] for item in json.loads((ROOT/'03_OUTPUT_CONTRACT.json').read_text(encoding='utf-8'))['required_files']]
    for example in ('b2b_alm','consumer_product'):
        sub=ROOT/'examples'/example
        m=json.loads((sub/'10_vse_model.json').read_text(encoding='utf-8'))
        result=validate_model(m,require_jsonschema=True)
        if not result['ok']:err.extend(result['errors'])
        for name in required:
            if not (sub/'candidate_bundle'/name).exists():err.append(f'missing {example}/{name}')
        if (sub/'candidate_bundle/10_vse_model.json').read_bytes() != (sub/'10_vse_model.json').read_bytes():
            err.append(f'{example}: source model vs projection model mismatch')
    print('PASS' if not err else 'FAIL',f'files={len(actual)}',f'errors={len(err)}')
    for item in err:print('ERROR:',item)
    return 0 if not err else 1

if __name__=='__main__':sys.exit(main())
