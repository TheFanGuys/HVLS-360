from pathlib import Path
import re
import subprocess
import tempfile
p=Path(__file__).resolve().parents[1]/"office"/"editorial-board.html"
html=p.read_text(encoding="utf-8")
assert 'publisher_review' in html
assert 'does not publish' in html.lower()
assert 'Import assignment JSON' in html
assert 'innerHTML' not in html
assert "fetch('./editorial-latest.json?fresh='" in html
assert 'unverified_assignment_briefs_not_articles' in html
js=re.search(r"<script>(.*?)</script>",html,re.S)
assert js
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as tmp:
    tmp.write(js.group(1))
    tmp.flush()
    subprocess.run(["node","--check",tmp.name],check=True)
print("Editorial board checks passed")
