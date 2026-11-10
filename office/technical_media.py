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
def article_requests(article_text, filename):
    if "publication_allowed: false" not in article_text:
        return []
    results=requests(article_text)
    if len(article_text.split()) >= 250:
        results.insert(0,{"subject":"Authentic HVLS fan installation for "+filename,
            "manufacturer_link":None,"visual_type":"authentic_editorial_hero_photo",
            "image_url":None,"image_rights":"not_verified","model_accuracy":"not_verified",
            "alt_text":None,"caption":None,"status":"media_research_required",
            "notes":"Find a real industrial installation photo with permission, accurate fan/structure depiction and appropriate crop."})
    return [{**item,"draft_file":filename} for item in results]
def main():
    records=[]
    for draft in sorted((ROOT/"editorial"/"drafts").glob("*.md")):
        records.extend(article_requests(draft.read_text(encoding="utf-8"),draft.name))
    out={"schema_version":1,"status":"visual_requests_not_approved_assets",
         "requests":records}
    dest=ROOT/"office"/"reports"/"technical-media-requests.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    public=ROOT/"office"/"media-latest.json"
    public.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Technical media requests:",len(out["requests"]))
if __name__=="__main__":main()
