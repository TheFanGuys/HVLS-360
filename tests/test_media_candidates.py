import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"editorial"/"media"/"hvls-air-movement-candidates.json"
d=json.loads(p.read_text())
assert d["status"]=="authentic_source_candidates_rights_not_cleared"
assert d["candidates"]
for item in d["candidates"]:
 assert item["image_url"].startswith("https://")
 assert item["original_page"].startswith("https://bigassfans.com/")
 assert item["license"]=="not_verified"
 assert item["publication_allowed"] is False
print("Manufacturer photo source and rights hold checks passed")
