#!/usr/bin/env python3
"""Static safety checks for Publisher Command Center; browser testing remains separate."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile

path=Path(__file__).resolve().parents[1]/"office"/"command-center.html"
html=path.read_text(encoding="utf-8")
class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.duplicates=[]
        self.scripts=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        if tag=="script":self.scripts+=1
p=Check()
p.feed(html)
assert not p.duplicates, "Duplicate IDs: "+str(p.duplicates)
for id in ("items","importResearch","researchFile","add","export","import","clear","modal","entryForm","total","review","approved"):
    assert id in p.ids, "Missing control: "+id
assert p.scripts==1, "Expected exactly one local script"
assert "Approved locally" in html
assert "publishing and spending are separate publisher actions" in html.lower()
assert 'name="robots" content="noindex,nofollow,noarchive"' in html
assert "https://api.github.com" not in html
assert "Import research report" in html
assert "eval(" not in html
assert "research-latest.json" in html, "Missing research feed integration"
assert "syncResearch" in p.ids, "Missing research sync control"
js=re.search(r"<script>(.*?)</script>",html,re.S)
assert js, "Inline script not found"
with tempfile.NamedTemporaryFile(suffix=".js",mode="w",encoding="utf-8") as temp:
    temp.write(js.group(1));temp.flush()
    subprocess.run(["node","--check",temp.name],check=True)
print("Command Center structural and JavaScript syntax checks passed.")
