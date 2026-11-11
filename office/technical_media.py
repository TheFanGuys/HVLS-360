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
        vividair=("vividair" in filename.lower() or "gfy" in filename.lower())
        results.insert(0,{"subject":("Model-verified VividAir / GFY photo needed for " if vividair else "Authentic HVLS fan installation for ")+filename,
            "manufacturer_link":("https://bigfanguys.com/" if vividair else None),"visual_type":"authentic_editorial_hero_photo",
            "image_url":None,"image_rights":("publisher_authorized_big_fan_guys_site" if vividair else "not_verified"),"model_accuracy":"not_verified",
            "alt_text":None,"caption":None,"status":"media_research_required",
            "notes":("First search BigFanGuys.com owner-authorized photographs; the publisher supplied three identified 72-inch TAZ photos separately. Verify exact model before labeling; do not substitute Patterson barrel fans. Check site/customer privacy and avoid a separate photo gallery." if vividair else "First check BigFanGuys.com for publisher-authorized original field photography, then verify manufacturer/model, site privacy and appropriate crop; do not build a photo gallery.")})
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
