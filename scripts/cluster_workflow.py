#!/usr/bin/env python3
"""Deterministic offline Codex cluster planning; no fetches, publication or article writer.

Overlap bands adapted from the pinned seo-cluster method; see ATTRIBUTION.md.
The standalone HTML renderer is original and has no external dependencies.
"""
import argparse
import copy
import re
import html
import itertools
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path

try:
    from .plan_keywords import norm_keyword, norm_url, require, INTENTS
except ImportError:
    from plan_keywords import norm_keyword, norm_url, require, INTENTS

INPUT_SCHEMA = 'cluster-input-1.0'
PLAN_SCHEMA = 'cluster-plan-1.0'
DEFAULTS = dict(candidate_target_min=30, candidate_target_max=50,
                pillar_words=[2500, 4000], spoke_words=[1200, 1800],
                sibling_link_limit=3, cross_link_limit=1)


def string(value, label):
    require(isinstance(value, str) and bool(value.strip()), label + ' must be a nonempty string')
    return value


def iso_date(value):
    string(value, 'date')
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ValueError('date must be YYYY-MM-DD')
    require(parsed.isoformat() == value, 'date must be YYYY-MM-DD')
    require(parsed <= datetime.now(timezone.utc).date(), 'future capture or metric date is not valid evidence')


def prepare(data):
    require(isinstance(data, dict), 'input must be an object')
    require(data.get('schema_version') == INPUT_SCHEMA, 'schema_version must be ' + INPUT_SCHEMA)
    for k in ('project', 'seed'):
        string(data.get(k), k)
    require(type(data.get('fictional')) is bool, 'fictional boolean required')
    sources = data.get('sources')
    require(isinstance(sources, list) and sources, 'sources required')
    source_ids = set()
    for s in sources:
        require(isinstance(s, dict), 'source must be an object')
        string(s.get('id'), 'source id')
        require(s['id'] not in source_ids, 'duplicate source id')
        require(s.get('kind') in ('supplied', 'synthetic'), 'invalid source kind')
        string(s.get('description'), 'source description')
        require(data['fictional'] or s['kind'] != 'synthetic', 'synthetic source requires fictional=true')
        source_ids.add(s['id'])
    context = data.get('business_context', {})
    require(isinstance(context, dict), 'business_context must be an object')
    for k, v in context.items():
        string(v, 'business_context.' + k)
    provenance = data.get('business_context_provenance', {})
    require(isinstance(provenance, dict), 'business_context_provenance must be an object')
    for field, record in provenance.items():
        require(field in context and isinstance(record, dict), 'context provenance must reference an existing context field')
        require(record.get('status') in ('confirmed', 'self_reported', 'assumption', 'unknown'), 'invalid context provenance status')
        require(record.get('source_id') in source_ids, 'unknown context source')
        iso_date(record.get('date'))
        string(record.get('evidence_locator'), 'context evidence_locator')
    settings = dict(DEFAULTS, **data.get('settings', {}))
    require(set(settings) == set(DEFAULTS), 'unknown setting')
    for k in ('candidate_target_min', 'candidate_target_max', 'sibling_link_limit', 'cross_link_limit'):
        require(type(settings[k]) is int and settings[k] >= 0, k + ' must be a nonnegative integer')
    require(0 < settings['candidate_target_min'] <= settings['candidate_target_max'], 'invalid candidate range')
    for k in ('pillar_words', 'spoke_words'):
        v = settings[k]
        require(isinstance(v, list) and len(v) == 2 and all(type(n) is int and n > 0 for n in v) and v[0] <= v[1], 'invalid word range')
    raw = data.get('candidates')
    require(isinstance(raw, list) and raw, 'candidates required')
    ids, keys, rows = set(), set(), []
    for raw_row in raw:
        require(isinstance(raw_row, dict), 'candidate must be an object')
        r = dict(raw_row)
        string(r.get('id'), 'candidate id')
        require(r['id'] not in ids, 'duplicate candidate id')
        ids.add(r['id'])
        key = norm_keyword(string(r.get('keyword'), 'keyword'))
        require(key not in keys, 'duplicate normalized keyword; reconcile aliases before planning')
        keys.add(key)
        require(r.get('intent') in INTENTS, 'invalid intent')
        string(r.get('intent_reason'), 'intent_reason')
        require(r.get('source_id') in source_ids, 'unknown candidate source')
        r['normalized_keyword'] = key
        s = r.get('serp')
        r['normalized_urls'] = []
        r['snapshot_eligible'] = False
        if s is not None:
            require(isinstance(s, dict), 'serp must be an object or null')
            require(s.get('status') in ('complete', 'exploratory', 'incomplete', 'unknown'), 'invalid SERP status')
            require(s.get('source_id') in source_ids, 'unknown SERP source')
            urls = s.get('organic_urls', [])
            require(isinstance(urls, list) and all(isinstance(u, str) for u in urls), 'organic_urls must be a list of URLs')
            r['normalized_urls'] = [norm_url(u) for u in urls]
            require(len(urls) <= 10, 'supply at most ten organic results')
            if s.get('date') is not None:
                iso_date(s['date'])
            if s['status'] == 'complete':
                for k in ('query', 'engine', 'market', 'language', 'device', 'date'):
                    string(s.get(k), 'complete SERP ' + k)
                require(norm_keyword(s['query']) == key, 'SERP query must match candidate keyword')
                require(s.get('collection_method') == 'google_organic_top10', 'complete snapshots require collection_method=google_organic_top10; generic web discovery is exploratory')
                require(s['engine'].casefold() == 'google', 'complete comparable snapshots must be Google organic top ten')
                require(len(urls) == 10 and len(set(r['normalized_urls'])) == 10, 'complete SERP requires ten distinct ordered organic URLs')
                r['snapshot_eligible'] = True
        volume = r.get('volume')
        if volume is not None:
            require(isinstance(volume, dict), 'volume must be object or null')
            v = volume.get('value')
            require(type(v) in (int, float) and math.isfinite(v) and v >= 0, 'volume value must be finite nonnegative number')
            require(volume.get('source_id') in source_ids, 'unknown volume source')
            string(volume.get('market'), 'volume market')
            iso_date(volume.get('date'))
        editorial = r.get('editorial', {})
        require(isinstance(editorial, dict), 'editorial must be an object')
        require(set(editorial) <= {'title', 'meta_description', 'outline', 'key_points', 'differentiation', 'reader_job', 'next_action', 'acceptance_criteria', 'evidence_needed', 'evidence_source_ids'}, 'unknown editorial field')
        for k, v in editorial.items():
            if k in ('outline', 'key_points', 'acceptance_criteria', 'evidence_needed', 'evidence_source_ids'):
                require(isinstance(v, list) and v and all(isinstance(x, str) and x.strip() for x in v), 'editorial list must contain text')
                if k == 'evidence_source_ids':
                    require(all(x in source_ids for x in v), 'unknown editorial source')
            else:
                string(v, 'editorial.' + k)
        r['volume'] = volume
        rows.append(r)
    return sorted(rows, key=lambda r: r['id']), context, settings


