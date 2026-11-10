# HVLS 360 — Publisher Office Board

## Operating rules
The public website stays on `main`. Work is prepared in feature branches and reviewed through pull requests. No draft article should be merged without the publisher's explicit approval. A green automated check means basic technical checks passed, **not** that a human verified every factual or visual claim.

## Current queues
| Department | Work | Status |
| --- | --- | --- |
| Web / Editorial | V3 magazine homepage, navigation, article archive | Draft PR #1, awaiting final review |
| Visual Media | Big Fan Guys hero image; source rights, crop and alt text | Pending visual review |
| Quality Control | Automated HTML/SEO/image metadata checks | In development |
| Research | Tuesday/Friday monitoring and Monday brief intake | Not yet integrated |
| Marketing / SEO | OpenSEO baseline and editorial search topics | Project created; audit pending |
| COO | Consolidated weekly publisher briefing | Not yet automated |

## Image workflow
1. Collect the original image or a permitted site asset.
2. Record rights, source and edit history in `media/assets.json`.
3. Prepare a technically faithful crop and optimized image.
4. Visual fact-check and editorial review.
5. Set `review_status` to approved only after publisher approval.

## Next
Review PR #1; finish a visual image approval; run quality gate on a PR; then add research discovery and COO summaries. Do not imply autonomous agents are active before successful tests.
