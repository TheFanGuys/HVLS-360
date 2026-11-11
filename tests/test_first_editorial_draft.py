from pathlib import Path
draft=Path(__file__).resolve().parents[1]/"editorial"/"drafts"/"hvls-air-movement-vs-ventilation.md"
text=draft.read_text(encoding="utf-8")
assert 'publication_allowed: false' in text
assert 'publisher_approval: "Required"' in text
assert 'https://learn.bigassfans.com/design-guide' in text
assert 'https://www.energy.gov/articles/' in text
review=(draft.parent.parent/'reviews'/'hvls-air-movement-vs-ventilation-review.md').read_text()
assert 'Technical review needed' in review
assert 'Publisher approval:** Not requested' in review
assert "2.1 (Thermal Comfort)" in text
assert "1.3 (Thermal Comfort)" not in text
print("First editorial draft safeguards and BAF source section citation passed")
