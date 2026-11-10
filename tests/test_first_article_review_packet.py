from pathlib import Path
import re
import subprocess
import tempfile

root=Path(__file__).resolve().parents[1]
html=(root/"office"/"first-article-review.html").read_text(encoding="utf-8")
assert 'name="robots" content="noindex,nofollow,noarchive"' in html
assert "No approval control is provided" in html
assert "innerHTML" not in html
assert "fetch(" not in html, "The hosted workbench must never fetch unpublished manuscripts"
assert "file.text()" in html
assert "air-movement-vs-ventilation.svg" in html
assert "img.loading=" in html
assert "renderMarkdown" in html
assert "rel='noopener noreferrer'" in html
assert "View source page" in html
for file in ["editorial/drafts/hvls-air-movement-vs-ventilation.md",
             "editorial/reviews/hvls-air-movement-vs-ventilation-review.md",
             "editorial/media/hvls-air-movement-candidates.json"]:
    assert (root/file).exists()
for file in ["office/command-center.html","office/editorial-board.html",
             "office/technical-review.html","office/media-desk.html"]:
    assert 'name="robots" content="noindex,nofollow,noarchive"' in (root/file).read_text()
js=re.search(r"<script>(.*?)</script>",html,re.S)
assert js
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as file:
    file.write(js.group(1))
    file.flush()
    subprocess.run(["node","--check",file.name],check=True)
print("Hosted review studio local-only and HTML/JS checks passed")
