from pathlib import Path
import re
import subprocess
import tempfile
html=(Path(__file__).resolve().parents[1]/"office"/"article-editor.html").read_text()
assert "publisher_approved:false" in html
assert "unapproved_draft" in html
assert "NOT approved or published" in html
assert "localStorage" in html
assert "innerHTML" not in html
script=re.search(r"<script>(.*?)</script>",html,re.S)
assert script
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as f:
 f.write(script.group(1));f.flush()
 subprocess.run(["node","--check",f.name],check=True)
print("Article editor safety and JavaScript syntax checks passed")