def term_tokens(value):
    """Conservative lexical signals only; never assert semantic or page coverage."""
    return set(re.findall(r"[^\W_]+", norm_keyword(value), flags=re.UNICODE))


def inventory_evidence(data, rows):
    sources = {s['id'] for s in data['sources']}
    def citation(record, label):
        require(record.get('source_id') in sources, label + ': unknown source')
        string(record.get('evidence_locator'), label + ': evidence_locator')
    inventory = data.get('existing_page_inventory')
    if inventory is None:
        inventory = dict(status='unknown', pages=[])
    else:
        require(isinstance(inventory, dict), 'existing_page_inventory must be object')
        require(inventory.get('status') in ('complete', 'partial', 'unknown'), 'invalid inventory status')
        citation(inventory, 'inventory')
        require(isinstance(inventory.get('pages'), list), 'inventory pages must be list')
    pages = {}
    for item in inventory['pages']:
        require(isinstance(item, dict), 'inventory page must be object')
        citation(item, 'inventory page')
        url = norm_url(string(item.get('url'), 'inventory page URL'))
        string(item.get('title'), 'inventory page title')
        terms = item.get('terms', [])
        require(isinstance(terms, list) and all(isinstance(t, str) and t.strip() for t in terms), 'inventory terms must be text list')
        pages.setdefault(url, []).append(item)
    decisions = {}
    for row in rows:
        mapping = row.get('existing_page')
        gap = row.get('new_page_evidence')
        if gap is not None:
            require(isinstance(gap, dict), 'new_page_evidence must be object')
            citation(gap, 'new page evidence')
            string(gap.get('gap'), 'documented gap')
            string(gap.get('business_rationale'), 'business rationale')
        if mapping is not None:
            require(isinstance(mapping, dict), 'existing_page must be object')
            citation(mapping, 'candidate mapping')
            require(mapping.get('coverage') in ('sufficient', 'partial', 'unknown'), 'invalid existing page coverage')
            url = norm_url(string(mapping.get('url'), 'existing page URL'))
            decisions[row['id']] = dict(status='retain' if mapping['coverage'] == 'sufficient' else 'review_existing',
                existing_urls=[url], coverage_evidence=[dict(mapping, basis='explicit_candidate_mapping')])
            continue
        tokens = term_tokens(row['keyword'])
        matches = []
        for url, records in pages.items():
            if any(tokens == term_tokens(term) or (len(tokens & term_tokens(term)) >= 2 and
                   len(tokens & term_tokens(term)) / max(1, min(len(tokens), len(term_tokens(term)))) >= .75)
                   for item in records for term in [item['title']] + item.get('terms', [])):
                matches.append(url)
        # Outline URLs are retained as unresolved destination hints, never parsed into coverage proof.
        hints = [u.rstrip('.,;)') for line in row.get('editorial', {}).get('outline', [])
                 for u in re.findall(r'https?://[^\s<>]+', line)]
        if matches:
            decisions[row['id']] = dict(status='review_existing', existing_urls=sorted(matches),
                coverage_evidence=[dict(basis='normalized_term_similarity_requires_review', url=u,
                                        records=pages[u]) for u in sorted(matches)])
        elif hints:
            decisions[row['id']] = dict(status='defer', existing_urls=[], coverage_evidence=[dict(
                basis='unstructured_outline_url_requires_explicit_mapping', urls=hints)])
        elif inventory['status'] == 'complete' and gap and row['intent'] not in ('mixed', 'navigational'):
            decisions[row['id']] = dict(status='new_proposal', existing_urls=[], coverage_evidence=[dict(
                gap, basis='supplied_gap_and_business_rationale_not_independently_verified')])
        else:
            decisions[row['id']] = dict(status='defer', existing_urls=[], coverage_evidence=[dict(
                basis='absence_not_established' if inventory['status'] != 'complete' else 'gap_or_business_rationale_missing_or_intent_unresolved')])
    return inventory, decisions


