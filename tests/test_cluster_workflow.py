"""Offline output-contract, evidence, graph and safety tests for the new CLI."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cluster_workflow as cw


def candidate(i, urls=None):
    r = dict(id=str(i), keyword='topic ' + str(i), intent='informational', intent_reason='supplied reader job', source_id='s')
    if urls is not None:
        r['serp'] = dict(status='complete', query=r['keyword'], engine='google', collection_method='google_organic_top10', market='US', language='en', device='desktop', date='2026-10-15', organic_urls=['https://example.com/' + str(u) for u in urls], source_id='s')
    return r


def fixture():
    return dict(schema_version=cw.INPUT_SCHEMA, project='Demo', seed='topic a', fictional=True,
                sources=[dict(id='s', kind='synthetic', description='Synthetic ordered organic SERP fixture; not measured demand')],
                candidates=[candidate('a', range(10)), candidate('b', list(range(7)) + [10, 11, 12]), candidate('c', list(range(4)) + [10, 11, 12, 13, 14, 15]), candidate('d')])


class ClusterWorkflowTests(unittest.TestCase):
    def test_utc_capture_day_and_future_dates(self):
        with patch.object(cw, 'datetime') as clock:
            clock.now.return_value = datetime(2026, 10, 16, 0, 1, tzinfo=timezone.utc)
            cw.iso_date('2026-10-16')
            clock.now.assert_called_with(timezone.utc)
            with self.assertRaises(ValueError): cw.iso_date('2026-10-17')

    def test_context_provenance_validation(self):
        data = fixture()
        data['business_context'] = {'primary_objective': 'awareness'}
        data['business_context_provenance'] = {'primary_objective': {'source_id': 's', 'date': '2026-10-15', 'status': 'assumption', 'evidence_locator': 'Fixture design'}}
        plan = cw.build_plan(data)
        self.assertEqual(plan['business_context_provenance'], data['business_context_provenance'])
        self.assertEqual(plan['business_context_status'], 'provenance_supplied_not_independently_verified')
        data['business_context_provenance']['primary_objective']['source_id'] = 'missing'
        with self.assertRaises(ValueError): cw.build_plan(data)

    def test_complete_link_not_transitive(self):
        plan = cw.build_plan(fixture())
        self.assertTrue(any(p['candidate_ids'] == ['a', 'b'] for p in plan['pages']))
        self.assertFalse(any(set(p['candidate_ids']) == {'a', 'b', 'c'} for p in plan['pages']))
        self.assertEqual(plan['serp_matrix']['scores'][3][3], None)

    def test_missing_snapshots_provisional_and_unknown_volume(self):
        data = fixture()
        data['candidates'] = [candidate('a'), candidate('b'), candidate('c')]
        plan = cw.build_plan(data)
        self.assertEqual(len(plan['pages']), 3)
        self.assertTrue(all(p['volume'] is None for p in plan['pages']))
        self.assertTrue(all(p['evidence_status'] == 'provisional_intent_only' for p in plan['pages']))
        self.assertEqual(plan['clusters'][0]['evidence_status'], 'provisional_intent_only')

    def test_comparability_and_discovery(self):
        data = fixture()
        data['candidates'][1]['serp']['market'] = 'GB'
        self.assertIsNone(cw.build_plan(data)['pairs'][0]['shared_top10'])
        data['candidates'][1]['serp']['collection_method'] = 'generic_web'
        with self.assertRaises(ValueError): cw.build_plan(data)
        data['candidates'][1]['serp']['status'] = 'exploratory'
        self.assertIsNone(cw.build_plan(data)['pairs'][0]['shared_top10'])

    def test_incomplete_duplicate_and_query_validation(self):
        for mutation in ('duplicate', 'query', 'short'):
            data = fixture()
            serp = data['candidates'][0]['serp']
            if mutation == 'duplicate': serp['organic_urls'][-1] = serp['organic_urls'][0] + '?utm_source=test'
            if mutation == 'query': serp['query'] = 'other query'
            if mutation == 'short': serp['organic_urls'].pop()
            with self.assertRaises(ValueError): cw.build_plan(data)

    def test_volume_scope_required_and_not_used_as_rank(self):
        data = fixture()
        data['candidates'][1]['volume'] = dict(value=999999, source_id='s', date='2026-10-15', market='GB')
        self.assertIsNone(cw.build_plan(data)['pillar_id'])
        del data['candidates'][1]['volume']['market']
        with self.assertRaises(ValueError): cw.build_plan(data)
        data['candidates'][1]['volume'] = dict(value=True, source_id='s', date='2026-10-15', market='US')
        with self.assertRaises(ValueError): cw.build_plan(data)

    def test_links_root_consistency_and_honest_scorecard(self):
        plan = cw.build_plan(fixture())
        ids = {p['id'] for p in plan['pages']}
        self.assertTrue(all(l['from'] in ids and l['to'] in ids for l in plan['links']))
        report = cw.scorecard(plan, True)
        self.assertIsNone(report['all_reachable_within_two_clicks'])
        self.assertEqual(report['disposition_counts']['defer'], len(ids))
        self.assertEqual(plan['links'], [])
        self.assertEqual(report['planned_orphans'], [])
        self.assertEqual(report['briefs_generated'], len(ids))
        for k in ('articles_written', 'published_pages', 'implemented_links', 'image_coverage', 'actual_coverage'):
            self.assertIsNone(report[k])

    def test_safe_map_and_filenames(self):
        data = fixture()
        row = data['candidates'][-1]
        row['keyword'] = '</script><img src=x onerror=alert(1)>'
        row['id'] = '../../escape'
        plan = cw.build_plan(data)
        document = cw.render_map(plan)
        self.assertNotIn('</script><img', document)
        self.assertIn('\\u003c/script\\u003e', document)
        self.assertNotIn('innerHTML', document)
        self.assertNotIn('<script src=', document)
        self.assertTrue(all('..' not in f for f in cw.artifacts(plan)))

    def test_context_and_editorial_change_brief(self):
        data = fixture()
        plain = cw.build_plan(data)
        data['business_context'] = dict(audience='independent designers', primary_objective='consideration', brand_position='evidence-led education', conversion_definition='request a portfolio review')
        data['candidates'][0]['editorial'] = dict(title='A practical decision guide', outline=['Compare two real workflows', 'Check review time'], key_points=['Verify each claim'], differentiation='Use a documented workflow example')
        tailored = cw.build_plan(data)
        self.assertNotEqual(cw.brief(plain, plain['pages'][0]), cw.brief(tailored, tailored['pages'][0]))
        text = cw.brief(tailored, tailored['pages'][0])
        self.assertIn('Compare two real workflows', text)
        self.assertNotIn('1. Answer the reader', text)
        outgoing = text.split('## Outgoing internal links (proposed)')[1].split('## Incoming')[0]
        self.assertIn('None proposed', outgoing)
        self.assertNotIn('Provenance', outgoing)
        self.assertEqual(tailored['business_context_status'], 'self_reported_unverified')

    def test_navigation_retained_review_only(self):
        data = fixture()
        data['candidates'][0]['intent'] = 'navigational'
        data['candidates'][1]['intent'] = 'mixed'
        plan = cw.build_plan(data)
        for p in plan['pages']:
            if p['intent'] in ('mixed', 'navigational'):
                self.assertEqual(p['status'], 'defer')
                self.assertIsNone(p['word_target'])
                self.assertNotEqual(p['id'], plan['pillar_id'])
                self.assertFalse(any(p['id'] in (link['from'], link['to']) for link in plan['links']))
                self.assertIn(p['id'], cw.scorecard(plan)['review_pending_unlinked'])
                self.assertNotIn(p['id'], cw.scorecard(plan)['planned_orphans'])

    def test_explicit_inventory_and_new_proposal_gate(self):
        data = fixture()
        data['existing_page_inventory'] = dict(status='complete', source_id='s', evidence_locator='Fixture site audit', pages=[])
        self.assertTrue(all(p['status'] == 'defer' for p in cw.build_plan(data)['pages']))
        for row in data['candidates']:
            row['new_page_evidence'] = dict(gap='Documented unanswered reader question', business_rationale='Help readers evaluate a relevant service', source_id='s', evidence_locator='Fixture gap audit')
        plan = cw.build_plan(data)
        self.assertTrue(all(p['status'] == 'new_proposal' for p in plan['pages']))
        self.assertTrue(cw.scorecard(plan)['all_reachable_within_two_clicks'])
        self.assertFalse(cw.scorecard(plan)['execution_approved'])
        self.assertTrue(all(p['proposed_path'] is None for p in plan['pages']))
        data['existing_page_inventory']['status'] = 'partial'
        self.assertTrue(all(p['status'] == 'defer' for p in cw.build_plan(data)['pages']))

    def test_existing_destination_dedup_and_coverage(self):
        data = fixture()
        data['candidates'] = [candidate('a'), candidate('b')]
        for row in data['candidates']:
            row['existing_page'] = dict(url='https://example.com/service?utm_source=fixture', coverage='sufficient', source_id='s', evidence_locator='Fixture page inspection')
        plan = cw.build_plan(data)
        self.assertEqual(len(plan['pages']), 1)
        self.assertEqual(plan['pages'][0]['status'], 'retain')
        self.assertEqual(plan['pages'][0]['existing_urls'], ['https://example.com/service'])
        data['candidates'][1]['existing_page']['coverage'] = 'unknown'
        self.assertEqual(cw.build_plan(data)['pages'][0]['status'], 'review_existing')

    def test_mapping_import_is_explicit_unknown_coverage(self):
        data = fixture()
        original = copy.deepcopy(data)
        mappings = [dict(candidate_id='a', existing_url='https://example.com/services')]
        imported = cw.import_page_mapping(data, mappings)
        self.assertEqual(data, original)
        plan = cw.build_plan(imported)
        self.assertEqual(plan['inventory_status'], 'unknown')
        self.assertEqual(plan['pages'][0]['status'], 'review_existing')
        self.assertEqual(imported['imported_page_mapping'], mappings)
        with self.assertRaises(ValueError):
            cw.import_page_mapping(data, mappings * 2)

    def test_normalized_terms_are_review_signals_not_coverage(self):
        data = fixture()
        data['candidates'] = [candidate('a')]
        data['candidates'][0]['keyword'] = 'COMMUNITY solar planning'
        data['existing_page_inventory'] = dict(status='complete', source_id='s', evidence_locator='Fixture audit', pages=[dict(url='https://example.com/solar', title='Planning community solar', terms=[], source_id='s', evidence_locator='Fixture title')])
        page = cw.build_plan(data)['pages'][0]
        self.assertEqual(page['status'], 'review_existing')
        self.assertEqual(page['existing_urls'], ['https://example.com/solar'])

    def test_recruitment_templates_and_next_action_precedence(self):
        data = fixture()
        data['candidates'] = [candidate('a')]
        data['candidates'][0]['intent'] = 'commercial'
        data['business_context'] = dict(content_purpose='recruitment_portfolio', next_action='Inspect relevant work', conversion_definition='Optional hiring conversation')
        data['candidates'][0]['editorial'] = dict(next_action='Retain the existing case if sufficient')
        plan = cw.build_plan(data)
        page = plan['pages'][0]
        self.assertEqual(page['template'], 'recruiter-evidence-review')
        self.assertEqual(page['next_action'], 'Retain the existing case if sufficient')
        self.assertEqual(page['conversion_definition'], 'Optional hiring conversation')
        self.assertNotIn('Compare relevant alternatives', cw.brief(plan, page))
        del data['candidates'][0]['editorial']
        self.assertEqual(cw.build_plan(data)['pages'][0]['next_action'], 'Inspect relevant work')
        data['business_context']['content_purpose'] = 'product_education'
        self.assertEqual(cw.build_plan(data)['pages'][0]['template'], 'comparison')

    def test_cli_all_modes_real_artifacts_and_preservation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_path = root / 'input.json'
            input_path.write_text(json.dumps(fixture()))
            def run(*args):
                return subprocess.run([sys.executable, str(ROOT / 'scripts/cluster_workflow.py'), *map(str, args)], capture_output=True, text=True)
            out = root / 'plan'
            result = run('plan', '--input', input_path, '--out', out)
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = out / 'cluster-plan.json'
            original = saved.read_bytes()
            self.assertEqual(cw.load_plan(saved), cw.build_plan(fixture()))
            for command in ('map', 'execute', 'scorecard'):
                args = [command, '--plan', saved, '--out', root / command]
                if command == 'execute': args += ['--mode', 'briefs']
                result = run(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotEqual(run('plan', '--input', input_path, '--out', out).returncode, 0)
            self.assertEqual(original, saved.read_bytes())
            tampered = json.loads(saved.read_text())
            tampered['pages'][0]['id'] = '../../escape'
            saved.write_text(json.dumps(tampered))
            with self.assertRaises(ValueError): cw.load_plan(saved)

    def test_determinism_and_symlink_refusal(self):
        data = fixture()
        a = cw.artifacts(cw.build_plan(data))
        self.assertEqual(a, cw.artifacts(cw.build_plan(copy.deepcopy(data))))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / 'real'
            real.mkdir()
            link = root / 'link'
            link.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ValueError): cw.write_artifacts(link, a)
            with self.assertRaises(ValueError): cw.write_artifacts(link / 'child', a)


if __name__ == '__main__': unittest.main()
