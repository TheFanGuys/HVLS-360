import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
from research_director import triage
class RelevanceTests(unittest.TestCase):
 def test_rental_desk_not_automatic_pass(self):
  status,_=triage("EquipmentShare supports veterans with donations","Rental Industry & Jobsite Economics","https://example.com")
  self.assertEqual(status,"hold")
 def test_construction_desk_not_automatic_pass(self):
  status,_=triage("Company announces quarterly results","Construction & Lifts","https://example.com")
  self.assertEqual(status,"hold")
 def test_industrial_fan_passes_to_review(self):
  status,_=triage("New industrial ceiling fan controls","Manufacturer Watch","https://example.com")
  self.assertEqual(status,"review")
 def test_aerial_lift_passes_to_review(self):
  status,_=triage("New scissor lift model announced for warehouses","Rental Industry & Jobsite Economics","https://example.com")
  self.assertEqual(status,"review")
 def test_international_still_held(self):
  status,_=triage("New industrial fan opens in Germany","Manufacturer Watch","https://example.com")
  self.assertEqual(status,"hold")
if __name__=="__main__":unittest.main()
