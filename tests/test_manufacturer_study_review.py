import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import manufacturer_study_review as m
class StudyReviewTests(unittest.TestCase):
    def test_blank_evidence_and_no_approval(self):
        d={"sources":[{"source":"Big Ass Fans","candidate_urls":["https://bigassfans.com/research/airflow"]}]}
        r=m.review_records(d)
        self.assertEqual(len(r),1)
        self.assertTrue(all(v is None for v in r[0]["evidence"].values()))
        self.assertEqual(r[0]["publisher_approval"],"not_requested")
    def test_reject_http(self):
        d={"sources":[{"source":"Example","candidate_urls":["http://example.com/study"]}]}
        self.assertEqual(m.review_records(d),[])
if __name__=="__main__":unittest.main()
