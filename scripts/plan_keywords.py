#!/usr/bin/env python3
"""Offline evidence planner. See ATTRIBUTION.md for adapted overlap heuristic."""
import argparse
import itertools
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

try:
    from .business_intake import intake, keyword_gate, report_guidance
except ImportError:
    from business_intake import intake, keyword_gate, report_guidance

INTENTS = {'informational', 'commercial', 'transactional', 'navigational', 'mixed'}
TRACKING = {'gclid', 'fbclid', 'msclkid'}


def norm_keyword(text):
    return ' '.join(unicodedata.normalize('NFKC', text).casefold().split())


def norm_url(url):
    u = urlsplit(url)
    if u.scheme not in {'http', 'https'} or not u.hostname or u.username or u.password:
        raise ValueError('SERP URL must be public-form HTTP(S) without credentials')
    query = [(k,v) for k,v in parse_qsl(u.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in TRACKING]
    # Preserve scheme, semantic queries and path case; do not invent canonicals.
    return urlunsplit((u.scheme, u.netloc.lower(), u.path.rstrip('/') or '/', urlencode(sorted(query)), ''))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def prepare(data):
    require(isinstance(data, dict), 'Input must be an object')
    for f in ('project', 'audience', 'goal'):
        require(isinstance(data.get(f), str) and bool(data[f].strip()), f + ' required')
    require(type(data.get('fictional')) is bool, 'fictional boolean required')
    cap = data.get('monthly_new_page_capacity')
    require(type(cap) is int and cap >= 0, 'capacity must be nonnegative integer')
    sources = data.get('sources', [])
    require(isinstance(sources,list) and len(sources)>0, 'sources required')
    source_ids = set()
    for s in sources:
        require(isinstance(s,dict) and isinstance(s.get('id'),str) and bool(s['id']), 'source id required')
        require(s['id'] not in source_ids, 'duplicate source id')
        require(s.get('kind') in {'synthetic','supplied'} and bool(s.get('description')), 'source provenance required')
        source_ids.add(s['id'])
    if not data['fictional']:
        require(not any(s['kind']=='synthetic' for s in sources), 'synthetic sources require fictional=true')
    raw = data.get('keywords')
    require(isinstance(raw,list) and bool(raw), 'keywords required')
    ids, seen, rows = set(), {}, []
    for r in raw:
        require(isinstance(r,dict) and isinstance(r.get('id'),str) and bool(r['id']), 'keyword id required')
        require(r['id'] not in ids, 'duplicate keyword id')
        ids.add(r['id'])
        require(isinstance(r.get('keyword'),str) and bool(norm_keyword(r['keyword'])), 'keyword text required')
        require(r.get('intent') in INTENTS and bool(r.get('intent_reason')), 'intent and reason required')
        require(r.get('business_priority') is None or (type(r['business_priority']) is int and 1<=r['business_priority']<=5), 'priority must be null or integer 1-5')
        require(r.get('source_id') in source_ids, 'unknown keyword source')
        ss = r.get('serp')
        urls = set()
        if ss is not None:
            require(isinstance(ss,dict) and ss.get('source_id') in source_ids, 'unknown SERP source')
            for f in ('date','market','language','device'):
                require(isinstance(ss.get(f),str) and bool(ss[f].strip()), 'SERP context required: '+f)
            try: date.fromisoformat(ss['date'])
            except ValueError: raise ValueError('invalid SERP date')
            require(isinstance(ss.get('organic_urls'),list) and all(isinstance(u,str) for u in ss['organic_urls']), 'organic_urls list required')
            urls = set(norm_url(u) for u in ss['organic_urls'])
            require(len(urls)<=10, 'supply at most top 10 unique URLs')
        key = norm_keyword(r['keyword'])
        fingerprint = (r['intent'],r.get('business_priority'),json.dumps(ss,sort_keys=True),r['source_id'],json.dumps({k:r.get(k) for k in ('brand_scope','funnel_stage','priority_evidence')},sort_keys=True))
        if key in seen:
            old, fp = seen[key]
            require(fingerprint == fp, 'conflicting duplicate keyword: '+key)
            old['input_ids'].append(r['id'])
            continue
        row = dict(r, keyword=key, input_ids=[r['id']], urls=urls, serp=ss)
        seen[key] = row, fingerprint
        rows.append(row)
    pages = data.get('existing_pages')
    require(isinstance(pages,list), 'existing_pages list required')
    paths=set()
    for p in pages:
        require(isinstance(p,dict) and isinstance(p.get('path'),str) and p['path'].startswith('/') and not p['path'].startswith('//') and '?' not in p['path'] and '#' not in p['path'], 'inventory requires site path')
        require(p['path'] not in paths, 'duplicate inventory path')
        paths.add(p['path'])
        require(isinstance(p.get('title'),str) and bool(p['title']), 'inventory title required')
        require(isinstance(p.get('keyword_ids'),list) and all(i in ids for i in p['keyword_ids']), 'unknown inventory keyword id')
    context = intake(data, source_ids)
    for r in rows:
        keyword_gate(r, context, source_ids)
    for p in pages:
        review = p.get('coverage_review')
        if review is not None:
            require(isinstance(review,dict) and review.get('result') in {'gap','covered','unknown'}, 'invalid coverage_review')
            require(isinstance(review.get('source_id'),str) and review['source_id'] in source_ids and isinstance(review.get('detail'),str) and bool(review['detail'].strip()), 'coverage review needs evidence and detail')
    return rows


def overlap(a,b):
    if a['serp'] is None or b['serp'] is None:
        return None, 'missing_snapshot'
    if len(a['urls']) != 10 or len(b['urls']) != 10:
        return None, 'incomplete_snapshot'
    if any(a['serp'][k] != b['serp'][k] for k in ('date','market','language','device')):
        return None, 'incompatible_context'
    n = len(a['urls'] & b['urls'])
    return n, 'same_page_candidate' if n>=7 else 'topic_candidate' if n>=4 else 'cross_link_candidate' if n>=2 else 'separate'


def plan(data):
    rows = prepare(data)
    context = intake(data, {s['id'] for s in data['sources']})
    sources = {s['id'] for s in data['sources']}
    pairs, scores = [], {}
    for a,b in itertools.combinations(rows,2):
        n, relation = overlap(a,b)
        scores[frozenset((a['id'],b['id']))] = n
        pairs.append(dict(a=a['id'],b=b['id'],shared_top10=n,relation=relation,
                          intent_compatible=a['intent']==b['intent'] and a['intent'] not in {'mixed','navigational'}))
    # Deterministic complete-link greedy groups. A-B and B-C alone cannot merge A-C.
    groups=[]
    for row in sorted(rows,key=lambda r:((r.get('business_priority') or 99) if not context['missing_for_commission'] and not keyword_gate(r,context,sources) else 99,r['id'])):
        for group in groups:
            if row['intent'] not in {'mixed','navigational'} and all(
                r['intent']==row['intent'] and (scores.get(frozenset((r['id'],row['id']))) or 0)>=7 for r in group):
                group.append(row)
                break
        else:
            groups.append([row])
    decisions=[]
    used = {p['path'] for p in data['existing_pages']}
    new_count=0
    for n, group in enumerate(groups,1):
        ids = [i for r in group for i in r['input_ids']]
        targets = [p['path'] for p in data['existing_pages'] if set(ids)&set(p['keyword_ids'])]
        complete = all(r['serp'] is not None and len(r['urls'])==10 for r in group)
        primary = group[0]
        action,target='defer',None
        gates = [keyword_gate(r, context, sources) for r in group]
        gate = next((g for g in gates if g), None)
        if context['missing_for_commission']: gate = 'business intake incomplete: '+', '.join(context['missing_for_commission'])
        if primary['intent']=='navigational':
            if len(targets)==1: action,target='review_existing',targets[0]
            reason='navigational: verify the intended known entity and destination in supplied inventory; no article commission'
        elif primary['intent']=='mixed': reason='mixed intent: analyst must resolve reader job before commissioning'
        elif len(targets)>1: reason='multiple inventory targets: consolidation review required; no redirect authorized'
        elif targets:
            target=targets[0]
            review=next(p for p in data['existing_pages'] if p['path']==target).get('coverage_review', {})
            if review.get('result')=='covered': action,reason='retain','supplied coverage review finds no gap; preserve current page'
            elif review.get('result')=='gap' and not gate: action,reason='update','supplied page-content gap and objective-linked priority support a reviewable change proposal: '+review['detail']
            else: action,reason='review_existing','inventory mapping is not a verified gap; review current coverage before proposing changes'+('; '+gate if gate else '')
        elif not complete: reason='missing or incomplete top-10 evidence: collect comparable evidence before commissioning'
        elif gate: reason=gate
        elif any(r['serp']['market'] != context['answers']['geography']['value'] or r['serp']['language'] != context['answers']['language']['value'] for r in group): reason='snapshot differs from intake target market/language; no commission'
        elif new_count>=data['monthly_new_page_capacity']: reason='new-page capacity exhausted; retain in backlog'
        else:
            action='new';new_count+=1
            slug=re.sub(r'[^a-z0-9]+','-',primary['keyword']).strip('-') or primary['id'].lower()
            target='/guides/'+slug
            while target in used: target += '-'+primary['id'].lower()
            used.add(target)
            reason='complete supplied snapshot; selected by business priority within capacity; editorial approval pending'
        decisions.append(dict(group_id='G'+str(n),input_ids=ids,keywords=[r['keyword'] for r in group],
            primary_keyword=primary['keyword'],intent=primary['intent'],business_priority=primary.get('business_priority') if not gate else None,
            supplied_priority=primary.get('business_priority'), priority_gate=gate,
            brand_scope=primary.get('brand_scope','unknown'),funnel_stage=primary.get('funnel_stage','unknown'),
            decision=action,target=target,reason=reason,evidence_source_ids=sorted({r['source_id'] for r in group}|{r['serp']['source_id'] for r in group if r['serp']}),
            evidence_basis='synthetic demonstration' if data['fictional'] else 'supplied evidence, not independently verified',
            snapshot_complete=complete,review_status='needs_human_review'))
    work_items=[]
    for d in decisions:
        if not d['target']: continue
        item=next((w for w in work_items if w['target']==d['target']),None)
        if item is None:
            item=dict(target=d['target'],group_ids=[],input_ids=[],actions=[],keyword_relationship='Inventory co-routing only; separate group IDs do not establish a keyword cluster.')
            work_items.append(item)
        item['group_ids'].append(d['group_id']);item['input_ids'] += d['input_ids']
        if d['decision'] not in item['actions']: item['actions'].append(d['decision'])
    return dict(schema_version='0.3',business_context=context,guidance=report_guidance(context),work_items=work_items,project=data['project'],fictional=data['fictional'],
        status='needs_human_review',input_rows=len(data['keywords']),unique_keywords=len(rows),
        new_pages=new_count,monthly_new_page_capacity=data['monthly_new_page_capacity'],
        decisions=decisions,pairs=pairs,
        limitations=['No search-volume, traffic or ranking claims.', 'Intent and inventory mappings are supplied analyst judgments.',
            'Same-page grouping is a heuristic requiring editorial review; no merge/redirect is executed.',
            'Single-snapshot decisions do not prove freshness, demand or conversion value.',
            'Update workload is outside the new-page cap and must be estimated separately.'])


def write_outputs(data,result,out):
    out=Path(out)
    if out.exists() and any(out.iterdir()): raise ValueError('output directory is nonempty; preserve previous evidence')
    out.mkdir(parents=True,exist_ok=True)
    (out/'plan.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    lines=['# Keyword page decisions', '', 'Status: needs_human_review. '+('SYNTHETIC CASE; NOT OBSERVED SEARCH RESULTS.' if result['fictional'] else 'Supplied evidence; not independently verified.'),'']
    lines += ['## Business context / report gate', 'Mode: '+result['business_context']['report_mode'], 'Missing: '+', '.join(result['business_context']['missing_for_commission']), 'Assumed: '+', '.join(result['business_context']['assumptions']), '']
    for field, answer in result['business_context']['answers'].items():
        lines += [f"- {field}: {answer['value'] or 'unknown'} ({answer['status']}; sources: {', '.join(answer['source_ids']) or 'none'})"]
    lines += ['', '## Reference guidance (editorial heuristics, not market evidence)'] + ['- '+v for v in result['guidance'].values()]
    lines += ['', '## Next intake questions'] + ['- '+q['question'] for q in result['business_context']['next_questions']] + ['']
    for d in result['decisions']:
        lines += [f"## {d['group_id']}: {d['decision']} — {d['primary_keyword']}",
                  f"- Input IDs: {', '.join(d['input_ids'])}",f"- Target: {d['target'] or 'none'}",f"- Reason: {d['reason']}",f"- Evidence: {', '.join(d['evidence_source_ids'])}; {d['evidence_basis']}",'']
    lines += ['## Assumptions and next validation', 'Supplied intent, positioning and priorities are hypotheses unless backed by the cited evidence. Validate page coverage, reader job, claims and workload before changes.', 'Industry-general output remains useful as a reference for evaluating supplied evidence and planning questions; it is not company-specific opportunity ranking. Generic-framework output contains no industry claims.', '## Limits']+['- '+x for x in result['limitations']]
    (out/'plan.md').write_text('\n'.join(lines)+'\n')
    briefs=['# Brief scaffolds: editorial work still required','', 'These are routing scaffolds, not completed writing briefs. Read the skill and complete the reader job, evidence-led outline and claim review.','']
    for w in result['work_items']:
        ds=[d for d in result['decisions'] if d['group_id'] in w['group_ids']]
        briefs += [f"## {w['target']}", f"- Actions: {', '.join(w['actions'])}", f"- Input IDs: {', '.join(w['input_ids'])}", f"- Groups: {', '.join(w['group_ids'])}", '- '+w['keyword_relationship'],
                   '- Objective: '+str(result['business_context']['objective'] or 'unknown'),
                   '- Lifecycle: '+str(result['business_context']['answers']['lifecycle']['value'] or 'unknown'),
                   '- Routing: '+ '; '.join(d['reason'] for d in ds),
                   '- Complete: reader job, objective/funnel fit, brand/nonbrand role, appropriate next action, evidence, workload and measurement definition.',
                   '- Review/retain means inspect or preserve, not rewrite. Unknown context means limited report, not ranked execution queue.',
                   '- Gate: no unsupported product, competitor, demand, pricing, performance or security claims.', '']
    (out/'brief-scaffolds.md').write_text('\n'.join(briefs)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input');p.add_argument('--out',required=True);args=p.parse_args()
    try:
        data=json.loads(Path(args.input).read_text());result=plan(data);write_outputs(data,result,args.out)
    except (ValueError,TypeError,KeyError,OSError) as exc:
        p.exit(2,'Input/output error: '+str(exc)+'\n')
    print(f"{result['unique_keywords']} unique keywords; {result['new_pages']} new page(s); review pending")
if __name__=='__main__': main()
