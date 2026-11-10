import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import research_director as rd
class DirectorTests(unittest.TestCase):
    def test_market_spam_hold(self):
        status,_=rd.triage("HVLS Fans Market Size Report to 2035","Market Intelligence","https://example.org/a")
        self.assertEqual(status,"hold")
    def test_relevant_lift(self):
        status,notes=rd.triage("Skyjack launches new scissor lift in USA","Scissor Lifts, Boom Lifts & MEWPs","https://example.org/a")
        self.assertEqual(status,"review")
    def test_international_not_automatically_approved(self):
        status,notes=rd.triage("Industrial ventilation HVLS fan launched in Europe","New Products","https://example.org/a")
        self.assertEqual(status,"hold")
        self.assertTrue(any("International story" in n for n in notes))
    def test_off_topic(self):
        status,_=rd.triage("Supermarket fridges hit by cyberattack","Controls & VFDs","https://example.org/a")
        self.assertEqual(status,"hold")
    def test_empty(self):
        self.assertEqual(rd.audit({"departments":[]}),[])
if __name__=="__main__":
    unittest.main()
