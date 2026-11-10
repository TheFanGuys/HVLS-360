from pathlib import Path
draft=Path(__file__).resolve().parents[1]/"editorial"/"drafts"/"hvls-air-movement-vs-ventilation.md"
text=draft.read_text(encoding="utf-8")
assert 'publication_allowed: false' in text
assert 'publisher_approval: "Required"' in text
assert 'https://learn.bigassfans.com/design-guide' in text
assert 'https://www.energy.gov/articles/' in text
assert 'Technical review needed' in text
assert 'Publisher approval: Not requested' in text
print("First editorial draft safeguards passed")
