from pathlib import Path
import re
import subprocess
import tempfile
html=(Path(__file__).resolve().parents[1]/"office"/"first-article-review.html").read_text()
assert "Load first article package" in html
assert "air-movement-vs-ventilation.svg" in html
assert "img.loading='lazy'" in html
assert "renderMarkdown(id,raw)" in html
assert "innerHTML" not in html
js=re.search(r"<script>(.*?)</script>",html,re.S)
assert js
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as f:
 f.write(js.group(1));f.flush()
 subprocess.run(["node","--check",f.name],check=True)
print("First article one-tap preview checks passed")
