from pathlib import Path
import re
import subprocess
import tempfile
html=(Path(__file__).resolve().parents[1]/"office"/"media-desk.html").read_text()
assert "No images are downloaded or published here" in html
assert "Image usage rights checked" in html
assert "local_visual_review_not_publication" in html
assert "innerHTML" not in html
script=re.search(r"<script>(.*?)</script>",html,re.S)
assert script
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as f:
 f.write(script.group(1));f.flush()
 subprocess.run(["node","--check",f.name],check=True)
print("Media desk syntax and safeguards passed")