def import_page_mapping(data, mappings):
    """Explicit legacy import; never treats a mapping list as a complete site inventory."""
    require(isinstance(mappings, list), 'page mapping must be a list')
    data = copy.deepcopy(data)
    by_id = {r['id']: r for r in data['candidates']}
    seen = set()
    source_id = 'explicit-page-mapping-import'
    existing_ids = {s['id'] for s in data['sources']}
    while source_id in existing_ids:
        source_id += '-import'
    data['sources'].append(dict(id=source_id, kind='supplied', description='Explicitly supplied candidate-to-existing-URL mapping; coverage and completeness unverified'))
    for record in mappings:
        require(isinstance(record, dict) and record.get('candidate_id') in by_id, 'mapping references unknown candidate')
        cid = record['candidate_id']
        require(cid not in seen, 'duplicate candidate mapping')
        seen.add(cid)
        row = by_id[cid]
        if record.get('keyword') is not None:
            require(norm_keyword(record['keyword']) == norm_keyword(row['keyword']), 'mapping keyword mismatch')
        mapping = dict(url=norm_url(record['existing_url']), coverage='unknown', source_id=source_id,
                       evidence_locator='Explicitly supplied page-mapping record for candidate ' + cid)
        require('existing_page' not in row or norm_url(row['existing_page']['url']) == mapping['url'], 'conflicting candidate mapping')
        row.setdefault('existing_page', mapping)
    data['imported_page_mapping'] = copy.deepcopy(mappings)
    return data


def content_purpose(context):
    if context.get('content_purpose'):
        return context['content_purpose']
    industry = norm_keyword(context.get('industry', ''))
    objective = norm_keyword(context.get('primary_objective', ''))
    if 'portfolio' in industry and ('recruit' in objective or 'hiring' in objective):
        return 'recruitment_portfolio'
    return 'general'


def page_template(intent, purpose):
    if purpose == 'recruitment_portfolio':
        return {'informational': 'portfolio-case-evidence', 'commercial': 'recruiter-evidence-review',
                'transactional': 'recruitment-contact', 'navigational': 'profile-destination-review',
                'mixed': 'reader-job-review'}[intent]
    return {'informational': 'explainer', 'commercial': 'comparison', 'transactional': 'landing-page',
            'navigational': 'entity-destination-review', 'mixed': 'intent-review'}[intent]


def compare(a, b):
    if not a['snapshot_eligible'] or not b['snapshot_eligible']:
        return None, 'missing_or_noncomparable_top10'
    if any(a['serp'][k] != b['serp'][k] for k in ('market', 'language', 'device', 'date')):
        return None, 'incompatible_snapshot_context'
    n = len(set(a['normalized_urls']) & set(b['normalized_urls']))
    return n, ('same_page_candidate' if n >= 7 else 'same_topic_candidate' if n >= 4 else 'cross_link_candidate' if n >= 2 else 'separate')


