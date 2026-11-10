from pathlib import Path
import re
import subprocess
import tempfile
html=(Path(__file__).resolve().parents[1]/"office"/"technical-review.html").read_text()
assert "Technical Review Desk" in html
assert "not a licensed engineering service" in html
assert "localStorage" in html
assert "innerHTML" not in html
assert "rel='noopener noreferrer'" in html
script=re.search(r"<script>(.*?)</script>",html,re.S)
assert script
with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as f:
    f.write(script.group(1));f.flush()
    subprocess.run(["node","--check",f.name],check=True)
print("Technical review desk syntax and safety checks passed")
