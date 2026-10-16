"""Verify pinned reference bytes, not execution of upstream instructions."""
from pathlib import Path
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1]/'upstream/claude-seo'
class UpstreamModuleIntegrity(unittest.TestCase):
 def test_complete_module_snapshot(self):
  lock=json.loads((ROOT/'SOURCE-MODULE.json').read_text())
  self.assertEqual(lock['commit'],'4b99de2f7de7e7d5247042e5fb5b4ea9368ef734')
  self.assertEqual(len(lock['files']),6)
  for item in lock['files']:
   with self.subTest(path=item['path']):
    data=(ROOT/item['path']).read_bytes()
    self.assertEqual(len(data),item['bytes'])
    self.assertEqual(hashlib.sha256(data).hexdigest(),item['sha256'])
    self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),item['git_blob_sha1'])
if __name__=='__main__':unittest.main()
