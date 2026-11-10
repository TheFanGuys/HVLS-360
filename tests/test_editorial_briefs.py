import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import editorial_briefs
class EditorialBriefTests(unittest.TestCase):
    def test_no_articles_claimed(self):
        data={"departments":[{"department":"Scissor Lifts, Boom Lifts & MEWPs","leads":[{"title":"New US scissor lift announced","url":"https://example.com/new"}]}]}
        briefs=editorial_briefs.make_briefs(data)
        self.assertEqual(len(briefs),1)
        self.assertEqual(briefs[0]["publisher_approval"],"not_requested")
        self.assertEqual(briefs[0]["source_verification"],"pending")
        self.assertEqual(briefs[0]["status"],"research_required")
    def test_spam_excluded(self):
        data={"departments":[{"department":"Market Intelligence","leads":[{"title":"HVLS market size report to 2035","url":"https://example.com/spam"}]}]}
        self.assertEqual(editorial_briefs.make_briefs(data),[])
    def test_empty(self):
        self.assertEqual(editorial_briefs.make_briefs({"departments":[]}),[])
if __name__=="__main__":unittest.main()
