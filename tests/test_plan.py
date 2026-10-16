import unittest,json,copy
from pathlib import Path
from scripts.validate_plan import validate_plan
ROOT=Path(__file__).resolve().parents[1]
class Checks(unittest.TestCase):
 def setUp(self): self.plan=json.loads((ROOT/'examples/input.json').read_text())
 def test_sample(self): self.assertEqual(validate_plan(self.plan),[])
 def test_capacity(self):
  self.plan['monthly_new_page_capacity']=0
  self.assertIn('New-page capacity exceeded',validate_plan(self.plan))
 def test_conflict(self):
  r=copy.deepcopy(self.plan['keywords'][0]);r['target']='/different';self.plan['keywords'].append(r)
  self.assertTrue(any('Conflicting' in x for x in validate_plan(self.plan)))
 def test_update_requires_existing_page(self):
  self.plan['existing_pages']=[]
  self.assertIn('Update target does not exist',validate_plan(self.plan))
if __name__=='__main__': unittest.main()
