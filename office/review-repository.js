/* GitHub draft storage. Credentials live in memory only; no publication endpoints. */
(function (root) {
'use strict';
const base = 'https://api.github.com/repos/TheFanGuys/HVLS-360/contents/';
const valid = slug => /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug);
const encode = text => btoa(Array.from(new TextEncoder().encode(text), b => String.fromCharCode(b)).join(''));
const decode = text => new TextDecoder().decode(Uint8Array.from(atob(text.replace(/\s/g, '')), c => c.charCodeAt(0)));
function reviewOnly(text) {
 const front = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
 if (!front || !/^publication_allowed: false\s*$/m.test(front[1]) || !/^status: "EDITORIAL DRAFT — NOT APPROVED"\s*$/m.test(front[1])) throw Error('Save blocked: manuscript must remain an unapproved editorial draft.');
 return text;
}
function client(token, transport = fetch) {
 token=token.trim();
 if (!token) throw Error('Enter a repository-scoped GitHub token.');
 async function request(slug, method = 'GET', body) {
  if (!valid(slug)) throw Error('Invalid article identifier');
  const response = await transport(base + 'editorial/drafts/' + slug + '.md' + (method === 'GET' ? '?ref=main' : ''), {
   method, cache: 'no-store', headers: {Accept:'application/vnd.github+json', Authorization:'Bearer '+token, 'X-GitHub-Api-Version':'2022-11-28', ...(body ? {'Content-Type':'application/json'} : {})},
   ...(body ? {body:JSON.stringify(body)} : {})
  });
  if (!response.ok) throw Error([409,422].includes(response.status) ? 'Conflict: repository draft changed. Your edit is retained; download it, reopen GitHub draft and reconcile before saving.' : 'GitHub request failed (HTTP '+response.status+'). Check repository access; your edit is retained.');
  return response.json();
 }
 async function read(slug) { const file = await request(slug); return {sha:file.sha, content:decode(file.content)}; }
 return {read, async save(slug, content, sha) {
  reviewOnly(content);
  if (!sha) throw Error('Open the GitHub draft before saving.');
  const result = await request(slug, 'PUT', {branch:'main', sha, content:encode(content), message:'Founder review: revise '+slug+' (unapproved)'});
  const verified = await read(slug);
  if (verified.content !== content || verified.sha !== result.content.sha) throw Error('Commit created, but latest draft differs. Reopen and reconcile before further edits.');
  return {...verified, commit:result.commit.sha};
 }};
}
root.HVLSReviewRepository = {client, reviewOnly};
})(globalThis);
