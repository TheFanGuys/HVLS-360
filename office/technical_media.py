#!/usr/bin/env python3
"""Prepare authentic manufacturer visual/link requests; does not copy images."""
import json
import pathlib
import re
ROOT=pathlib.Path(__file__).resolve().parents[1]
CATALOG=[{"pattern":r"\bABB\s+ACH580\b","name":"ABB ACH580 HVACR drive","official_url":"https://new.abb.com/us/us-motion-business-area/drives-products/industry-specific-drives/drives-for-hvac/ach580"}]
def requests(article_text):
    out=[]
    for entry in CATALOG:
        if re.search(entry["pattern"],article_text,re.I):
            out.append({"subject":entry["name"],"manufacturer_link":entry["official_url"],
              "visual_type":"official_product_photo_preferred",
              "image_url":None,"image_rights":"not_verified","model_accuracy":"not_verified",
              "alt_text":None,"caption":None,"status":"media_research_required",
              "notes":"Link to official product page is allowed; do not copy or republish manufacturer photo without rights review."})
    return out
def main():
    draft=ROOT/"editorial"/"drafts"/"hvls-air-movement-vs-ventilation.md"
    out={"schema_version":1,"status":"visual_requests_not_approved_assets",
         "requests":requests(draft.read_text(encoding="utf-8"))}
    dest=ROOT/"office"/"reports"/"technical-media-requests.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("Technical media requests:",len(out["requests"]))
if __name__=="__main__":main()
