"""Supplied-answer validation and conservative commissioning gates; no data collection."""
FIELDS = ('industry', 'audience', 'geography', 'language', 'brand_position',
          'competitive_position', 'lifecycle', 'primary_objective',
          'conversion_definition', 'resources', 'constraints', 'business_problem', 'objective_tradeoffs', 'website_stage', 'brand_lifecycle', 'product_lifecycle')
ESSENTIAL = ('industry', 'audience', 'geography', 'language', 'primary_objective')
OBJECTIVES = {'awareness', 'consideration', 'conversion', 'retention', 'other'}
QUESTIONS = {
 'brand_lifecycle': 'If different from the product, what stage is the brand at?',
 'product_lifecycle': 'If different from the brand, what stage is this product/offer at?',
 'business_problem': 'What concrete marketing or customer problem should this report help decide? Unknown is fine.',
 'objective_tradeoffs': 'Which secondary goals must not override the primary objective?',
 'website_stage': 'Separately from brand/product lifecycle, how old is the site and what measurement history exists?',
 'industry': 'What industry, offer and business model is this for?',
 'audience': 'Who is the primary audience, and what decision or problem brings them here?',
 'geography': 'Which geographic market should this plan address?',
 'language': 'Which content language should this plan use?',
 'primary_objective': 'What is the one primary objective: awareness, consideration, conversion, retention or other?',
 'brand_position': 'How is the brand positioned today, and which differentiators have evidence versus assumptions?',
 'competitive_position': 'What alternatives do customers consider, and what evidence supports the claimed competitive position?',
 'lifecycle': 'What stage is the product/brand at (prelaunch, launch, growth, mature, repositioning or other)?',
 'conversion_definition': 'What exact action counts as conversion, for whom, and how could it be measured?',
 'resources': 'What production/review capacity, expertise, assets and measurement access are available?',
 'constraints': 'What timing, budget, approval, regulatory, brand voice or claim restrictions apply? State none if none.',
}


def intake(data, source_ids):
    raw = data.get('business_context', {})
    if not isinstance(raw, dict):
        raise ValueError('business_context must be an object')
    answers = {}
    for field in FIELDS:
        answer = raw.get(field, {'status': 'unknown', 'value': None, 'source_ids': []})
        if not isinstance(answer, dict) or answer.get('status') not in {'supplied', 'assumed', 'unknown'}:
            raise ValueError('invalid answer status: '+field)
        status, value, refs = answer['status'], answer.get('value'), answer.get('source_ids', [])
        if not isinstance(refs, list) or any(s not in source_ids for s in refs):
            raise ValueError('unknown intake source: '+field)
        if status != 'unknown' and (not isinstance(value, str) or not value.strip()):
            raise ValueError('answer value required: '+field)
        if status == 'supplied' and not refs:
            raise ValueError('supplied answer needs source_ids: '+field)
        if status == 'unknown' and value not in (None, ''):
            raise ValueError('unknown answer must not hide a value: '+field)
        if field == 'primary_objective' and status != 'unknown' and value not in OBJECTIVES:
            raise ValueError('unsupported primary_objective')
        answers[field] = dict(status=status, value=value, source_ids=refs)
    objective = answers['primary_objective']['value']
    required = list(ESSENTIAL) + ['business_problem', 'lifecycle', 'resources', 'constraints']
    if objective == 'conversion': required.append('conversion_definition')
    missing = [f for f in required if answers[f]['status'] != 'supplied']
    # Positioning is never silently treated as a fact, even if basic planning can proceed.
    unknown_position = [f for f in ('brand_position', 'competitive_position') if answers[f]['status'] == 'unknown']
    missing += unknown_position
    first = [f for f in ESSENTIAL if answers[f]['status'] != 'supplied']
    follow = [f for f in missing if f not in first]
    # Keep first conversation round small; an explicit unknown is a valid answer and allows a limited report.
    unanswered = [f for f in first + follow if f not in raw]
    questions = [dict(field=f, question=QUESTIONS[f]) for f in unanswered[:3]]
    return dict(answers=answers, missing_for_commission=missing,
                report_mode=('generic_framework' if answers['industry']['status'] != 'supplied' else 'industry_general' if missing else 'tailored'),
                commissioning_status='limited' if missing else 'context_ready',
                next_questions=questions, assumptions=[f for f in FIELDS if answers[f]['status']=='assumed'],
                objective=objective,
                note='Supplied answers are traceable statements, not independent verification. Unknown is accepted; do not fabricate priorities.')


def keyword_gate(row, context, source_ids):
    if row.get('brand_scope', 'unknown') not in {'brand', 'nonbrand', 'competitor', 'unknown'}:
        raise ValueError('invalid brand_scope')
    if row.get('funnel_stage', 'unknown') not in {'awareness', 'consideration', 'conversion', 'retention', 'navigation', 'unknown'}:
        raise ValueError('invalid funnel_stage')
    evidence = row.get('priority_evidence')
    if not evidence:
        return 'priority needs objective-linked rationale and cited supplied source'
    if not isinstance(evidence, dict) or evidence.get('source_id') not in source_ids or not isinstance(evidence.get('rationale'), str) or not evidence['rationale'].strip():
        raise ValueError('invalid priority_evidence')
    if evidence.get('objective') != context['objective']:
        return 'priority rationale does not match the primary objective'
    if row.get('brand_scope', 'unknown') == 'unknown' or row.get('funnel_stage', 'unknown') == 'unknown':
        return 'brand/nonbrand role and funnel stage require clarification'
    if row.get('business_priority') is None:
        return 'business priority unknown; no inferred ordering'
    return None


def report_guidance(context):
    """Editorial heuristics explicitly separated from industry evidence."""
    objective = context['objective']
    guidance = {
      'awareness': 'Assess problem/category education and credible brand associations; a visit is not a lead or a sale.',
      'consideration': 'Assess decision criteria, relevant proof and alternatives; avoid unverified superiority claims.',
      'conversion': 'Assess the defined conversion event, offer fit and friction; distinguish CTA clicks from completed outcomes.',
      'retention': 'Assess existing-customer tasks, adoption and support navigation; acquisition keywords may be irrelevant.',
      'other': 'Clarify the objective-specific success signal before assigning an editorial queue.',
    }.get(objective, 'Compare education, evaluation, action and retention use cases as an industry-general reference; ask which problem matters before ranking work.')
    stage = context['answers']['lifecycle']['value'] or 'unknown'
    return dict(editorial_heuristic=guidance,
                lifecycle=stage,
                brand_lifecycle=context['answers']['brand_lifecycle']['value'] or stage,
                product_lifecycle=context['answers']['product_lifecycle']['value'] or stage,
                lifecycle_caution='Use stage as supplied context, not evidence of demand. Prelaunch/launch work must not imply proven adoption; mature/repositioning work must check existing equity and coverage before replacing content.',
                brand_caution='Brand terms can serve entity navigation or reassurance; nonbrand terms can serve problem discovery; competitor terms need verified comparison facts. None automatically means higher value.',
                reference_value='Even without a concrete problem, the report can organize supplied intent, page coverage, evidence gaps and useful validation questions. This is general planning guidance, not invented industry research.')
