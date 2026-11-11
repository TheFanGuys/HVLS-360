import pathlib,sys,unittest,datetime as dt,json,tempfile
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'office'))
import manufacturer_news as news
import research,editorial_briefs,coo_issues
BASE='https://www.invertekdrives.com/news'
def article(title='Optidrive E4 diagnostics update',date='Nov 10, 2026',url='/news/general-news/e4'):
 return '<article><span class="post-date"><i></i>'+date+'</span><h2><a class="post-link" href="'+url+'">'+title+'</a></h2></article>'
class ManufacturerNewsTests(unittest.TestCase):
 def test_official_title_date_and_link(self):
  row=news.entries(article(),BASE)[0]
  self.assertEqual(row['url'],BASE+'/general-news/e4')
  self.assertEqual(row['published'],'2026-11-10')
  self.assertEqual(row['date_basis'],'publisher_reported_date_only')
 def test_missing_invalid_and_off_source_entries_rejected(self):
  self.assertFalse(news.entries(article(date='not dated'),BASE))
  self.assertFalse(news.entries(article(url='https://evil.example/news/e4'),BASE))
  self.assertFalse(news.entries(article(url='http://www.invertekdrives.com/news/e4'),BASE))
 def test_bounded_articles(self):
  self.assertEqual(len(news.entries(article()*100,BASE)),news.MAX_ARTICLES)
 def test_manufacturer_index_flows_to_shared_assignment_candidates(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);(root/'office').mkdir()
   (root/'office/sources.json').write_text(json.dumps({'departments':[{'name':'Controls & VFDs','feeds':[{'name':'Official','url':BASE,'type':'manufacturer_news_html','parser':'invertek_news'}]}]}))
   with patch.object(research,'ROOT',root),patch.object(news,'fetch',return_value=(article()+article(title='Old Optidrive update',date='Jan 01, 2024')).encode()):
    self.assertEqual(research.run(dt.datetime(2026,11,11,tzinfo=dt.timezone.utc)),0)
   data=json.loads((root/'office/research-latest.json').read_text());rows=data['departments'][0]['leads'];self.assertEqual(len(rows),1)
   briefs=editorial_briefs.make_briefs(data);self.assertEqual(len(briefs),1)
   items=coo_issues.build_items(briefs);self.assertEqual(len(items),1)
   self.assertEqual(items[0]['source'],BASE+'/general-news/e4')
   self.assertEqual(briefs[0]['us_relevance'],'unverified')
 def test_layout_change_is_visible_error(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);(root/'office').mkdir();(root/'office/sources.json').write_text(json.dumps({'departments':[{'name':'Controls','feeds':[{'name':'Official','url':BASE,'type':'manufacturer_news_html','parser':'invertek_news'}]}]}))
   with patch.object(research,'ROOT',root),patch.object(news,'fetch',return_value=b'<html>changed layout</html>'):
    self.assertEqual(research.run(dt.datetime(2026,11,11,tzinfo=dt.timezone.utc)),2)
   self.assertTrue(json.loads((root/'office/research-latest.json').read_text())['errors'])

class SampleLimitTests(unittest.TestCase):
 def test_large_archive_uses_complete_bounded_sample(self):
  import io
  class Response(io.BytesIO):
   headers={'Content-Type':'text/html'}
   def geturl(self):return BASE
  data=(article()*50).encode()
  with patch.object(news,'MAX_ARTICLES',2),patch.object(news,'MAX_BYTES',len(article().encode())*3),patch('urllib.request.urlopen',return_value=Response(data)):
   raw=news.fetch(BASE)
   self.assertEqual(len(raw),len(article().encode())*3)
   self.assertEqual(len(news.entries(raw,BASE)),2)
 def test_incomplete_oversized_archive_stays_visible_failure(self):
  import io
  class Response(io.BytesIO):
   headers={'Content-Type':'text/html'}
   def geturl(self):return BASE
  with patch.object(news,'MAX_BYTES',50),patch('urllib.request.urlopen',return_value=Response(b'<html>'+b'x'*100)):
   with self.assertRaisesRegex(ValueError,'bounded sample'):news.fetch(BASE)