def build_plan(data):
    rows, context, settings = prepare(data)
    inventory, decisions = inventory_evidence(data, rows)
    purpose = content_purpose(context)
    scores, pairs = {}, []
    for a, b in itertools.combinations(rows, 2):
        n, relation = compare(a, b)
        scores[frozenset((a['id'], b['id']))] = n
        pairs.append(dict(a=a['id'], b=b['id'], shared_top10=n, relation=relation))
    def score(a, b):
        return scores.get(frozenset((a['id'], b['id'])))
    # Complete-link at both levels: no transitive A-B-C merge without A-C evidence.
    groups = []
    for r in rows:
        for g in groups:
            if (len(decisions[r['id']]['existing_urls']) == 1 and all(decisions[x['id']]['existing_urls'] == decisions[r['id']]['existing_urls'] for x in g)) or (not decisions[r['id']]['existing_urls'] and r['intent'] not in ('mixed', 'navigational') and all(not decisions[x['id']]['existing_urls'] and x['intent'] == r['intent'] and decisions[x['id']]['status'] == decisions[r['id']]['status'] and (score(x, r) or 0) >= 7 for x in g)):
                g.append(r)
                break
        else:
            groups.append([r])
    objective = context.get('primary_objective', 'unknown; clarify the business objective')
    position = context.get('brand_position', 'unknown; obtain a defensible positioning statement')
    pages = []
    for i, group in enumerate(groups, 1):
        primary = next((r for r in group if r['normalized_keyword'] == norm_keyword(data['seed'])), group[0])
        statuses = [decisions[r['id']]['status'] for r in group]
        disposition = next((v for v in ('defer', 'review_existing', 'retain', 'new_proposal') if v in statuses), 'defer')
        urls = sorted({u for r in group for u in decisions[r['id']]['existing_urls']})
        editorial = primary.get('editorial', {})
        pages.append(dict(id='page-%03d' % i, title=primary.get('editorial', {}).get('title', primary['keyword']), editorial=primary.get('editorial', {}), primary_keyword=primary['keyword'],
                          candidate_ids=[r['id'] for r in group], secondary_keywords=[r['keyword'] for r in group if r is not primary],
                          intent=primary['intent'], volume=primary['volume'],
                          evidence_status=('synthetic_top10' if data['fictional'] else 'supplied_top10') if all(r['snapshot_eligible'] for r in group) else 'provisional_intent_only',
                          template=page_template(primary['intent'], purpose), content_purpose=purpose,
                          proposed_path=urls[0] if len(urls) == 1 else None, path_status='existing_destination_review' if urls else 'no_new_url_authorized', status=disposition,
                          existing_urls=urls, coverage_evidence=[dict(candidate_id=r['id'], **decisions[r['id']]) for r in group],
                          next_action=editorial.get('next_action', context.get('next_action', context.get('conversion_definition', 'Unknown; agree an appropriate next step'))),
                          conversion_definition=context.get('conversion_definition'),
                          candidate_next_actions={r['id']: r.get('editorial', {}).get('next_action', context.get('next_action', context.get('conversion_definition'))) for r in group},
                          rationale='Objective: ' + objective + '. Positioning: ' + position + '. ' +
                          ('Retain relevant entity/navigation content; verify destination and reader job.' if primary['intent'] == 'navigational' else 'Validate reader job and supporting claims before commissioning.')))
    row_by_id = {r['id']: r for r in rows}
    def members(p):
        return [row_by_id[i] for i in p['candidate_ids']]
    def page_overlap(a, b):
        vals = [score(x, y) for x in members(a) for y in members(b)]
        return min(vals) if all(v is not None for v in vals) else None
    # Pick the seed page, otherwise strongest measured connection count then stable ID.
    eligible_pillars = [p for p in pages if p['status'] == 'new_proposal']
    structural_candidates = eligible_pillars or [p for p in pages if p['intent'] not in ('navigational', 'mixed')] or pages
    pillar = next((p for p in structural_candidates if any(norm_keyword(row_by_id[i]['keyword']) == norm_keyword(data['seed']) for i in p['candidate_ids'])), None)
    if pillar is None:
        pillar = sorted(structural_candidates, key=lambda p: (-sum((page_overlap(p, q) or 0) >= 4 for q in pages if p != q), p['id']))[0]
    topic_groups = []
    for p in pages:
        if p is pillar:
            continue
        for g in topic_groups:
            if all((page_overlap(p, q) or 0) >= 4 for q in g):
                g.append(p)
                break
        else:
            topic_groups.append([p])
    # Intent-only provisional folders are explicitly not measured keyword clusters.
    provisional = {}
    measured = []
    for g in topic_groups:
        if len(g) == 1 and g[0]['evidence_status'] == 'provisional_intent_only':
            provisional.setdefault(g[0]['intent'], []).extend(g)
        else:
            measured.append((g, ('synthetic_top10' if data['fictional'] else 'supplied_top10') if len(g) > 1 else 'standalone_topic'))
    measured += [(g, 'provisional_intent_only') for _, g in sorted(provisional.items())]
    clusters = []
    for i, (group, basis) in enumerate(measured, 1):
        cid = 'topic-%03d' % i
        clusters.append(dict(id=cid, label=group[0]['primary_keyword'], page_ids=[p['id'] for p in group], evidence_status=basis))
        for p in group:
            p['cluster_id'] = cid
    pillar['cluster_id'] = None
    for p in pages:
        p['role'] = ('pillar' if p is pillar else 'spoke') if p['status'] == 'new_proposal' else ('existing_review' if p['existing_urls'] else 'deferred')
        p['word_target'] = None if p['status'] != 'new_proposal' else settings['pillar_words' if p is pillar else 'spoke_words']
    links = []
    def link(a, b, kind, basis):
        if a['status'] != 'new_proposal' or b['status'] != 'new_proposal':
            return
        if not any(x['from'] == a['id'] and x['to'] == b['id'] for x in links):
            links.append(dict(source='editorial_architecture', **{'from': a['id'], 'to': b['id']}, type=kind, anchor=b['primary_keyword'], evidence_basis=basis))
    for p in pages:
        if p is not pillar:
            link(pillar, p, 'hub_spoke', 'proposed editorial navigation; validate relevance')
            link(p, pillar, 'hub_spoke', 'proposed editorial navigation; validate relevance')
    for p in pages:
        siblings = [q for q in pages if q != p and p['cluster_id'] is not None and q['cluster_id'] == p['cluster_id'] and (page_overlap(p, q) or 0) >= 4]
        for q in siblings[:settings['sibling_link_limit']]:
            link(p, q, 'sibling', 'minimum all-member top10 overlap >=4')
        cross = [q for q in pages if q != p and q is not pillar and p is not pillar and q['cluster_id'] != p['cluster_id'] and (page_overlap(p, q) or 0) >= 2]
        for q in cross[:settings['cross_link_limit']]:
            link(p, q, 'cross_cluster', 'minimum all-member top10 overlap >=2')
    warnings = ['Planning heuristics, not Google rules or publication approval. No demand, urgency, ranking or traffic lift is inferred.',
                'Source records are supplied provenance, not independent verification. Analyst must confirm organic ranking order, freshness and authenticity.',
                'Word ranges and link counts are adjustable editorial heuristics. Hub/spoke links require relevance review.',
                'Existing-page mappings and inventory coverage are supplied assertions, not independent audits. Lexical similarity is a review hint only.',
                'No new destination is authorized. A new_proposal requires a supplied complete inventory and cited gap/business rationale, and still requires editorial approval.']
    if inventory['status'] != 'complete':
        warnings.append('Inventory incomplete or unknown: missing matches do not establish an empty site or justify new pages.')
    if not settings['candidate_target_min'] <= len(rows) <= settings['candidate_target_max']:
        warnings.append('Candidate count outside configured discovery target; do not fabricate candidates to meet a quota.')
    if any(not r['snapshot_eligible'] for r in rows):
        warnings.append('Missing/exploratory/incomplete evidence: intent-only provisional folders do not establish SERP clusters or merge authority.')
    if not context:
        warnings.append('Business context absent: generic framework only; collect positioning, audience and objective before commissioning.')
    matrix = [[(10 if a['snapshot_eligible'] else None) if a is b else score(a, b) for b in rows] for a in rows]
    return dict(schema_version=PLAN_SCHEMA, project=data['project'], seed=data['seed'], fictional=data['fictional'],
                evidence_input=data, existing_page_inventory=inventory, inventory_status=inventory['status'], content_purpose=purpose, business_context=context, business_context_status=('provenance_supplied_not_independently_verified' if data.get('business_context_provenance') else 'self_reported_unverified') if context else 'unknown', business_context_provenance=data.get('business_context_provenance', {}), settings=settings, candidates=rows, pairs=pairs,
                serp_matrix={'candidate_ids': [r['id'] for r in rows], 'scores': matrix},
                pillar_id=pillar['id'] if eligible_pillars else None, pages=pages, clusters=clusters, links=links, warnings=warnings,
                pillar_selection='Seed page if present; otherwise highest count of measured topic connections, then stable ID. Editorial heuristic, not demand ranking.', ordering='Deterministic structural order, not demand or publication priority', publication_status='not_executed')


