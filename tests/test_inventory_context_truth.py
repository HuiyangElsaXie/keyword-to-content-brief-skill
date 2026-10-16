"""Independent synthetic regression tests: inventory is evidence, not publish authority."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from scripts import cluster_workflow as cw

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'cases/inventory-context-repair'

def fixture(name):
    return json.loads((CASES / (name + '.input.json')).read_text())

class InventoryContextTruthTests(unittest.TestCase):
    def test_sufficient_existing_url_is_one_retained_work_item(self):
        p = cw.build_plan(fixture('portfolio-existing'))
        self.assertEqual(len(p['pages']), 1)
        self.assertEqual(p['pages'][0]['status'], 'retain')
        self.assertCountEqual(p['pages'][0]['candidate_ids'], ['R1', 'R2'])
        self.assertEqual(p['links'], [])

    def test_portfolio_commercial_intent_is_not_shopping_comparison(self):
        p = cw.build_plan(fixture('portfolio-existing'))
        self.assertTrue(all(x['template'] != 'comparison' for x in p['pages']))
        self.assertTrue(all(x['word_target'] is None for x in p['pages']))

    def test_context_next_action_is_propagated_without_conversion_override(self):
        d = fixture('portfolio-existing')
        d['business_context']['conversion_definition'] = 'Count only independently verified interview invitations.'
        p = cw.build_plan(d)
        for page in p['pages']:
            self.assertEqual(page['next_action'], d['business_context']['next_action'])
            text = cw.brief(p, page)
            self.assertIn(d['business_context']['next_action'], text)
            self.assertIn(d['business_context']['conversion_definition'], text)

    def test_editorial_next_action_has_precedence(self):
        d = fixture('portfolio-existing')
        d['candidates'][0]['editorial'] = {'next_action':'Inspect the methods appendix first.'}
        p = cw.build_plan(d)
        self.assertEqual(p['pages'][0]['next_action'], 'Inspect the methods appendix first.')

    def test_nonportfolio_existing_mapping_also_blocks_new_pages(self):
        p = cw.build_plan(fixture('marine-existing'))
        mapped = next(x for x in p['pages'] if 'M1' in x['candidate_ids'])
        self.assertEqual(mapped['status'], 'review_existing')
        self.assertTrue(all(x['status'] != 'new_proposal' for x in p['pages']))
        self.assertEqual(p['links'], [])

    def test_missing_and_partial_inventory_do_not_establish_absence(self):
        for name in ('missing-inventory', 'partial-inventory'):
            with self.subTest(name=name):
                p = cw.build_plan(fixture(name))
                self.assertTrue(all(x['status'] == 'defer' for x in p['pages']))
                self.assertEqual(p['links'], [])

    def test_complete_inventory_without_cited_gap_does_not_justify_page(self):
        d = fixture('complete-new-gap')
        d['candidates'][0].pop('new_page_evidence')
        self.assertEqual(cw.build_plan(d)['pages'][0]['status'], 'defer')

    def test_justified_new_gap_and_new_site_remain_proposable(self):
        for name in ('complete-new-gap', 'explicit-new-site'):
            with self.subTest(name=name):
                p = cw.build_plan(fixture(name))
                self.assertEqual(p['pages'][0]['status'], 'new_proposal')
                self.assertEqual(p['publication_status'], 'not_executed')
                self.assertIsNone(cw.scorecard(p)['published_pages'])

    def test_normalized_term_match_is_review_not_coverage(self):
        d = fixture('portfolio-existing')
        for c in d['candidates']: c.pop('existing_page')
        p = cw.build_plan(d)
        self.assertTrue(all(x['status'] == 'review_existing' for x in p['pages']))
        self.assertIsNone(cw.scorecard(p)['actual_coverage'])

    def test_same_url_tracking_alias_is_not_duplicate_proposal(self):
        d = fixture('portfolio-existing')
        d['candidates'][1]['existing_page']['url'] += '?utm_source=fictional#methods'
        p = cw.build_plan(d)
        self.assertEqual(len(p['pages']), 1)
        self.assertEqual(p['links'], [])

    def test_semantic_overlap_is_not_claimed_resolved_by_exact_keywords(self):
        d = fixture('portfolio-existing')
        d['candidates'][1]['keyword'] = 'research work samples for hiring'
        d['candidates'][1].pop('existing_page')
        p = cw.build_plan(d)
        unresolved = next(x for x in p['pages'] if 'R2' in x['candidate_ids'])
        self.assertIn(unresolved['status'], ('defer', 'review_existing'))
        s = cw.scorecard(p)
        self.assertIsNone(s['actual_coverage'])
        self.assertIsNone(s['measured_content_gaps'])
        # A zero exact-key duplicate count must not assert semantic disjointness.
        self.assertNotEqual(s.get('semantic_overlap_resolved'), True)

    def test_unknown_serp_and_volume_stay_null(self):
        p = cw.build_plan(fixture('portfolio-existing'))
        self.assertTrue(all(v is None for row in p['serp_matrix']['scores'] for v in row))
        self.assertTrue(all(pair['shared_top10'] is None for pair in p['pairs']))
        self.assertTrue(all(page['volume'] is None for page in p['pages']))

    def test_partial_coverage_on_duplicate_destination_cannot_become_retain(self):
        d = fixture('portfolio-existing')
        d['candidates'][1]['existing_page']['coverage'] = 'partial'
        p = cw.build_plan(d)
        self.assertEqual(len(p['pages']), 1)
        self.assertEqual(p['pages'][0]['status'], 'review_existing')

    def test_missing_inventory_is_explicitly_unknown_not_complete_empty(self):
        p = cw.build_plan(fixture('missing-inventory'))
        self.assertEqual(p['inventory_status'], 'unknown')
        self.assertEqual(p['existing_page_inventory']['status'], 'unknown')
        self.assertFalse(cw.scorecard(p)['execution_approved'])

    def test_inventory_duplicate_url_does_not_create_duplicate_destinations(self):
        d = fixture('portfolio-existing')
        for c in d['candidates']: c.pop('existing_page')
        duplicate = copy.deepcopy(d['existing_page_inventory']['pages'][0])
        duplicate['url'] += '?utm_campaign=fictional'
        d['existing_page_inventory']['pages'].append(duplicate)
        p = cw.build_plan(d)
        self.assertEqual(len(p['pages']), 1)
        self.assertEqual(cw.scorecard(p)['normalized_existing_destination_count'], 1)
        self.assertEqual(p['pages'][0]['status'], 'review_existing')

    def test_distinct_review_destinations_never_receive_automatic_graph_links(self):
        d = fixture('portfolio-existing')
        d['candidates'][1]['existing_page']['url'] = 'https://portfolio.example/work/interviews'
        d['candidates'][1]['existing_page']['coverage'] = 'unknown'
        p = cw.build_plan(d)
        self.assertEqual(len(p['pages']), 2)
        self.assertEqual(p['links'], [])
        report = cw.scorecard(p)
        self.assertIsNone(report['all_reachable_within_two_clicks'])
        self.assertEqual(report['reachable_within_two_clicks'], [])
        self.assertEqual(report['planned_orphans'], [])
        self.assertTrue(all(page['role'] not in ('pillar', 'spoke') for page in p['pages']))

    def test_existing_review_without_metadata_does_not_suggest_replacement(self):
        p = cw.build_plan(fixture('portfolio-existing'))
        text = cw.brief(p, p['pages'][0])
        self.assertNotIn('Explore design research portfolio for', text)

    def test_supplied_mapping_assertions_are_not_independent_verification(self):
        p = cw.build_plan(fixture('portfolio-existing'))
        self.assertIn('not independent verification', ' '.join(p['warnings']))
        self.assertIsNone(cw.scorecard(p)['actual_coverage'])
        self.assertFalse(cw.scorecard(p)['execution_approved'])

    def test_unknown_mapping_source_rejected(self):
        d = fixture('portfolio-existing')
        d['candidates'][0]['existing_page']['source_id'] = 'MISSING'
        with self.assertRaises(ValueError): cw.build_plan(d)

    def test_unknown_gap_source_rejected(self):
        d = fixture('complete-new-gap')
        d['candidates'][0]['new_page_evidence']['source_id'] = 'MISSING'
        with self.assertRaises(ValueError): cw.build_plan(d)

    def test_cli_legacy_page_mapping_is_consumed_as_unknown_coverage(self):
        d = fixture('portfolio-existing')
        for c in d['candidates']: c.pop('existing_page')
        d.pop('existing_page_inventory')
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td/'input.json').write_text(json.dumps(d))
            (td/'mapping.json').write_text(json.dumps([{'candidate_id':c['id'],'existing_url':'https://portfolio.example/work/research'} for c in d['candidates']]))
            run = subprocess.run([sys.executable,str(ROOT/'scripts/cluster_workflow.py'),'plan','--input',str(td/'input.json'),'--page-mapping',str(td/'mapping.json'),'--out',str(td/'result')], capture_output=True,text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            p = json.loads((td/'result/cluster-plan.json').read_text())
            self.assertEqual(len(p['pages']), 1)
            self.assertEqual(p['pages'][0]['status'], 'review_existing')
            self.assertEqual(p['links'], [])
            self.assertEqual(cw.load_plan(td/'result/cluster-plan.json'), p)

if __name__ == '__main__':
    unittest.main()
