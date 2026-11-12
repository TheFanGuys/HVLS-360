"""Bind release authorization to selected image bytes, framing and metadata.

Manuscript checksum remains separate. This digest never grants authorization.
"""
import hashlib
import json
from pathlib import Path


def digest(root, slug):
    root = Path(root).resolve()
    manifest = root / 'editorial/media/article-images.json'
    media = json.loads(manifest.read_text())['items'].get(slug) if manifest.exists() else None
    assets = {}
    if media:
        path = root / media['file']
        if not path.resolve().is_relative_to(root) or not path.is_file():
            raise ValueError('Selected release media missing or unsafe')
        assets[media['file']] = hashlib.sha256(path.read_bytes()).hexdigest()
    # Include inline original illustrations as well as the selected lead.
    import re
    draft = root / 'editorial/drafts' / (slug + '.md')
    for name in re.findall(r'\]\(\.\./\.\./(editorial/media/[^)]+)\)', draft.read_text()):
        path = root / name
        if not path.resolve().is_relative_to(root) or not path.is_file():
            raise ValueError('Inline release media missing or unsafe')
        assets[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    payload = {'media': media, 'assets': assets}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def validate(root, slug, record):
    # No historic live news exists to grandfather. All selected-media releases bind bytes/captions/framing.
    root = Path(root)
    if (root / 'editorial/media/article-images.json').exists() or record.get('release_inputs_sha256'):
        if record.get('release_inputs_sha256') != digest(root, slug):
            raise ValueError('Release image bytes or presentation changed after authorization')