def md(value):
    return html.escape(str(value), quote=True).replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('`', '\\`').replace('\n', ' ')


def render_plan(plan):
    lines = ['# ' + md(plan['project']) + ': cluster plan', '', 'Status: planning only; no articles written or published.', '', '## Caveats']
    lines += ['- ' + md(w) for w in plan['warnings']]
    lines += ['', '## Business context (' + plan['business_context_status'] + ')'] + ['- ' + md(k) + ': ' + md(v) for k, v in plan['business_context'].items()]
    for field, record in plan['business_context_provenance'].items():
        lines += ['- Provenance for ' + md(field) + ': ' + md(json.dumps(record, sort_keys=True))]
    lines += ['', '## Pages']
    for p in plan['pages']:
        lines += ['', '### ' + p['id'] + ': ' + md(p['title']), '- Role: ' + p['role'], '- Evidence: ' + p['evidence_status'], '- Primary keyword: ' + md(p['primary_keyword']), '- Rationale: ' + md(p['rationale']), '- Disposition: ' + p['status'], '- Existing destinations: ' + (', '.join(md(u) for u in p['existing_urls']) or 'Unresolved; no new URL authorized'), '- Coverage evidence: ' + md(json.dumps(p['coverage_evidence'], ensure_ascii=False))]
    lines += ['', '## Planned internal links']
    lines += ['- ' + l['from'] + ' → ' + l['to'] + ' (' + l['type'] + '): ' + md(l['anchor']) for l in plan['links']]
    return '\n'.join(lines) + '\n'


