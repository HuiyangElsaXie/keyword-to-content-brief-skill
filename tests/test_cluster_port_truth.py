"""Independent adversarial/regression checks for the Codex cluster port.

No network calls. Synthetic reserved-domain fixtures only. CLI contract tests are
added against the documented new port once its entrypoint is available.
"""
import copy
import json
import unittest
from pathlib import Path
from scripts.plan_keywords import plan

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'cases/codex-cluster-port'

class ClusterEvidenceTruthTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((CASE / 'awareness.input.json').read_text())

    def test_source_provenance_required(self):
        self.data['keywords'][0]['serp']['source_id'] = 'nonexistent'
        with self.assertRaises(ValueError):
            plan(self.data)

    def test_synthetic_source_cannot_be_marked_real(self):
        self.data['fictional'] = False
        with self.assertRaisesRegex(ValueError, 'synthetic'):
            plan(self.data)

    def test_missing_snapshot_prevents_merge_and_commission(self):
        self.data['keywords'][0]['serp'] = None
        p = plan(self.data)
        d = next(d for d in p['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(d['decision'], 'defer')
        self.assertFalse(any({'K1','K2'} <= set(d['input_ids']) for d in p['decisions']))

    def test_context_dimensions_are_each_incomparable(self):
        for field, value in [('date','2026-10-15'),('market','GB'),('device','mobile'),('language','fr')]:
            with self.subTest(field=field):
                d = copy.deepcopy(self.data)
                d['keywords'][1]['serp'][field] = value
                pair = next(p for p in plan(d)['pairs'] if p['a']=='K1' and p['b']=='K2')
                self.assertIsNone(pair['shared_top10'])
                self.assertEqual(pair['relation'], 'incompatible_context')

    def test_repeated_url_is_not_ten_results(self):
        self.data['keywords'][0]['serp']['organic_urls'] = ['https://fixture.example/a'] * 10
        p = plan(self.data)
        d = next(d for d in p['decisions'] if 'K1' in d['input_ids'])
        self.assertEqual(d['decision'], 'defer')

    def test_transitive_overlap_never_creates_three_way_merge(self):
        d = copy.deepcopy(self.data)
        d['keywords'] = d['keywords'][:3]
        d['existing_pages'] = []
        for row, start in zip(d['keywords'], (1,4,7)):
            row['intent'] = 'informational'
            row['serp']['organic_urls'] = [f'https://fixture.example/{n}' for n in range(start,start+10)]
        p = plan(d)
        self.assertFalse(any(len(x['input_ids'])==3 for x in p['decisions']))
        self.assertEqual(sorted(len(x['input_ids']) for x in p['decisions']), [1,2])

    def test_exact_duplicate_preserves_alias_id(self):
        row = copy.deepcopy(self.data['keywords'][0]); row['id']='K1-alias'
        row['keyword'] = ' CLIENT ONBOARDING CHECKLIST '
        self.data['keywords'].append(row)
        p = plan(self.data)
        self.assertEqual(p['input_rows'],6)
        self.assertEqual(p['unique_keywords'],5)
        self.assertTrue(any({'K1','K1-alias'} <= set(x['input_ids']) for x in p['decisions']))

    def test_navigation_never_commissions_article(self):
        d = next(d for d in plan(self.data)['decisions'] if 'K6' in d['input_ids'])
        self.assertEqual(d['decision'],'review_existing')
        self.assertEqual(d['target'],'/login')
        self.assertIn('no article',d['reason'])

    def test_same_keywords_really_are_same(self):
        other = json.loads((CASE / 'conversion.input.json').read_text())
        self.assertEqual([(k['id'],k['keyword'],k['serp']) for k in self.data['keywords']],
                         [(k['id'],k['keyword'],k['serp']) for k in other['keywords']])
        self.assertNotEqual(self.data['business_context']['primary_objective'], other['business_context']['primary_objective'])


class NewCodexPortTruthTests(unittest.TestCase):
    def setUp(self):
        from scripts import cluster_workflow
        self.module = cluster_workflow
        self.data = json.loads((CASE / 'awareness.cluster-input.json').read_text())

    def test_complete_generic_web_not_google_topten(self):
        for field,value in [('collection_method','generic_web'),('engine','bing'),('query','different query')]:
            with self.subTest(field=field):
                d=copy.deepcopy(self.data);d['candidates'][0]['serp'][field]=value
                with self.assertRaises(ValueError): self.module.build_plan(d)

    def test_exploratory_ten_links_still_unknown_overlap(self):
        self.data['candidates'][0]['serp']['status']='exploratory'
        self.data['candidates'][0]['serp']['collection_method']='generic_web'
        p=self.module.build_plan(self.data)
        pair=next(x for x in p['pairs'] if x['a']=='K1' and x['b']=='K2')
        self.assertIsNone(pair['shared_top10'])

    def test_unknown_volume_remains_null(self):
        p=self.module.build_plan(self.data)
        self.assertTrue(all(x['volume'] is None for x in p['pages']))
        self.assertTrue(all(x['volume'] is None for x in p['candidates']))

    def test_source_assertions_not_authentication(self):
        p=self.module.build_plan(self.data)
        self.assertIn('not independent verification',' '.join(p['warnings']))
        self.data['candidates'][0]['source_id']='missing'
        with self.assertRaises(ValueError):self.module.build_plan(self.data)

    def test_context_mismatches_block_overlap(self):
        for field,value in [('date','2026-10-15'),('market','GB'),('device','mobile'),('language','fr')]:
            with self.subTest(field=field):
                d=copy.deepcopy(self.data);d['candidates'][1]['serp'][field]=value
                pair=next(x for x in self.module.build_plan(d)['pairs'] if x['a']=='K1' and x['b']=='K2')
                self.assertIsNone(pair['shared_top10'])

    def test_duplicate_normalized_urls_rejected(self):
        self.data['candidates'][0]['serp']['organic_urls']=['https://fixture.example/a']*10
        with self.assertRaises(ValueError):self.module.build_plan(self.data)

    def test_duplicate_queries_require_reconciliation(self):
        c=copy.deepcopy(self.data['candidates'][0]);c['id']='alias';self.data['candidates'].append(c)
        with self.assertRaisesRegex(ValueError,'duplicate'):self.module.build_plan(self.data)

    def test_no_transitive_merge(self):
        self.data['candidates']=self.data['candidates'][:3]
        for c,start in zip(self.data['candidates'],(1,4,7)):
            c['intent']='informational';c['serp']['organic_urls']=[f'https://fixture.example/{i}' for i in range(start,start+10)]
        p=self.module.build_plan(self.data)
        self.assertEqual(sorted(len(x['candidate_ids']) for x in p['pages']),[1,2])

    def test_future_snapshot_is_rejected(self):
        self.data['candidates'][0]['serp']['date']='2999-01-01'
        with self.assertRaises(ValueError):self.module.build_plan(self.data)

    def test_future_volume_date_is_rejected(self):
        self.data['candidates'][0]['volume']={'value':10,'source_id':'S1','market':'US','date':'2999-01-01'}
        with self.assertRaises(ValueError):self.module.build_plan(self.data)

    def test_synthetic_labels_visible_in_brief_and_map(self):
        p=self.module.build_plan(self.data)
        self.assertIn('synthetic',self.module.render_map(p).lower())
        self.assertIn('synthetic',self.module.brief(p,p['pages'][0]).lower())
        self.data['fictional']=False
        with self.assertRaises(ValueError):self.module.build_plan(self.data)

    def test_nav_and_mixed_are_review_only_without_word_budget(self):
        p=self.module.build_plan(self.data)
        for page in p['pages']:
            if page['intent'] in ('navigational','mixed'):
                # No inventory mapping establishes a destination: preserve uncertainty.
                self.assertEqual(page['status'],'defer')
                self.assertIsNone(page['word_target'])
        # Unknown inventory authorizes no new architecture or pillar.
        self.assertIsNone(p['pillar_id'])

    def test_no_written_article_claim(self):
        p=self.module.build_plan(self.data);s=self.module.scorecard(p,True)
        self.assertIn(s['articles_written'],(None,0))
        self.assertIn(s['published_pages'],(None,0))
        self.assertEqual(p['publication_status'],'not_executed')

    def test_script_termination_payload_is_inert(self):
        attack='</script><script>window.PWNED=1</script>'
        self.data['candidates'][0]['editorial']={'title':attack}
        p=self.module.build_plan(self.data);html=self.module.render_map(p)
        self.assertNotIn(attack,html)
        self.assertIn('\\u003c/script\\u003e',html)
        self.assertNotIn('innerHTML',html)
        self.assertNotIn('src="http',html)
        self.assertNotIn('href="http',html)
        self.assertIn("connect-src 'none'",html)

    def test_javascript_result_url_rejected_without_network(self):
        self.data['candidates'][0]['serp']['organic_urls'][0]='javascript:alert(1)'
        with self.assertRaises(ValueError):self.module.build_plan(self.data)

    def test_artifact_traversal_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):self.module.write_artifacts(Path(td)/'out',{'../escape.txt':'test'})
            self.assertFalse((Path(td)/'escape.txt').exists())

    def test_existing_output_is_not_overwritten(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'out';self.module.write_artifacts(p,{'evidence.txt':'first'})
            with self.assertRaises(ValueError):self.module.write_artifacts(p,{'evidence.txt':'second'})
            self.assertEqual((p/'evidence.txt').read_text(),'first')

    def test_tampered_plan_id_cannot_write_outside_brief_dir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p=self.module.build_plan(self.data);p['pages'][0]['id']='../../escape'
            f=Path(td)/'tampered.json';f.write_text(json.dumps(p))
            with self.assertRaises(ValueError):self.module.load_plan(f)

class AgentPairedArtifactTests(unittest.TestCase):
    def test_substantive_reader_jobs_and_next_actions_differ(self):
        a=(CASE/'final-awareness/cluster-briefs/page-001.md').read_text()
        c=(CASE/'final-conversion/cluster-briefs/page-001.md').read_text()
        self.assertIn('owner/due-date/status checklist',a)
        self.assertIn('closing action is to adapt the checklist',a)
        self.assertIn('requirement / evidence available / unanswered question',c)
        self.assertIn('unique completed walkthrough-request submission',c)
        self.assertIn('click is not completion',c)
        self.assertNotIn('unique completed walkthrough-request submission',a)

    def test_count_semantics_distinguish_review_and_editorial_scaffolds(self):
        for goal in ('awareness','conversion'):
            s=json.loads((CASE/f'final-{goal}/cluster-scorecard.json').read_text())
            self.assertEqual(s['planned_pages'],4)
            self.assertEqual(s['actionable_planning_pages'],2)
            self.assertEqual(s['review_only_count'],2)
            self.assertEqual(s['brief_scaffolds_generated'],4)
            self.assertEqual(s['briefs_with_supplied_editorial_direction'],2)
            self.assertIsNone(s['articles_written'])

    def test_context_provenance_preserved_and_unknown_not_tailored(self):
        from scripts.cluster_workflow import build_plan
        d=json.loads((CASE/'awareness.agent-enriched-input.json').read_text())
        p=build_plan(d)
        self.assertEqual(p['business_context_provenance']['brand_position']['status'],'assumption')
        self.assertEqual(p['business_context_provenance']['primary_objective']['source_id'],'S1')
        d['business_context_provenance']['primary_objective']['source_id']='unknown'
        with self.assertRaises(ValueError):build_plan(d)
        d['business_context']={};d['business_context_provenance']={};p=build_plan(d)
        self.assertIn('generic framework',' '.join(p['warnings']))
        self.assertNotIn('tailored',p.get('business_context_status',''))


class FinalRendererAndReviewGraphTests(unittest.TestCase):
    def test_supplied_structure_first_and_links_adjacent(self):
        text=(CASE/'final2-awareness/cluster-briefs/page-001.md').read_text()
        self.assertLess(text.index('## Suggested structure'),text.index('## Appendix'))
        self.assertNotIn('1. Answer the reader',text)
        self.assertIn('## Outgoing internal links (proposed)\n- page-002:',text)

    def test_review_nodes_have_no_auto_edges(self):
        p=json.loads((CASE/'final2-awareness/cluster-plan.json').read_text())
        pending={x['id'] for x in p['pages'] if x['status']=='review_only'}
        self.assertEqual(len(pending),2)
        self.assertTrue(all(l['from'] not in pending and l['to'] not in pending for l in p['links']))
        self.assertEqual(len(p['links']),2)
        s=json.loads((CASE/'final2-awareness/cluster-scorecard.json').read_text())
        self.assertCountEqual(s['review_pending_unlinked'],list(pending))
        self.assertEqual(s['planned_orphans'],[])

    def test_all_review_case_not_a_false_success_or_orphan_alarm(self):
        from scripts.cluster_workflow import build_plan,scorecard
        d=json.loads((CASE/'awareness.cluster-input.json').read_text())
        d['candidates']=[x for x in d['candidates'] if x['intent'] in ('navigational','mixed')]
        p=build_plan(d);s=scorecard(p,True)
        self.assertEqual(p['links'],[])
        self.assertEqual(s['actionable_planning_pages'],0)
        self.assertEqual(s['review_only_count'],2)
        self.assertEqual(s['planned_orphans'],[])
        self.assertIsNone(s['all_reachable_within_two_clicks'])
        self.assertEqual(s['reachable_within_two_clicks'],[])

if __name__ == '__main__':
    unittest.main()
