# Editorial Director — November 11, 2026

All eight manuscripts remain in founder review. No approval records, public article files, homepage, RSS or sitemap were changed. Technical and media holds remain open.

## Handoff and repository evidence

PROJECT-HANDOFF.md was not present in the repository or attached project files. The handoff supplied in this conversation and PROJECT-HQ.md were used. Baseline: main 33b1b80.

The deployed Review Studio was inspected in a browser at https://thefanguys.github.io/HVLS-360/office/first-article-review.html . It offered only local save, restore and export, with GitHub Read/Edit links. Local edits did not flow into the repository. A single shared recovery slot could be overwritten by another article. Restore required loading a file first.

## Copy pass

| Manuscript | Specific changes | Remaining hold |
| --- | --- | --- |
| Air movement / ventilation | Replaced abstract conclusion with acceptance criteria; shortened claims heading | Technical and diagram review |
| ABB IP66 | Removed repeated lead argument and bypass preamble; made environmental limits actionable | Exact drive variant and technical review |
| CFEI | Rewrote lead around a submittal; separated laboratory evidence and installed acceptance criteria | Current regulatory applicability and technical review |
| Greenheck DS | Led with manual shipping cutoff; fixed broken labor-claim sentence; replaced generic ending with submittal request | Manual/controller review and image rights |
| Powerfoil 6 | Led with four mobilization decisions; cut duplicated inspection and wiring language | Mounting, electrical and fire-relay review |
| Scissor lift | Removed duplicate load sentence; tied closing to estimate and mobilization | Qualified access-equipment review |
| VividAir / GFY | Removed unsupported prevalence language about a “recurring mistake”; cut brand cheerleading and promises of future coverage | Hardware generations and controls review |
| TAZ 72 | Qualified photographic identification; removed internal image-selection history from reader copy; replaced generic conclusion with discharge-path task | Nameplate, captions and technical review |

Existing source URLs, numerical specifications, manual revisions and attributed claims were preserved. This was a copy pass, not a fresh independent technical sign-off. No sources were silently certified current. The internal verification records remain with the manuscripts.

## Shared save path

Connect with a repository-scoped fine-grained GitHub token (Contents read/write), entered in the Studio password field, never in chat. It is kept only in memory. Closing/reloading requires reconnecting. GitHub Read/Edit remains an alternative using GitHub's own signed-in editor.

Open in Studio → authenticated Contents API read from main → edit and preview → Save to GitHub → Contents API write with the originally opened blob SHA → reread and compare exact bytes and returned SHA → show verified commit. The saved file is editorial/drafts/<slug>.md, the same manuscript linked by the review queue. A second device must connect and reopen it. Branch rules can block direct main writes; errors retain the local text.

A save rejects missing or approved manuscript frontmatter. It only addresses the eight listed draft paths, never approval or publication endpoints. Founder release still needs the separate approval record bound to the manuscript checksum. This client check is not a replacement for GitHub permissions or the repository publication guard.

Local recovery copies are per filename, with the originating blob SHA. Reopening offers recovery. A recovery copy based on a different GitHub revision disables remote saving until the user downloads/reconciles and reopens the current manuscript. HTTP conflicts preserve edits instead of overwriting someone else's draft. Legacy recovery is offered only for a matching filename. Successful remote saves remove the recovery copy.

## Verification and limits

- 152 Python tests passed; publication guard passed.
- Executable Node tests passed: Unicode, two independent clients, stale SHA conflict, approval block, access denial and mismatched post-save readback.
- DOM integration with a simulated GitHub store passed: local recovery after closing/reopening, exact reviewed manuscript update, stale-device conflict, blocked stale recovery, fresh-device reopen and no credential persistence.
- The actual deployed page was inspected before deployment; it still has the old local-only interface.
- Chromium launch was blocked by this workspace's socket permissions. No iPhone-size screenshot, physical iPhone Safari, real cross-device browser save, or authenticated live Studio write was verified. Simulated clients/DOM tests must not be described as a live-device acceptance test.
- Git CLI push lacked credentials; repository delivery uses the connected GitHub API instead.