def brief(plan, page):
    context = plan['business_context']
    editorial = page.get('editorial', {})
    candidates = [r for r in plan['candidates'] if r['id'] in page['candidate_ids']]
    competing = list(dict.fromkeys(u for r in candidates for u in r['normalized_urls']))
    lines = ['# ' + md(page['title']), '', 'Planning scaffold pending agent/editor completion. Not a commissioned or written article.',
             '', '- Primary keyword: ' + md(page['primary_keyword']), '- Secondary keywords: ' + (', '.join(md(x) for x in page['secondary_keywords']) or 'None supplied'),
             '- Template: ' + page['template'], '- Role: ' + page['role'], '- Evidence: ' + page['evidence_status'], '- Status: ' + page['status'],
             '- Word target (adjustable heuristic): ' + ('Review only; no article target' if page['word_target'] is None else '–'.join(map(str, page['word_target']))),
             '- Audience: ' + md(context.get('audience', 'Unknown; clarify')), '- Objective: ' + md(context.get('primary_objective', 'Unknown; clarify')),
             '- Positioning: ' + md(context.get('brand_position', 'Unknown; clarify')),
             '- Conversion/next step: ' + md(page['next_action']),
             '- Conversion definition (supplied): ' + md(page['conversion_definition'] or 'Not supplied'),
             '- Existing destinations: ' + (', '.join(md(u) for u in page['existing_urls']) or 'Unresolved; no new URL authorized'),
             '- Business context status: ' + plan['business_context_status'],
             '- Meta description draft: ' + md(editorial.get('meta_description', 'Not proposed; review existing metadata only if gap evidence warrants it.' if page['status'] in ('retain', 'review_existing') else 'Not proposed; resolve inventory and evidence first.' if page['status'] == 'defer' else 'Explore ' + page['primary_keyword'] + ' for ' + context.get('audience', 'the intended audience') + '. Review practical considerations and decide your next step.')),
             ]
    if len(page['candidate_ids']) > 1:
        lines += ['- Candidate next actions (preserved supplied direction): ' + md(json.dumps(page['candidate_next_actions'], ensure_ascii=False))]
    for field in ('reader_job', 'next_action'):
        if editorial.get(field):
            lines += ['- ' + field.replace('_', ' ') + ' (supplied draft): ' + md(editorial[field])]
    lines += ['', '## Suggested structure' + (' (supplied editorial draft; review required)' if editorial.get('outline') else ' (generic scaffold; replace with researched outline)')]
    portfolio_outline = ['Identify the role and reader question', 'Present relevant work evidence and personal contribution', 'Explain decisions, constraints and collaborators', 'Distinguish observed outcomes from planned validation', 'Offer the supplied recruitment next step'] if page['content_purpose'] == 'recruitment_portfolio' else None
    outline = editorial.get('outline') or portfolio_outline or ['Answer the reader’s ' + page['intent'] + ' question directly', 'Explain the decision criteria and important limits', 'Demonstrate the approach with a sourced example', 'Compare relevant alternatives without unsupported claims', 'Summarize and offer the agreed next step']
    lines += [str(i) + '. ' + md(text) for i, text in enumerate(outline, 1)]
    lines += ['', '## Key points and differentiation' + (' (supplied editorial draft; verify)' if editorial.get('key_points') else ' (scaffold)')]
    points = editorial.get('key_points') or [page['rationale'], 'Support claims with primary sources and first-hand examples. Do not invent credentials, outcomes, statistics or urgency.', 'Review competing pages before claiming a content gap; URLs alone do not prove one.']
    lines += ['- ' + md(text) for text in points]
    if editorial.get('differentiation'):
        lines += ['- Differentiation to verify: ' + md(editorial['differentiation'])]
    if editorial.get('evidence_needed'):
        lines += ['', '## Evidence to gather'] + ['- ' + md(text) for text in editorial['evidence_needed']]
    lines += ['', '## Outgoing internal links (proposed)']
    lines += ['- ' + l['to'] + ': ' + md(l['anchor']) + ' (' + l['type'] + ')' for l in plan['links'] if l['from'] == page['id']] or ['- None proposed; relevance review required.']
    lines += ['', '## Incoming internal links (proposed)']
    lines += ['- ' + l['from'] + ': ' + md(l['anchor']) for l in plan['links'] if l['to'] == page['id']] or ['- None proposed; relevance review required.']
    lines += ['', '## Supplied competing result URLs; not content-audited']
    lines += ['- ' + md(u) for u in competing] or ['- No SERP URLs supplied; collect comparable Google organic top ten.']
    lines += ['', '## Existing-page coverage and disposition evidence (supplied; verify)']
    lines += ['- ' + md(json.dumps(record, ensure_ascii=False)) for record in page['coverage_evidence']]
    lines += ['', '## Acceptance checks']
    lines += ['- ' + md(text) for text in editorial.get('acceptance_criteria', [])]
    lines += ['- Resolve provisional intent and evidence gaps', '- Verify title, claims, positioning and intended destination', '- Review actual copy and implemented links after writing']
    if editorial.get('evidence_source_ids'):
        lines += ['', '## Editorial evidence source IDs (supplied; verify)'] + ['- ' + md(source) for source in editorial['evidence_source_ids']]
    if plan['business_context_provenance']:
        lines += ['', '## Appendix: business context provenance (supplied assertions; independently verify)']
        lines += ['- ' + md(k) + ': ' + md(json.dumps(v, sort_keys=True)) for k, v in plan['business_context_provenance'].items()]
    return '\n'.join(lines) + '\n'


