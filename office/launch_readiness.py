#!/usr/bin/env python3
"""Audit release-planning metadata. Never creates approvals or public files."""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def audit(root=ROOT):
    root=Path(root)
    package=json.loads((root/'office/launch-package.json').read_text())
    registry=json.loads((root/'office/editorial-queue.json').read_text())
    errors=[]
    if package.get('publication_allowed') is not False:
        errors.append('Launch package must not authorize publication')
    expected={x['slug'] for x in registry['items']}
    items=package.get('items',[])
    if len(items)!=len(expected) or {x.get('slug') for x in items}!=expected:
        errors.append('Launch package must match every registered manuscript exactly once')
    for item in items:
        slug=item.get('slug','')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):
            errors.append('Invalid launch slug');continue
        path=root/'editorial/drafts'/(slug+'.md')
        if not path.is_file():
            errors.append(slug+': draft missing');continue
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=item.get('draft_sha256'):
            errors.append(slug+': launch packet stale; recheck copy against current manuscript')
        text=raw.decode('utf-8')
        front=re.match(r'\A---\s*\n([\s\S]*?)\n---\s*\n',text)
        for key,low,high in [('seo_title',20,70),('seo_description',100,170)]:
            value=item.get(key,'')
            if not isinstance(value,str) or not low<=len(value)<=high:
                errors.append(slug+': '+key+' outside editorial length range')
            match=re.search(r'^'+key+r': (.+)$',front[1] if front else '',re.M)
            try:metadata=json.loads(match[1]) if match else None
            except ValueError:metadata=None
            if value!=metadata:errors.append(slug+': '+key+' differs from manuscript')
        if item.get('publisher_approved') is not False:
            errors.append(slug+': launch planning is not approval')
        if item.get('distribution_status')!='held_for_article_approval_and_separate_channel_authorization':
            errors.append(slug+': distribution authorization boundary missing')
        related=item.get('related_story_candidates',[])
        if len(related)!=len(set(related)) or any(x not in expected or x==slug for x in related):
            errors.append(slug+': invalid related-story candidate')
    return errors

if __name__=='__main__':
    problems=audit()
    for problem in problems:print('LAUNCH HOLD:',problem)
    if problems:raise SystemExit(1)
    print('Launch metadata checked for all registered drafts. Technical/media holds and founder approval remain required.')
