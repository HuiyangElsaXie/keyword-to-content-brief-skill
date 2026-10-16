import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.plan_keywords import plan, write_outputs
ROOT=Path(__file__).resolve().parents[1]

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'examples/intake-case/input.json').read_text())
    def unknown(self, field):
        self.data['business_context'][field]=dict(status='unknown',value=None,source_ids=[])
    def test_tailored_context_ready(self):
        p=plan(self.data)
        self.assertEqual(p['business_context']['report_mode'],'tailored')
        self.assertEqual(p['business_context']['commissioning_status'],'context_ready')
        self.assertIn('brand_position',p['business_context']['assumptions'])
    def test_missing_context_not_validation_error(self):
        del self.data['business_context']; p=plan(self.data)
        self.assertEqual(p['business_context']['report_mode'],'generic_framework')
        self.assertEqual(p['new_pages'],0)
        self.assertTrue(all(d['business_priority'] is None for d in p['decisions']))
        self.assertLessEqual(len(p['business_context']['next_questions']),3)
    def test_unknown_problem_yields_industry_reference(self):
        self.unknown('business_problem');p=plan(self.data)
        self.assertEqual(p['business_context']['report_mode'],'industry_general')
        self.assertEqual(p['new_pages'],0)
        self.assertTrue(p['guidance']['reference_value'])
    def test_unknown_industry_generic_framework(self):
        self.unknown('industry')
        self.assertEqual(plan(self.data)['business_context']['report_mode'],'generic_framework')
    def test_unknown_objective_industry_general(self):
        self.unknown('primary_objective')
        self.assertEqual(plan(self.data)['business_context']['report_mode'],'industry_general')
    def test_reuse_answers_and_do_not_repeat_explicit_unknown(self):
        self.unknown('business_problem')
        self.assertNotIn('business_problem',[q['field'] for q in plan(self.data)['business_context']['next_questions']])
    def test_conversion_requires_event(self):
        self.data['business_context']['primary_objective']['value']='conversion';self.unknown('conversion_definition')
        p=plan(self.data);self.assertIn('conversion_definition',p['business_context']['missing_for_commission']);self.assertEqual(p['new_pages'],0)
    def test_awareness_does_not_require_conversion_definition(self):
        self.data['business_context']['primary_objective']['value']='awareness';self.unknown('conversion_definition')
        self.assertNotIn('conversion_definition',plan(self.data)['business_context']['missing_for_commission'])
    def test_intake_source_invalid(self):
        self.data['business_context']['industry']['source_ids']=['BAD']
        with self.assertRaisesRegex(ValueError,'source'):plan(self.data)
    def test_supplied_answer_requires_trace(self):
        self.data['business_context']['industry']['source_ids']=[]
        with self.assertRaisesRegex(ValueError,'source'):plan(self.data)
    def test_assumed_objective_cannot_commission(self):
        self.data['business_context']['primary_objective']['status']='assumed'
        self.assertEqual(plan(self.data)['new_pages'],0)
    def test_inventory_does_not_prove_update(self):
        d=next(d for d in plan(self.data)['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(d['decision'],'review_existing')
    def test_gap_plus_context_supports_update(self):
        self.data['existing_pages'][0]['coverage_review']=dict(result='gap',detail='Fictional body excerpt omits approval handoff steps.',source_id='S1')
        d=next(d for d in plan(self.data)['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(d['decision'],'update')
        self.unknown('business_problem')
        d=next(d for d in plan(self.data)['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(d['decision'],'review_existing')
    def test_covered_means_retain(self):
        self.data['existing_pages'][0]['coverage_review']=dict(result='covered',detail='Fictional review finds task already covered.',source_id='S1')
        self.assertEqual(plan(self.data)['decisions'][0]['decision'],'retain')
    def test_same_target_single_brief_without_cluster_claim(self):
        self.data['existing_pages'][0]['keyword_ids'] += ['K3']
        for r in self.data['keywords']:r['serp']=None
        p=plan(self.data);w=next(w for w in p['work_items'] if w['target']=='/guides/client-onboarding')
        self.assertGreater(len(w['group_ids']),1)
        self.assertIn('do not establish',w['keyword_relationship'])
        with tempfile.TemporaryDirectory() as td:
            write_outputs(self.data,p,td)
            self.assertEqual((Path(td)/'brief-scaffolds.md').read_text().count('## /guides/client-onboarding'),1)
    def test_entity_navigation_not_hardcoded_product_help(self):
        self.data['existing_pages'].append(dict(path='/about',title='About the creator',keyword_ids=['K6']))
        d=next(d for d in plan(self.data)['decisions'] if 'K6' in d['input_ids'])
        self.assertEqual(d['target'],'/about');self.assertNotIn('product/help',d['reason'])
    def test_no_priority_rationale_no_commission(self):
        del self.data['keywords'][3]['priority_evidence']
        d=next(d for d in plan(self.data)['decisions'] if 'K4' in d['input_ids'])
        self.assertEqual(d['decision'],'defer');self.assertIsNone(d['business_priority'])
    def test_unknown_priority_accepted(self):
        self.data['keywords'][3]['business_priority']=None
        d=next(d for d in plan(self.data)['decisions'] if 'K4' in d['input_ids'])
        self.assertEqual(d['decision'],'defer')
    def test_objective_mismatch_blocks_prioritization(self):
        self.data['keywords'][3]['priority_evidence']['objective']='conversion'
        d=next(d for d in plan(self.data)['decisions'] if 'K4' in d['input_ids'])
        self.assertEqual(d['decision'],'defer')
    def test_market_mismatch_no_commission(self):
        self.data['business_context']['geography']['value']='CA'
        self.assertEqual(plan(self.data)['new_pages'],0)
    def test_invalid_classification_rejected_without_priority(self):
        self.data['keywords'][3].pop('priority_evidence');self.data['keywords'][3]['brand_scope']='made-up'
        with self.assertRaisesRegex(ValueError,'brand_scope'):plan(self.data)
    def test_lifecycle_separate_from_site_age(self):
        self.data['business_context']['website_stage']['value']='Website 10 years old'
        self.assertEqual(plan(self.data)['guidance']['lifecycle'],'prelaunch')

    def test_missing_audience_industry_general(self):
        self.unknown('audience')
        self.assertEqual(plan(self.data)['business_context']['report_mode'],'industry_general')
    def test_distinct_brand_product_lifecycles(self):
        self.data['business_context']['brand_lifecycle']=dict(status='supplied',value='mature',source_ids=['S1'])
        self.data['business_context']['product_lifecycle']=dict(status='supplied',value='launch',source_ids=['S1'])
        p=plan(self.data)
        self.assertEqual(p['guidance']['brand_lifecycle'],'mature')
        self.assertEqual(p['guidance']['product_lifecycle'],'launch')
