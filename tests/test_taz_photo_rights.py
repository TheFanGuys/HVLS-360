import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
record=json.loads((root/"editorial/media/publisher/taz-72-rights.json").read_text())
assert record["count"]==3
assert "Explicit permission" in record["permission"]
assert record["public_assets_uploaded"] is False
assert "Patterson" in record["correction"]
print("TAZ photo rights and manufacturer identification correction recorded")
