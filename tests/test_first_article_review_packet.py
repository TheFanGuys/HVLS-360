from pathlib import Path
import re
import subprocess
import tempfile
root=Path(__file__).resolve().parents[1]
html=(root/"office"/"first-article-review.html").read_text()
assert "NOT READY FOR APPROVAL OR PUBLICATION" in html
assert "No approval control is provided" in html
assert "innerHTML" not in html
assert "rel='noopener noreferrer'" in html
for path in ["editorial/drafts/hvls-air-movement-vs-ventilation.md","editorial/reviews/hvls-air-movement-vs-ventilation-review.md","editorial/media/hvls-air-movement-candidates.json"]:
 assert (root/path).exists()
js=re.search(r"<script>(.*?)</script>",html,re.S)
assert js
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as f:
 f.write(js.group(1));f.flush()
 subprocess.run(["node","--check",f.name],check=True)
print("First article review packet safety and syntax checks passed")
