import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.plan_keywords import plan, prepare, overlap, norm_url, write_outputs
ROOT=Path(__file__).resolve().parents[1]

class EvidenceWorkflowTests(unittest.TestCase):
    def setUp(self): self.data=json.loads((ROOT/'examples/intake-case/input.json').read_text())
    def test_case_groups_aliases_and_routes_inventory(self):
        p=plan(self.data)
        self.assertEqual(p['input_rows'],10); self.assertEqual(p['unique_keywords'],9)
        d=next(d for d in p['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(set(d['input_ids']),{'K1','K2','K9'})
        self.assertEqual((d['decision'],d['target']),('review_existing','/guides/client-onboarding'))
    def test_capacity_selects_priority_not_volume(self):
        p=plan(self.data);new=[d for d in p['decisions'] if d['decision']=='new']
        self.assertEqual(len(new),1);self.assertEqual(new[0]['input_ids'],['K4'])
        self.data['monthly_new_page_capacity']=0
        self.assertEqual(plan(self.data)['new_pages'],0)
    def test_every_input_is_represented_once(self):
        ids=[i for d in plan(self.data)['decisions'] for i in d['input_ids']]
        self.assertCountEqual(ids,[r['id'] for r in self.data['keywords']])
    def test_context_mismatch_is_unknown_not_zero(self):
        p=plan(self.data);pair=next(p for p in p['pairs'] if p['a']=='K1' and p['b']=='K8')
        self.assertIsNone(pair['shared_top10']); self.assertEqual(pair['relation'],'incompatible_context')
    def test_incomplete_snapshot_does_not_use_threshold(self):
        self.data['keywords'][3]['serp']['organic_urls']=self.data['keywords'][3]['serp']['organic_urls'][:8]
        d=next(d for d in plan(self.data)['decisions'] if 'K4' in d['input_ids'])
        self.assertEqual(d['decision'],'defer');self.assertIn('incomplete',d['reason'])
    def test_navigation_and_mixed_intent_are_deferred(self):
        for d in plan(self.data)['decisions']:
            if d['intent'] in {'navigational','mixed'}: self.assertEqual(d['decision'],'defer')
    def test_conflicting_duplicate_rejected(self):
        self.data['keywords'][8]['intent']='commercial'
        with self.assertRaisesRegex(ValueError,'conflicting duplicate'):plan(self.data)
    def test_two_inventory_targets_require_review(self):
        self.data['existing_pages'].append(dict(path='/old-guide',title='Old',keyword_ids=['K2']))
        d=next(d for d in plan(self.data)['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(d['decision'],'defer');self.assertIsNone(d['target'])
    def test_no_transitive_chain_merge(self):
        data=copy.deepcopy(self.data);data['keywords']=data['keywords'][:3];data['existing_pages']=[]
        sets=[range(1,11),range(4,14),range(7,17)] # A-B=7, B-C=7, A-C=4
        for r,nums in zip(data['keywords'],sets):
            r['serp']['organic_urls']=[f'https://search.example/{n}' for n in nums]
        groups=[set(d['input_ids']) for d in plan(data)['decisions']]
        self.assertIn({'K1','K2'},groups);self.assertIn({'K3'},groups)
    def test_distinct_intents_do_not_auto_merge(self):
        self.data['keywords'][3]['serp']=copy.deepcopy(self.data['keywords'][0]['serp'])
        self.assertFalse(any('K1' in d['input_ids'] and 'K4' in d['input_ids'] for d in plan(self.data)['decisions']))
    def test_normalizer_preserves_meaningful_query_and_path_case(self):
        self.assertEqual(norm_url('https://EXAMPLE.com/A/?product=1&utm_source=x#heading'),'https://example.com/A?product=1')
        self.assertNotEqual(norm_url('https://example.com/?p=1'),norm_url('https://example.com/?p=2'))
        self.assertNotEqual(norm_url('https://example.com/A'),norm_url('https://example.com/a'))
    def test_credentials_not_allowed_in_url(self):
        with self.assertRaises(ValueError):norm_url('https://name:password@example.com/')
    def test_repeated_urls_do_not_inflate_overlap(self):
        self.data['keywords'][3]['serp']['organic_urls']=['https://same.example/a']*10
        row=next(r for r in prepare(self.data) if r['id']=='K4')
        self.assertEqual(len(row['urls']),1)
        self.assertEqual(next(d for d in plan(self.data)['decisions'] if 'K4' in d['input_ids'])['decision'],'defer')
    def test_unknown_source_fails(self):
        self.data['keywords'][0]['source_id']='MISSING'
        with self.assertRaisesRegex(ValueError,'unknown keyword source'):plan(self.data)
    def test_synthetic_cannot_be_marked_real(self):
        self.data['fictional']=False
        with self.assertRaisesRegex(ValueError,'synthetic sources'):plan(self.data)
    def test_boolean_capacity_is_not_integer(self):
        self.data['monthly_new_page_capacity']=True
        with self.assertRaisesRegex(ValueError,'capacity'):plan(self.data)
    def test_output_refuses_to_overwrite_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            p=plan(self.data);write_outputs(self.data,p,d)
            with self.assertRaisesRegex(ValueError,'nonempty'):write_outputs(self.data,p,d)
    def test_new_path_does_not_collide_inventory(self):
        self.data['existing_pages'].append(dict(path='/guides/client-onboarding-software-comparison',title='Other',keyword_ids=[]))
        p=plan(self.data)
        d=next(d for d in p['decisions'] if d['decision']=='new')
        self.assertNotIn(d['target'],[p['path'] for p in self.data['existing_pages']])
    def test_threshold_boundaries(self):
        rows=prepare(self.data);a,b=rows[0],rows[1]
        for n,expected in [(0,'separate'),(1,'separate'),(2,'cross_link_candidate'),(3,'cross_link_candidate'),(4,'topic_candidate'),(6,'topic_candidate'),(7,'same_page_candidate'),(10,'same_page_candidate')]:
            b['urls']=set(list(sorted(a['urls']))[:n])|{f'https://new.example/{i}' for i in range(10-n)}
            self.assertEqual(overlap(a,b),(n,expected))
    def test_omitted_serp_is_normalized_to_missing(self):
        del self.data['keywords'][3]['serp']
        d=next(d for d in plan(self.data)['decisions'] if 'K4' in d['input_ids'])
        self.assertEqual(d['decision'],'defer')
        self.assertIn('missing',d['reason'])
    def test_reproducible(self): self.assertEqual(plan(self.data),plan(copy.deepcopy(self.data)))

if __name__=='__main__':unittest.main()
