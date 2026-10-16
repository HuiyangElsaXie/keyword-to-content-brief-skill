"""Validate planning constraints, not SEO effectiveness."""
def validate_plan(plan):
    errors=[]
    rows=plan.get('keywords',[])
    new_targets={r.get('target') for r in rows if r.get('decision')=='new'}
    if None in new_targets: errors.append('New pages need a target path')
    if len(new_targets)>plan.get('monthly_new_page_capacity',0): errors.append('New-page capacity exceeded')
    seen={}
    for row in rows:
        k=row['keyword'].strip().casefold()
        if k in seen and seen[k]!=row.get('target'): errors.append('Conflicting target for '+k)
        seen[k]=row.get('target')
        if row.get('decision')=='update' and row.get('target') not in plan.get('existing_pages',[]): errors.append('Update target does not exist')
    return errors