def render_map(plan):
    # Escape JSON delimiters, never interpolate untrusted strings into markup or innerHTML.
    payload = json.dumps({'pages': plan['pages'], 'links': plan['links']}, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; base-uri 'none'; form-action 'none'">
<title>Local cluster map</title><style>body{font:16px system-ui;margin:2rem;background:#f5f7fa;color:#152238}input,select{padding:.6rem;margin:.4rem}#pages{display:flex;flex-wrap:wrap;gap:1rem}button{padding:1rem;text-align:left;border:1px solid #62768b;background:white;border-radius:.5rem;max-width:22rem}button:focus{outline:3px solid #4078e0}pre{white-space:pre-wrap}svg{width:100%;height:480px;background:white}text{font:12px system-ui}line{stroke:#a2aebc}circle{fill:#315dae}</style>
<h1>Local cluster map</h1><p>Planned architecture only. No articles published. Select a node or card to inspect its proposed links.</p>
<label>Search <input id="search" type="search"></label><label>Role <select id="role"><option value="">All</option><option>pillar</option><option>spoke</option><option>existing_review</option><option>deferred</option></select></label>
<svg id="graph" viewBox="0 0 1000 480" role="img" aria-label="Planned page and link graph"></svg><div id="pages"></div><h2>Page details</h2><pre id="details" aria-live="polite">Choose a page.</pre>
<script id="data" type="application/json">''' + payload + '''</script><script>
'use strict';const data=JSON.parse(document.getElementById('data').textContent),ns='http://www.w3.org/2000/svg';
function show(p){document.getElementById('details').textContent=JSON.stringify({page:p,outgoing:data.links.filter(x=>x.from===p.id),incoming:data.links.filter(x=>x.to===p.id)},null,2)}
function draw(){const term=document.getElementById('search').value.toLowerCase(),role=document.getElementById('role').value,rows=data.pages.filter(p=>p.title.toLowerCase().includes(term)&&(!role||p.role===role)),ids=new Set(rows.map(p=>p.id)),box=document.getElementById('pages'),svg=document.getElementById('graph');box.replaceChildren();svg.replaceChildren();const pos=new Map(rows.map((p,i)=>[p.id,[500+390*Math.cos(i*2*Math.PI/rows.length),240+190*Math.sin(i*2*Math.PI/rows.length)]]));
for(const l of data.links){if(!ids.has(l.from)||!ids.has(l.to))continue;const a=pos.get(l.from),b=pos.get(l.to),el=document.createElementNS(ns,'line');['x1','y1','x2','y2'].forEach((k,i)=>el.setAttribute(k,[...a,...b][i]));svg.append(el)}
for(const p of rows){const btn=document.createElement('button');btn.textContent=p.title+' · '+p.role+' · '+p.evidence_status;btn.addEventListener('click',()=>show(p));box.append(btn);const [x,y]=pos.get(p.id),g=document.createElementNS(ns,'g'),c=document.createElementNS(ns,'circle'),t=document.createElementNS(ns,'text');c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',p.role==='pillar'?13:9);t.setAttribute('x',x);t.setAttribute('y',y-17);t.setAttribute('text-anchor','middle');t.textContent=p.id;g.append(c,t);g.setAttribute('tabindex','0');g.setAttribute('role','button');g.setAttribute('aria-label',p.title);g.addEventListener('click',()=>show(p));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')show(p)});svg.append(g)}}
document.getElementById('search').addEventListener('input',draw);document.getElementById('role').addEventListener('change',draw);draw();</script></html>'''


def scorecard(plan, briefs_generated=False):
    all_ids = {p['id'] for p in plan['pages']}
    ids = {p['id'] for p in plan['pages'] if p['status'] == 'new_proposal'}
    review_ids = all_ids - ids
    incoming = {i: sum(l['to'] == i for l in plan['links']) for i in ids}
    outgoing = {i: sum(l['from'] == i for l in plan['links']) for i in ids}
    root = plan['pillar_id']
    reached = {root} & ids
    frontier = set(reached)
    for _ in range(2):
        frontier = {l['to'] for l in plan['links'] if l['from'] in frontier} - reached
        reached |= frontier
    return dict(schema_version='cluster-scorecard-1.0', scope='planned architecture and generated briefs only',
                planned_pages=len(all_ids), actionable_planning_pages=sum(p['status'] == 'new_proposal' for p in plan['pages']),
                inventory_status=plan['inventory_status'], disposition_counts={status: sum(p['status'] == status for p in plan['pages']) for status in ('retain', 'review_existing', 'defer', 'new_proposal')},
                normalized_existing_destination_count=len({u for p in plan['pages'] for u in p['existing_urls']}),
                execution_approved=False,
                review_only_count=sum(p['status'] != 'new_proposal' for p in plan['pages']),
                brief_scaffolds_generated=len(all_ids) if briefs_generated else None,
                briefs_with_supplied_editorial_direction=sum(bool(p.get('editorial')) for p in plan['pages']) if briefs_generated else None,
                briefs_generated=len(all_ids) if briefs_generated else None,
                articles_written=None, published_pages=None, implemented_links=None, image_coverage=None,
                measured_content_gaps=None, actual_coverage=None,
                planned_links=len(plan['links']), planned_incoming=incoming, planned_outgoing=outgoing,
                planned_orphans=sorted(i for i, n in incoming.items() if n == 0),
                graph_scope='new_proposal pages only; retained, existing-review and deferred nodes have no automatic links',
                review_pending_unlinked=sorted(review_ids),
                reachable_within_two_clicks=sorted(reached), all_reachable_within_two_clicks=(ids == reached) if ids else None,
                duplicate_primary_keywords=len(plan['pages']) - len({norm_keyword(p['primary_keyword']) for p in plan['pages']}),
                provisional_pages=sum(p['evidence_status'] == 'provisional_intent_only' for p in plan['pages']),
                limitations='Unobserved article, publication, image and implemented-link metrics remain null. A brief is not a written article.')


def artifacts(plan, command='plan'):
    result = {}
    if command == 'plan':
        result['cluster-plan.json'] = json.dumps(plan, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
        result['cluster-plan.md'] = render_plan(plan)
    if command in ('plan', 'map'):
        result['cluster-map.html'] = render_map(plan)
    if command in ('plan', 'execute'):
        for p in plan['pages']:
            result['cluster-briefs/' + p['id'] + '.md'] = brief(plan, p)
    if command in ('plan', 'execute', 'scorecard'):
        report = scorecard(plan, command in ('plan', 'execute'))
        result['cluster-scorecard.json'] = json.dumps(report, indent=2, sort_keys=True) + '\n'
        result['cluster-scorecard.md'] = '# Cluster scorecard\n\n' + '\n'.join('- ' + md(k) + ': ' + md(json.dumps(v, ensure_ascii=False)) for k, v in report.items()) + '\n'
    return result


def write_artifacts(directory, files):
    out = Path(directory)
    require(not out.is_symlink(), 'output directory cannot be a symlink')
    require(not out.exists() or (out.is_dir() and not any(out.iterdir())), 'output directory must be new or empty; evidence is never overwritten')
    require(not any(p.is_symlink() for p in out.absolute().parents), 'output parent cannot be a symlink')
    out.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        relative = Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe artifact path')
        path = out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x', encoding='utf-8') as handle:
            handle.write(content)


def load_plan(path):
    # Rebuild from retained evidence: do not trust arbitrary page IDs as filenames.
    saved = json.loads(Path(path).read_text(encoding='utf-8'))
    require(isinstance(saved, dict) and saved.get('schema_version') == PLAN_SCHEMA, 'unsupported plan schema')
    rebuilt = build_plan(saved.get('evidence_input'))
    require(saved == rebuilt, 'plan does not match retained input; edit input and regenerate instead')
    return rebuilt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('plan', help='Build plan, map, briefs and planning scorecard')
    p.add_argument('--input', required=True)
    p.add_argument('--page-mapping', help='Explicit legacy candidate-to-existing-URL mapping JSON; unknown coverage only')
    p.add_argument('--out', required=True)
    for name in ('map', 'execute', 'scorecard'):
        p = commands.add_parser(name)
        p.add_argument('--plan', required=True)
        p.add_argument('--out', required=True)
        if name == 'execute':
            p.add_argument('--mode', choices=['briefs'], required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'plan':
            data = json.loads(Path(args.input).read_text(encoding='utf-8'))
            if args.page_mapping:
                data = import_page_mapping(data, json.loads(Path(args.page_mapping).read_text(encoding='utf-8')))
            plan = build_plan(data)
        else:
            plan = load_plan(args.plan)
        output = artifacts(plan, args.command)
        write_artifacts(args.out, output)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, 'Error: ' + str(exc) + '\n')
    print(json.dumps({'command': args.command, 'files': sorted(output), 'publication_status': 'not_executed'}))


if __name__ == '__main__':
    main()
