"""Offline structural tests of the sample data and validator safety invariants."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_vse import validate_model
from render_projections import render

class VseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b2b=json.loads((ROOT/'examples/b2b_alm/10_vse_model.json').read_text(encoding='utf-8'))
        cls.consumer=json.loads((ROOT/'examples/consumer_product/10_vse_model.json').read_text(encoding='utf-8'))

    def test_two_synthetic_examples_pass_structure(self):
        for model in [self.b2b,self.consumer]:
            self.assertTrue(validate_model(model,require_jsonschema=True)['ok'])
            self.assertTrue(model['meta']['synthetic_case'])

    def test_relation_to_nonexistent_id_rejected(self):
        d=copy.deepcopy(self.b2b)
        d['relations'][0]['target_id']='PRB-9999'
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_wrong_direction_rejected(self):
        d=copy.deepcopy(self.b2b)
        d['relations'][8]['source_id']='HYP-0001'
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_ai_observation_promotion_rejected(self):
        d=copy.deepcopy(self.b2b)
        d['hypotheses'][0]['claim_state']='observed'
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_approved_decision_without_human_rejected(self):
        d=copy.deepcopy(self.b2b)
        d['decisions'][0]['decision_status']='approved'
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_causal_relation_missing_status_rejected(self):
        d=copy.deepcopy(self.b2b)
        for rel in d['relations']:
            if rel['relation_type']=='causally_influences':rel.pop('causal_status')
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_causal_experimentally_estimated_without_completed_experiment_rejected(self):
        d=copy.deepcopy(self.b2b)
        for rel in d['relations']:
            if rel['relation_type']=='causally_influences':rel['causal_status']='experimentally_estimated'
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_no_status_quo_rejected(self):
        d=copy.deepcopy(self.b2b)
        d['alternatives']=[a for a in d['alternatives'] if a['option_kind']!='status_quo']
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_synthetic_source_cannot_be_marked_real(self):
        d=copy.deepcopy(self.b2b)
        d['source_fragments'][0]['is_synthetic']=False
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_missing_hypothesis_falsification_rejected(self):
        d=copy.deepcopy(self.b2b)
        d['hypotheses'][0]['falsification_condition']=''
        self.assertFalse(validate_model(d,require_jsonschema=True)['ok'])

    def test_render_17_files_and_relations_are_source_projection(self):
        report=validate_model(self.b2b,require_jsonschema=True)
        with tempfile.TemporaryDirectory() as tmp:
            files=render(self.b2b,Path(tmp),report)
            self.assertEqual(len(files),17)
            self.assertTrue(all((Path(tmp)/p).exists() for p in files))
            proj=json.loads((Path(tmp)/'10_vse_model.json').read_text(encoding='utf-8'))
            self.assertEqual(proj,self.b2b)
            csv_text=(Path(tmp)/'09_traceability.csv').read_text(encoding='utf-8-sig')
            self.assertIn('causally_influences',csv_text)
            manifest=json.loads((Path(tmp)/'16_generation_manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(len(manifest['files']),16)

    def test_no_actual_customer_measurements_in_examples(self):
        for d in [self.b2b,self.consumer]:
            self.assertFalse(any(x['observation_status']=='observed' for x in d['outcomes']))
            self.assertFalse(any(x['decision_status']=='approved' for x in d['decisions']))
            self.assertFalse(any(x['status']=='completed' for x in d['experiments']))

if __name__=='__main__':unittest.main()
